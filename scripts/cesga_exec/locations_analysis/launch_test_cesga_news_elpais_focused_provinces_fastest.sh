#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." &>/dev/null && pwd)"

export TEST_NAME="news_elpais_focused_provinces"
export SCRIPT_NAME="tests/v0.3_tests/test_cesga_drought.py"

export CIENA_LLM_MODEL="qwen2.5:3b-instruct-q4_K_M"

export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/fastest/$(date +%Y-%m-%d_%H-%M-%S)/"

export DATASET_PATH="$HOME/CienaLLM/data/news-elpais-focused-annotated-provinces/sample/"

export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_SUMMARIZATION_ENABLE="False"
export CIENA_LLM_EVENT_IDENTIFICATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="False"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="True"
export CIENA_LLM_COT_ENABLE="False"
export CIENA_LLM_SELF_CRITICISM_ENABLE="False"
export CIENA_LLM_IMPACT_PROMPT_CATEGORY="description"

export SLURM_JOB_TIME="0:30:00"
export SLURM_CPUS=32
export SLURM_GPUS=1

mkdir -p $RESULTS_DIR

cd $HOME/CienaLLM/ciena_llm

sbatch \
    -t $SLURM_JOB_TIME \
    -o $RESULTS_DIR/slurm.out \
    -e $RESULTS_DIR/slurm.err \
    -c $SLURM_CPUS \
    --gres=gpu:a100:$SLURM_GPUS \
    $DIR/ciena_sbatch.sh
