#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export CIENA_LLM_MODEL="qwen2.5:72b-instruct-q4_K_M"
export CIENA_LLM_LANGUAGE="en"

export CIENA_LLM_SUMMARIZATION_ENABLE="False"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="True"
export CIENA_LLM_COT_ENABLE="False"
export CIENA_LLM_SELF_CRITICISM_ENABLE="False"
export CIENA_LLM_IMPACT_PROMPT_CATEGORY="description"

export SLURM_JOB_TIME="24:00:00"
export SLURM_CPUS=64
export SLURM_GPUS=2

for i in {0..29}; do

    export DATASET_PATH="$HOME/CienaLLM/data/news-elpais-hail-filtered/subsets/subset_$i"
    export TEST_NAME="news_elpais_hail_filtered"
    export SCRIPT_NAME="tests/v0.3_tests/test_cesga_hail.py"

    export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/subset_$i/"

    mkdir -p $RESULTS_DIR

    cd $HOME/CienaLLM/ciena_llm

    sbatch \
        -t $SLURM_JOB_TIME \
        -o $RESULTS_DIR/slurm.out \
        -e $RESULTS_DIR/slurm.err \
        -c $SLURM_CPUS \
        --gres=gpu:a100:$SLURM_GPUS \
        $DIR/ciena_sbatch.sh

done
