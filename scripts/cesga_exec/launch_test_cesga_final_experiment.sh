#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test-final-experiment"

export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="True"

bools=("True" "False")
categories=("simple" "description")

export DATASETS="news-elpais-grupoz-impact-complete-subset news-elpais-sample-194-annotated-e2e"

export MODELS="llama3.2:3b-instruct-q4_K_M llama3.1:8b-instruct-q4_K_M"
# export MODELS="llama3.2:3b-instruct-q4_K_M llama3.1:8b-instruct-q4_K_M llama3.1:8b-instruct-fp16 llama3.3:70b-instruct-q4_K_M qwen2.5:3b-instruct-q4_K_M qwen2.5:7b-instruct-q4_K_M qwen2.5:7b-instruct-fp16 qwen2.5:72b-instruct-q4_K_M"
# export MODELS="llama3.2:3b-instruct-q4_K_M llama3.1:8b-instruct-q4_K_M llama3.1:8b-instruct-fp16 llama3.3:70b-instruct-q4_K_M gemma2:2b-instruct-q4_K_M gemma2:9b-instruct-q4_K_M gemma2:9b-instruct-fp16 gemma2:27b-instruct-q4_K_M qwen2.5:3b-instruct-q4_K_M qwen2.5:7b-instruct-q4_K_M qwen2.5:7b-instruct-fp16 qwen2.5:72b-instruct-q4_K_M"

for dataset in $DATASETS; do
    for model in $MODELS; do
        if [[ $model == *"llama3.1"* || $model == *"llama3.3"* || $model == *"gemma2:27b"* || $model == *"qwen2.5:72b"* ]]; then
            export SLURM_JOB_TIME="2:00:00"
        else
            export SLURM_JOB_TIME="0:30:00"
        fi
        for summarization in "${bools[@]}"; do
            for response_parsing in "${bools[@]}"; do
                for self_criticism in "${bools[@]}"; do
                    for cot in "${bools[@]}"; do
                        for category in "${categories[@]}"; do

                            export DATASET_PATH="$HOME/CienaLLM/data/$dataset/sample/"

                            export CIENA_LLM_MODEL="$model"
                            export CIENA_LLM_SUMMARIZATION_ENABLE="$summarization"
                            export CIENA_LLM_RESPONSE_PARSING_ENABLE="$response_parsing"
                            export CIENA_LLM_COT_ENABLE="$cot"
                            export CIENA_LLM_SELF_CRITICISM_ENABLE="$self_criticism"
                            export CIENA_LLM_IMPACT_PROMPT_CATEGORY="$category"

                            export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/dataset_$dataset/model_$CIENA_LLM_MODEL/summarization_$CIENA_LLM_SUMMARIZATION_ENABLE/response_parsing_$CIENA_LLM_RESPONSE_PARSING_ENABLE/self_criticism_$CIENA_LLM_SELF_CRITICISM_ENABLE/cot_$CIENA_LLM_COT_ENABLE/impact_prompt_category_$CIENA_LLM_IMPACT_PROMPT_CATEGORY/"

                            mkdir -p $RESULTS_DIR

                            cd $HOME/CienaLLM/ciena_llm

                            sbatch \
                                -t $SLURM_JOB_TIME \
                                -o $RESULTS_DIR/slurm.out \
                                -e $RESULTS_DIR/slurm.err \
                                $DIR/ciena_sbatch.sh
                        done
                    done
                done
            done
        done
    done
done
