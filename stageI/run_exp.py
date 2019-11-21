from __future__ import division
from __future__ import print_function

import dateutil
import dateutil.tz
# import datetime
import argparse
import pprint

from misc.datasets import TextDataset
from stageI.model import CondGAN
from stageI.trainer import CondGANTrainer
from misc.utils import mkdir_p
from misc.config import cfg, cfg_from_file


def parse_args():
    parser = argparse.ArgumentParser(description='Train a GAN network')
    parser.add_argument('--epoch', dest='epoch',
                        default=600, type=int)
    parser.add_argument('--batch_size', dest='batch_size',
                        default=64, type=int)
    parser.add_argument('--dataset_dir', dest='dataset_dir', type=str)
    # if len(sys.argv) == 1:
    #    parser.print_help()
    #    sys.exit(1)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    cfg_from_file("stageI/cfg/flowers.yml")

    cfg.TRAIN.MAX_EPOCH = args.epoch
    cfg.TRAIN.BATCH_SIZE = args.batch_size

    print('Using config:')
    pprint.pprint(cfg)

    ## now = datetime.datetime.now(dateutil.tz.tzlocal())
    ## timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

    datadir = args.dataset_dir
    dataset = TextDataset(datadir, cfg.EMBEDDING_TYPE, 1)
    filename_test = '%s/test' % (datadir)
    dataset.test = dataset.get_data(filename_test)
    if cfg.TRAIN.FLAG:
        filename_train = '%s/train' % (datadir)
        dataset.train = dataset.get_data(filename_train)

        ckt_logs_dir = "ckt_logs/%s/%s" % \
            (cfg.DATASET_NAME, cfg.CONFIG_NAME)
        mkdir_p(ckt_logs_dir)
        models_dir = "models/%s/%s" % \
            (cfg.DATASET_NAME, cfg.CONFIG_NAME)
        mkdir_p(models_dir)
    else:
        s_tmp = cfg.TRAIN.PRETRAINED_MODEL
        ckt_logs_dir = s_tmp[:s_tmp.find('.ckpt')]

    model = CondGAN(
        image_shape=dataset.image_shape
    )

    algo = CondGANTrainer(
        model=model,
        dataset=dataset,
        ckt_logs_dir=ckt_logs_dir,
        models_dir=models_dir
    )
    if cfg.TRAIN.FLAG:
        algo.train()
    else:
        ''' For every input text embedding/sentence in the
        training and test datasets, generate cfg.TRAIN.NUM_COPY
        images with randomness from noise z and conditioning augmentation.'''
        algo.evaluate()
