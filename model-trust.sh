#!/bin/bash

cd $CODE_PATH/stackgan

python api-server/api.py --model_path $MODEL_PATH
