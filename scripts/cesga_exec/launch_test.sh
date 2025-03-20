#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

export TEST_NAME="test_cesga_short"
export RESULTS_DIR="$HOME/CienaLLM/ciena_llm/results/$TEST_NAME/$(date +%Y-%m-%d_%H-%M-%S)/" # TODO do not do only with date, put something more descriptive
export DATASET_PATH="$HOME/CienaLLM/data/test-datasets-small/news-elpais-binary-2T-1F/sample"
export CIENA_LLM_MODEL="llama3.2:3b"
export CIENA_LLM_LANGUAGE="en"

mkdir -p $RESULTS_DIR

module load cesga/2020 python/3.10.8
cd $HOME/CienaLLM/ciena_llm

# TODO do always?
git pull
poetry lock
poetry install

sbatch -o $RESULTS_DIR/slurm.out -e $RESULTS_DIR/slurm.err $DIR/ciena_sbatch_test_short.sh
