#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test-12-all-models"

export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/$(date +%Y-%m-%d_%H-%M-%S)/"

export DATASET_PATH="$HOME/CienaLLM/data/test-datasets-small/cesga-test-12/sample/"
export ANNOTATION_PATH="$HOME/CienaLLM/data/test-datasets-small/cesga-test-12/dataset.csv"

export MODELS="gemma2:2b-instruct-q4_K_M gemma2:9b-instruct-q4_K_M gemma2:9b-instruct-fp16 gemma2:27b-instruct-q4_K_M"
# TODO: Add more models
# export MODELS="llama3.2:3b-instruct-q4_K_M llama3.1:8b-instruct-q4_K_M llama3.1:8b-instruct-fp16 llama3.3:70b-instruct-q4_K_M gemma2:2b-instruct-q4_K_M gemma2:9b-instruct-q4_K_M gemma2:9b-instruct-fp16 gemma2:27b-instruct-q4_K_M qwen2.5:3b-instruct-q4_K_M qwen2.5:7b-instruct-q4_K_M qwen2.5:7b-instruct-fp16 qwen2.5:72b-instruct-q4_K_M"

export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_SUMMARIZATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="False"

export SLURM_JOB_TIME="00:30:00"
# TODO: Change to 3 hours
# export SLURM_JOB_TIME="03:00:00"

mkdir -p $RESULTS_DIR

cd $HOME/CienaLLM/ciena_llm

sbatch \
    -t $SLURM_JOB_TIME \
    -o $RESULTS_DIR/slurm.out \
    -e $RESULTS_DIR/slurm.err \
    -c 32 \
    --gres=gpu:a100:1 \
    $DIR/ciena_sbatch_many_models.sh
# TODO: Add more GPUs
# sbatch \
#     -t $SLURM_JOB_TIME \
#     -o $RESULTS_DIR/slurm.out \
#     -e $RESULTS_DIR/slurm.err \
#     -c 64 \
#     --gres=gpu:a100:2 \
#     $DIR/ciena_sbatch_many_models.sh
