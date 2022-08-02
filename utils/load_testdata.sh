#!/bin/bash

./load_run_to_db.pl ./testdata/results/210319_NB501697_0239_AHMV7CAFX2/
./add_metadata_to_db.pl ./testdata/metadata/test.csv
./add_ct_to_db.pl $(date +%Y-%m-%d) ./testdata/qpcr/quantstudio_test.txt
