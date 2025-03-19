#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export CIENA_LLM_DIR="$HOME/CienaLLM"
export TEST_NAME="test_cesga_short_env_delete" # REMOVE Rename test
export RESULTS_DIR="$CIENA_LLM_DIR/results/$TEST_NAME/$(date +%Y%m%d_%H%M%S)/"
export DATASET_PATH="$CIENA_LLM_DIR/data/test-datasets-small/news-elpais-binary-2T-1F/sample"
export CIENA_LLM_MODEL="llama3.2:2b" # TODO does not exist, pull and warmup model
export CIENA_LLM_LANGUAGE="en"

mkdir -p $RESULTS_DIR

# TODO rename file to ciena_sbatch_test_short.sh
sbatch $DIR/ciena_sbatch_test_short.sh -o $RESULTS_DIR/slurm.out -e $RESULTS_DIR/slurm.err
