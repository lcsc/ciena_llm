#!/bin/bash

REMOTE_PATH="CienaLLM/ciena_llm/results/"
LOCAL_PATH="/home/javier/Developer/ciena_llm/results_cesga/"

rsync -a --info=progress2 --info=name0 -e ssh cesga:$REMOTE_PATH $LOCAL_PATH
rsync -a --info=progress2 --info=name0 -e ssh cesga_alex:$REMOTE_PATH $LOCAL_PATH
