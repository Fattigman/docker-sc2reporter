use mongodb::{Client, bson::{Document, doc, oid::ObjectId}};
use serde::{Deserialize, Serialize};
use futures::stream::TryStreamExt;
use std::error::Error;
use std::{cmp};
use ndarray::{arr2} ;
use tokio;

// Define the schema for the mongodb collections:
 #[derive(Serialize, Deserialize, Debug)]
 struct Sample {
    sample_id: String,
 }

 #[derive(Serialize, Deserialize, Debug)]
struct Depth {
    #[serde(rename = "_id", skip_serializing_if = "Option::is_none")]
    _id: Option<ObjectId>,
    sample_id: String,
    sample_oid: String,
    A: u16,
    T: u16,
    G: u16,
    C: u16,
    REFSKIP: u16,
    DEL: u16,
    pos: u16,
    dp: u16,
 }

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    
   // Load the MongoDB connection string from an environment variable:
   // /(Switch to env variable later)
   let client_uri = "mongodb://localhost:27017";

   // A Client is needed to connect to MongoDB:
   let client = Client::with_uri_str(client_uri).await.unwrap();
   let database = client.database("sarscov2_standalone");
   
   // Define the collection to query:
   let sample_collection = database.collection::<Sample>("sample");
   let mut samples = sample_collection.find(None,None).await?;
   let mut sample_names : Vec<String> = Vec::new();
   
   // Get all the sample names
   while let Some(sample) = samples.try_next().await? {
      sample_names.push(sample.sample_id);
   }

   let depth_collection = database.collection::<Depth>("depth");
   let mut temp : [f32; 4];
   let mut index : Vec<String> = Vec::new();
   let mut matrix: Vec<Vec<f32>> = Vec::new();
   for name in &sample_names {
      let mut depths = depth_collection.find(doc! {"sample_id": name},None).await?;
      let mut column : Vec<f32> = Vec::new();
      // Fetch all depth information for a sample
      // Calculate an array for each sample ranging from 0 to 1 based on the frequency of each nucleotide
      while let Some(depth) = depths.try_next().await? {
         let max_value = cmp::max(cmp::max(depth.A, depth.T), cmp::max(depth.G, depth.C));
         let temp = [depth.A as f32, depth.T as f32, depth.G as f32, depth.C as f32];
         for i in 0..4 {
            column.push(temp[i] / max_value as f32);
         }
         // Appends index vector with each position and nucleotide
         for char in ['A', 'T', 'G', 'C'].iter() {
            if ! index.contains(&format!("{}_{}", depth.pos, char)){
               index.push(format!("{}_{}", depth.pos, char));
            }
         }
      }
      matrix.push(column);
   }
   Ok(())
}