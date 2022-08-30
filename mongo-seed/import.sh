#! /bin/bash

#chmod -R ugo+rwx /mongo-seed
mongorestore --host=mongodb  --db sarscov2_standalone /mongo-seed/sarscov2_standalone