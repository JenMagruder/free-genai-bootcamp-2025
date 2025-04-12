import torch
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'models', 'toki_pona_ocr_model_85acc.pth')
checkpoint = torch.load(model_path, map_location='cpu')

print("Model state dict keys:")
for key in checkpoint['model_state_dict'].keys():
    print(f"{key}: {checkpoint['model_state_dict'][key].shape}")

print("\nModel metadata:")
for key in checkpoint.keys():
    if key != 'model_state_dict':
        print(f"{key}: {checkpoint[key]}")
