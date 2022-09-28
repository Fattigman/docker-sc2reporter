#!/bin/bash

# Load output from arctic pipeline
perl ./load_run_to_db.pl $LOAD_DATA_RESULTS
perl ./add_metadata_to_db.pl $LOAD_DATA_META
perl ./add_ct_to_db.pl $(date +%Y-%m-%d) $LOAD_DATA_QPCR
