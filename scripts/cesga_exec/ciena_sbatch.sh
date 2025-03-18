#!/bin/bash
#----------------------------------------------------
# CienaLLM (test)
#----------------------------------------------------
#SBATCH -J ciena_llm_test       # Job name
#SBATCH -o ciena_llm_test_%j.o  # Name of stdout output file
#SBATCH -e ciena_llm_test_%j.e  # Name of stderr output file
#SBATCH -c 32                   # Cores per task requested
#SBATCH -t 00:10:00             # Run time (hh:mm:ss)
#SBATCH --mem-per-cpu=3G        # Memory per core demandes
#SBATCH --gres=gpu:a100:1       # Number of GPUs

# Load Ollama and Python modules
module load cesga/2020 ollama/0.5.13 python/3.10.8

cd $HOME/CienaLLM/ciena_llm

# REMOVE
nvidia-smi > gpu_info.log

# Restore the poetry.lock file with the correct version
cp poetry.lock.ft3 poetry.lock

# Load Python and Poetry
pip install poetry

# poetry lock # For this specific poetry version
poetry install

# Maximum number of retries (for port and server check)
MAX_RETRIES=5

# Set the Ollama port
if [ -z "$SLURM_JOBID" ]; then
    export OLLAMA_PORT=11434
else
    export OLLAMA_PORT=$(expr 10000 + $(echo -n $SLURM_JOBID | tail -c 4))
fi

# Check if the port is already in use and increment if necessary
RETRY_COUNT=0
while netstat -tuln | grep -q ":$OLLAMA_PORT"; do
    echo "Port $OLLAMA_PORT is already in use. Incrementing..."
    RETRY_COUNT=$(expr $RETRY_COUNT + 1)
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Error: Could not find an available port after $MAX_RETRIES retries."
        exit 1
    fi
    export OLLAMA_PORT=$(expr $OLLAMA_PORT + 1)
done

export OLLAMA_HOST=$(hostname -i):$OLLAMA_PORT
export OLLAMA_TMPDIR=$TMPDIR

echo "OLLAMA_PORT: $OLLAMA_PORT"
echo "OLLAMA_HOST: $OLLAMA_HOST"
echo "OLLAMA_TMPDIR: $OLLAMA_TMPDIR"

# Start the Ollama server
ollama serve > ollama_server.log 2>&1 &

# Check if the Ollama server is running
RETRY_COUNT=0
while ! curl -s $OLLAMA_HOST | grep -q "Ollama is running"; do
    echo "Ollama server is not running. Retrying..."
    RETRY_COUNT=$(expr $RETRY_COUNT + 1)
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Error: Ollama server is not running after $MAX_RETRIES retries."
        exit 1
    fi
    sleep 1
done

# Run the test
poetry run python tests/test_cesga_short.py

