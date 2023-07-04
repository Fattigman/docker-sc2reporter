use mongodb::{Client, bson::{Document, doc, oid::ObjectId}};
use serde::{Deserialize, Serialize};
use futures::stream::TryStreamExt;
use std::error::Error;
use std::{cmp};
use tokio;

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
    
    let pipeline: Vec<Document> = vec![
        doc! {
           // sort by year, ascending:
           "$sort": {
              "sample_id": 1
           }
        },
     ];
   // Load the MongoDB connection string from an environment variable:
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
   for name in &sample_names {
      let mut depths = depth_collection.find(doc! {"sample_id": name},None).await?;
      while let Some(depth) = depths.try_next().await? {
         let max_value = cmp::max(cmp::max(depth.A, depth.T), cmp::max(depth.G, depth.C));
         let mut temp = [depth.A as f32, depth.T as f32, depth.G as f32, depth.C as f32];
         for i in 0..4 {
            temp[i] = temp[i] / max_value as f32;
         }
         println!("{:?}", temp);
      }
   }
   Ok(())
}