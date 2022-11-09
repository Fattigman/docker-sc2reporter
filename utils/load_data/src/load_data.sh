#!/bin/bash

# ./load_run_to_db.pl /data/bnf/dev/jonas/sarscov2/reporter/testdata/results/210319_NB501697_0239_AHMV7CAFX2_small/
# ./add_metadata_to_db.pl /data/bnf/dev/jonas/sarscov2/reporter/testdata/metadata/test.csv
# ./add_ct_to_db.pl 2022-02-03 /data/bnf/dev/jonas/sarscov2/reporter/testdata/qpcr/quantstudio_test.txt

python ./db_init.py

perl ./load_run_to_db.pl $LOAD_DATA_RESULTS
perl ./add_metadata_to_db.pl $LOAD_DATA_META
perl ./add_ct_to_db.pl $(date +%Y-%m-%d) $LOAD_DATA_QPCR

python ./add_snp_mtx.py 

echo "Insertion complete"