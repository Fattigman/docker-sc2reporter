docker exec -i docker-sc2reporter_mongo_1 /usr/bin/mongodump  --db sarscov2_standalone --out /dump

docker cp docker-sc2reporter_mongo_1:/dump /Users/jacobkarlstrom/Projects/SarsCov2/docker-sc2reporter/utils

mv ./dump/sarscov2_standalone ../mongo-seed/sarscov2_standalone

rm -r dump