#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test_cesga_short"
export SCRIPT_NAME="tests/test_cesga_drought.py"

# TODO do not do only with date, put something more descriptive
export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/$(date +%Y-%m-%d_%H-%M-%S)/"

export DATASET_PATH="$HOME/CienaLLM/data/test-datasets-small/news-elpais-binary-2T-1F/sample"

export CIENA_LLM_MODEL="llama3.2:3b"
export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_SUMMARIZATION_ENABLE="True"
export CIENA_LLM_EVENT_IDENTIFICATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="True"
export CIENA_LLM_COT_ENABLE="False"
export CIENA_LLM_SELF_CRITICISM_ENABLE="False"
export CIENA_LLM_IMPACT_PROMPT_CATEGORY="simple"

export SLURM_JOB_TIME="00:05:00"

mkdir -p $RESULTS_DIR

cd $HOME/CienaLLM/ciena_llm

sbatch \
    -t $SLURM_JOB_TIME \
    -o $RESULTS_DIR/slurm.out \
    -e $RESULTS_DIR/slurm.err \
    -c 32 \
    --gres=gpu:a100:1 \
    $DIR/ciena_sbatch.sh
