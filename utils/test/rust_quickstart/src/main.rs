use mongodb::{Client, bson::{Document, doc,  oid::ObjectId}};
use serde::{Deserialize, Serialize};
use std::env;
use std::error::Error;
use futures::stream::StreamExt;
use tokio;

#[derive(Serialize, Deserialize, Debug)]
struct Depth {
    #[serde(rename = "_id", skip_serializing_if = "Option::is_none")]
    _id: Option<ObjectId>,
    sample_id: String,
    sample_oid: String,
    A: i32,
    T: i32,
    G: i32,
    C: i32,
    REFSKIP: i32,
    DEL: i32,
    pos: i16,
    dp: i32,
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

    while let Some(result) = results.next().await {
        // Use serde to deserialize into the MovieSummary struct:
        let doc: Depth = bson::from_document(result?)?;
        println!("* {:?}", doc);
     }
   Ok(())
}