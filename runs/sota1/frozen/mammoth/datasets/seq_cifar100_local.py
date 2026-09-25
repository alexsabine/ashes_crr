# SOTA1 addition (not upstream Mammoth): Split-CIFAR-100 read from a local, sha256-verified .npz file, so that no
# download can happen before the pre-registration hash; the same class also reads the synthetic surrogate streams.
# Keys: x_train (N,32,32,3) uint8, y_train (N,), x_test, y_test. Path from the environment variable CRR_CIFAR100_NPZ.
import os
from typing import Tuple

import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

from datasets.seq_cifar100 import SequentialCIFAR100
from datasets.utils.continual_dataset import store_masked_loaders


class NPZImages(torch.utils.data.Dataset):
    def __init__(self, data, targets, train, transform=None, target_transform=None):
        self.data = data
        self.targets = np.asarray(targets, dtype=np.int64)
        self.train = train
        self.transform = transform
        self.target_transform = target_transform
        self.not_aug_transform = transforms.Compose([transforms.ToTensor()])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        img, target = self.data[index], int(self.targets[index])
        img = Image.fromarray(img, mode='RGB')
        if not self.train:
            if self.transform is not None:
                img = self.transform(img)
            return img, target
        original_img = img.copy()
        not_aug_img = self.not_aug_transform(original_img)
        if self.transform is not None:
            img = self.transform(img)
        if hasattr(self, 'logits'):
            return img, target, not_aug_img, self.logits[index]
        return img, target, not_aug_img


class SequentialCIFAR100Local(SequentialCIFAR100):
    NAME = 'seq-cifar100-local'

    def get_data_loaders(self) -> Tuple[torch.utils.data.DataLoader, torch.utils.data.DataLoader]:
        z = np.load(os.environ['CRR_CIFAR100_NPZ'])
        test_transform = transforms.Compose([transforms.ToTensor(), self.get_normalization_transform()])
        train_dataset = NPZImages(z['x_train'], z['y_train'], True, transform=self.TRANSFORM)
        test_dataset = NPZImages(z['x_test'], z['y_test'], False, transform=test_transform)
        return store_masked_loaders(train_dataset, test_dataset, self)

    def get_class_names(self):
        if self.class_names is None:
            self.class_names = [f'class_{i}' for i in range(self.N_CLASSES)]
        return self.class_names
