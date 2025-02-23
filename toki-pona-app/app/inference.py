import torch
from PIL import Image
from ocr_model import TokiPonaOCR
import torchvision.transforms as transforms

def load_model(model_path):
    model = TokiPonaOCR(num_classes=YOUR_NUM_CLASSES)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def process_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    image = Image.open(image_path).convert('L')
    return transform(image).unsqueeze(0)

def predict_character(model, image_path):
    image = process_image(image_path)
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        return predicted.item()