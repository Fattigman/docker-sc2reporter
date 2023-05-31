use mongodb::{Client, bson::{Document, doc,  oid::ObjectId}};
use serde::{Deserialize, Serialize};
use std::{cmp, env};
use std::error::Error;
use futures::stream::StreamExt;
use tokio;

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
struct MatrixVector {
    sample_id: String,
    array: Vec<f32>,
}
struct Matric {
    array: Vec<MatrixVector>
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
   let client_uri =
      env::var("MONGODB_URI").expect("You must set the MONGODB_URI environment var!");

   // A Client is needed to connect to MongoDB:
   let client = Client::with_uri_str(client_uri).await.unwrap();

   // 
   let database = client.database("sarscov2_standalone");

    let depth_collection : mongodb::Collection<Vec<Depth>> = database.collection("depth");
    
    let mut results = depth_collection.aggregate(pipeline, None).await?;
    // Declare variables
    let mut sample_name : String = "no_col".to_string();
    let mut sample_name_vector : Vec<String> = Vec::new();
    let mut col: Vec<f32> = Vec::new();
    while let Some(result) = results.next().await {
        let doc: Depth = bson::from_document(result?)?;
        if doc.sample_id != sample_name{
            sample_name = doc.sample_id;
            sample_name_vector.push(sample_name.clone());
            col.clear();
        }
        // Calculate the max frequency of the four nucleotides
        let max_value = cmp::max(cmp::max(doc.A, doc.T), cmp::max(doc.G, doc.C));
    }
    println!("col: {:?}", sample_name_vector);
   Ok(())
}