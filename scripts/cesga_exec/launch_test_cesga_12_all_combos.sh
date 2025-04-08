#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test-12-all-combos"

export DATASET_PATH="$HOME/CienaLLM/data/test-datasets-small/cesga-test-12/sample/"
export ANNOTATION_PATH="$HOME/CienaLLM/data/test-datasets-small/cesga-test-12/dataset.csv"

export CIENA_LLM_MODEL="llama3.1:8b-instruct-q4_K_M"
export CIENA_LLM_LANGUAGE="en"

export CIENA_LLM_EVENT_IDENTIFICATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"

export SLURM_JOB_TIME="0:10:00"

bools=("True" "False")
categories=("simple" "description")

for summarization in "${bools[@]}"; do
    for response_parsing in "${bools[@]}"; do
        for self_criticism in "${bools[@]}"; do
            for cot in "${bools[@]}"; do
                for category in "${categories[@]}"; do
                    export CIENA_LLM_SUMMARIZATION_ENABLE="$summarization"
                    export CIENA_LLM_RESPONSE_PARSING_ENABLE="$response_parsing"
                    export CIENA_LLM_COT_ENABLE="$cot"
                    export CIENA_LLM_SELF_CRITICISM_ENABLE="$self_criticism"
                    export CIENA_LLM_IMPACT_PROMPT_CATEGORY="$category"

                    export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/model_$CIENA_LLM_MODEL/summarization_$CIENA_LLM_SUMMARIZATION_ENABLE/response_parsing_$CIENA_LLM_RESPONSE_PARSING_ENABLE/self_criticism_$CIENA_LLM_SELF_CRITICISM_ENABLE/cot_$CIENA_LLM_COT_ENABLE/impact_prompt_category_$CIENA_LLM_IMPACT_PROMPT_CATEGORY/"

                    mkdir -p $RESULTS_DIR

                    cd $HOME/CienaLLM/ciena_llm

                    sbatch \
                        -t $SLURM_JOB_TIME \
                        -o $RESULTS_DIR/slurm.out \
                        -e $RESULTS_DIR/slurm.err \
                        -c 32 \
                        --gres=gpu:a100:1 \
                        $DIR/ciena_sbatch.sh

                done
            done
        done
    done
done
