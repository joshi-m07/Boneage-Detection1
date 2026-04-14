import torch
from torchvision import transforms
import random


class BoneAgeAugmentation:
    """On-the-fly augmentation for bone age X-ray images"""
    
    def __init__(self, apply_augmentation=True):
        self.apply_augmentation = apply_augmentation
        
        # Base preprocessing (always applied)
        self.base_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])
        
        # Augmentation transforms
        self.augment_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomRotation(degrees=10),
            transforms.RandomAffine(degrees=0, translate=(0.05, 0.05), scale=(0.95, 1.05)),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])
    
    def __call__(self, image):
        """Apply augmentation to PIL Image"""
        if self.apply_augmentation and random.random() > 0.5:
            return self.augment_transform(image)
        else:
            return self.base_transform(image)
    
    def get_base_transform(self):
        """Get base transform without augmentation"""
        return self.base_transform


# Preprocessing transform (no augmentation for inference)
eval_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])
