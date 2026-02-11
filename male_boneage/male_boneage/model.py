import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import vit_b_16


class CoordAttention(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.conv = nn.Conv2d(c, c, kernel_size=1)

    def forward(self, x):
        return x * torch.sigmoid(self.conv(self.pool(x)))


class BoneAgeModel(nn.Module):
    def __init__(self):
        super().__init__()

        # ---- CNN backbone (ResNet18) ----
        cnn = models.resnet18(pretrained=True)
        cnn.conv1 = nn.Conv2d(1, 64, 7, 2, 3, bias=False)
        self.cnn = nn.Sequential(*list(cnn.children())[:-2])

        self.ca = CoordAttention(512)
        self.pool = nn.AdaptiveAvgPool2d(1)

        # ---- ViT backbone ----
        self.vit = vit_b_16(pretrained=True)
        self.vit.heads = nn.Identity()

        # ---- Fusion ----
        self.fc = nn.Linear(512 + 768, 256)

        # ---- HEAD NAMES (DO NOT CHANGE) ----
        self.grp = nn.Linear(256, 4)
        self.unc = nn.Linear(256, 2)

    def forward(self, x):
        c = self.pool(self.ca(self.cnn(x))).flatten(1)
        v = self.vit(x.repeat(1, 3, 1, 1))
        f = self.fc(torch.cat([c, v], dim=1))
        return self.grp(f), self.unc(f)
