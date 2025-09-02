import os
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import torch
from torchvision import transforms

# mapping folder ke multi-label vektor
LABEL_MAP = {
    "all_closed":       [0,0,0,0,0],
    "front_left_open":  [1,0,0,0,0],
    "front_right_open": [0,1,0,0,0],
    "rear_left_open":   [0,0,1,0,0],
    "rear_right_open":  [0,0,0,1,0],
    "hood_open":        [0,0,0,0,1],
}

class CarDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        root_dir: path ke folder split (train/val/test)
        """
        self.root_dir = root_dir
        self.transform = transform

        self.samples = []
        for folder, label in LABEL_MAP.items():
            class_dir = os.path.join(root_dir, folder)
            if not os.path.isdir(class_dir):
                continue
            for fname in os.listdir(class_dir):
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    fpath = os.path.join(class_dir, fname)
                    self.samples.append((fpath, torch.tensor(label, dtype=torch.float32)))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        fpath, label = self.samples[idx]
        image = Image.open(fpath).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label