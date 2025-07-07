#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test-final-experiment"
export SCRIPT_NAME="tests/test_cesga_drought.py"

export CIENA_LLM_LANGUAGE="en"
export CIENA_LLM_EVENT_IDENTIFICATION_ENABLE="False"
export CIENA_LLM_IMPACT_EXTRACTION_ENABLE="True"
export CIENA_LLM_LOCATION_EXTRACTION_ENABLE="False"
export CIENA_LLM_STRUCTURED_OUTPUT_MODE="prompt"

bools=("True" "False")
categories=("simple" "description")

export MODELS="llama3.1:8b-instruct-fp16 llama3.1:8b-instruct-q4_K_M llama3.2:3b-instruct-q4_K_M llama3.3:70b-instruct-q4_K_M qwen2.5:3b-instruct-q4_K_M qwen2.5:7b-instruct-q4_K_M qwen2.5:7b-instruct-fp16 qwen2.5:72b-instruct-q4_K_M gemma3:4b-it-q4_K_M gemma3:12b-it-q4_K_M gemma3:12b-it-fp16 gemma3:27b-it-q4_K_M"

export SLURM_JOB_TIME="10:00:00"
export SLURM_CPUS=64
export SLURM_GPUS=2

export DATASETS="news-elpais-sample-194-annotated-e2e news-elpais-grupoz-impact-complete-subset"

for model in $MODELS; do
    for dataset in $DATASETS; do
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

                            if [ ! -f "$RESULTS_DIR/summary.csv" ]; then
                                echo "$RESULTS_DIR"

                                mkdir -p $RESULTS_DIR

                                cd $HOME/CienaLLM/ciena_llm

                                sbatch \
                                    -t $SLURM_JOB_TIME \
                                    -o $RESULTS_DIR/slurm.out \
                                    -e $RESULTS_DIR/slurm.err \
                                    -c $SLURM_CPUS \
                                    --gres=gpu:a100:$SLURM_GPUS \
                                    $DIR/ciena_sbatch.sh
                            fi
                        done
                    done
                done
            done
        done
    done
done
