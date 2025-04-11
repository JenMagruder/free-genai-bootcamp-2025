import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from ocr_model import TokiPonaDataset
import os

def show_batch(images, labels, class_names):
    plt.figure(figsize=(12, 6))
    for i in range(min(16, len(images))):
        plt.subplot(4, 4, i + 1)
        img = images[i].numpy().transpose((1, 2, 0))
        # Denormalize
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img = std * img + mean
        img = np.clip(img, 0, 1)
        plt.imshow(img)
        plt.title(f'Class: {class_names[labels[i]]}')
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('dataset_samples.png')
    plt.close()

def analyze_dataset():
    # Data transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Load datasets
    train_dataset = TokiPonaDataset("img/sitelen_pona/augmented", transform=transform, val_split=0.2, is_val=False)
    val_dataset = TokiPonaDataset("img/sitelen_pona/augmented", transform=transform, val_split=0.2, is_val=True)
    
    # Get class names
    class_names = list(train_dataset.class_to_idx.keys())
    
    # Analyze training set
    print("\nTraining Set Analysis:")
    print(f"Number of samples: {len(train_dataset)}")
    
    # Count samples per class
    train_counts = {}
    for _, label in train_dataset:
        class_name = class_names[label]
        train_counts[class_name] = train_counts.get(class_name, 0) + 1
    
    print("\nSamples per class (Training):")
    for class_name, count in sorted(train_counts.items()):
        print(f"  {class_name}: {count}")
    
    # Analyze validation set
    print("\nValidation Set Analysis:")
    print(f"Number of samples: {len(val_dataset)}")
    
    val_counts = {}
    for _, label in val_dataset:
        class_name = class_names[label]
        val_counts[class_name] = val_counts.get(class_name, 0) + 1
    
    print("\nSamples per class (Validation):")
    for class_name, count in sorted(val_counts.items()):
        print(f"  {class_name}: {count}")
    
    # Visualize some training samples
    print("\nSaving sample images to dataset_samples.png...")
    images = []
    labels = []
    seen_classes = set()
    
    for image, label in train_dataset:
        class_name = class_names[label]
        if class_name not in seen_classes:
            images.append(image)
            labels.append(label)
            seen_classes.add(class_name)
        if len(seen_classes) == len(class_names):
            break
    
    show_batch(images, labels, class_names)
    print("Done! Check dataset_samples.png to verify the images and labels.")

if __name__ == "__main__":
    analyze_dataset()
