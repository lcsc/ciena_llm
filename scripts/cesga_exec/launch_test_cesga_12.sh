#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test-12"

export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/$(date +%Y-%m-%d_%H-%M-%S)/"

export DATASET_PATH="$HOME/CienaLLM/data/test-datasets-small/cesga-test-12/sample/"
export ANNOTATION_PATH="$HOME/CienaLLM/data/test-datasets-small/cesga-test-12/dataset.csv"

export CIENA_LLM_MODEL="llama3.2:3b"
export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_SUMMARIZATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="False"

export SLURM_JOB_TIME="00:10:00"

mkdir -p $RESULTS_DIR

cd $HOME/CienaLLM/ciena_llm

sbatch \
    -t $SLURM_JOB_TIME \
    -o $RESULTS_DIR/slurm.out \
    -e $RESULTS_DIR/slurm.err \
    $DIR/ciena_sbatch.sh
