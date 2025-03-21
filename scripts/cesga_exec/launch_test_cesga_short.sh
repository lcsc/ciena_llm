#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test_cesga_short"

# TODO do not do only with date, put something more descriptive
export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/$(date +%Y-%m-%d_%H-%M-%S)/"

export DATASET_PATH="$HOME/CienaLLM/data/test-datasets-small/news-elpais-binary-2T-1F/sample"

export CIENA_LLM_MODEL="llama3.2:3b"
export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_SUMMARIZATION_ENABLE="True"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="True"

export SLURME_JOB_TIME="00:05:00"

mkdir -p $RESULTS_DIR

module load cesga/2020 python/3.10.8

cd $HOME/CienaLLM/ciena_llm

# TODO do always?
# Maybe, if git pull pulls something new, do lock and install
git pull
poetry lock
poetry install

sbatch \
    -t $SLURME_JOB_TIME \
    -o $RESULTS_DIR/slurm.out \
    -e $RESULTS_DIR/slurm.err \
    $DIR/ciena_sbatch.sh
