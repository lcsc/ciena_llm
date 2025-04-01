#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="news_elpais_all_drought_seqia_no_drought_cienallm"

export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/$(date +%Y-%m-%d_%H-%M-%S)/"

export DATASET_PATH="$HOME/CienaLLM/data/news-elpais-all-drought-seqia-no-drought-cienallm/sample/"

export CIENA_LLM_MODEL="gemma2:9b"
export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_SUMMARIZATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"
export CIENA_LLM_RESPONSE_PARSING_ENABLE="False"
export CIENA_LLM_COT_ENABLE="False"
export CIENA_LLM_SELF_CRITICISM_ENABLE="False"
export CIENA_LLM_IMPACT_PROMPT_CATEGORY="simple"

export SLURM_JOB_TIME="12:00:00"

mkdir -p $RESULTS_DIR

cd $HOME/CienaLLM/ciena_llm

sbatch \
    -t $SLURM_JOB_TIME \
    -o $RESULTS_DIR/slurm.out \
    -e $RESULTS_DIR/slurm.err \
    $DIR/ciena_sbatch.sh
