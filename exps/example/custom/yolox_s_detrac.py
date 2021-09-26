#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.
import os

from yolox.exp import Exp as MyExp


class Exp(MyExp):
    def __init__(self):
        super(Exp, self).__init__()
        self.depth = 0.33
        self.width = 0.50
        self.exp_name = os.path.split(os.path.realpath(__file__))[1].split(".")[0]

        # Define yourself dataset path
        self.data_dir = "datasets/UA-DETRAC"
        self.train_ann = "train10.json"
        self.val_ann = "val10.json"

        self.num_classes = 4

        self.max_epoch = 300
        self.data_num_workers = 16
        self.eval_interval = 1
