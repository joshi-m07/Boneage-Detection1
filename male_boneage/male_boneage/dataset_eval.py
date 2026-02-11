import pandas as pd
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

eval_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])


class BoneAgeEvalDataset(Dataset):
    def __init__(self, csv_path, img_dir):
        self.df = pd.read_csv(csv_path)
        self.df["id"] = self.df["id"].astype(str)
        self.img_dir = img_dir

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img = Image.open(f"{self.img_dir}/{row.id}.png").convert("L")
        img = eval_tf(img)
        return img, row.age_group, row.boneage
