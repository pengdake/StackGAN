#!/bin/bash

cd $CODE_PATH/stackgan
cp -r $DATASET_PATH/* /tmp/

python ./misc/preprocess_flowers.py /tmp/flowers
python stageI/run_exp.py --dataset_dir /tmp/flowers  --epoch $STAGEI_EPOCH --batch_size $BATCH_SIZE 
python stageII/run_exp.py --pretrained_epoch $STAGEI_EPOCH --epoch $STAGEII_EPOCH --batch_size $BATCH_SIZE  --dataset_dir /tmp/flowers --model_dir $MODEL_PATH
