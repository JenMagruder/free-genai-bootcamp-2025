import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from ocr_model import SiameseNet, ContrastiveLoss, TokiPonaDataset, train_model
import math

class PairDataset:
    def __init__(self, dataset):
        self.dataset = dataset
    
    def __getitem__(self, index):
        return self.dataset.get_pair(index)
    
    def __len__(self):
        return len(self.dataset)

if __name__ == "__main__":
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # More balanced data augmentation
    train_transform = transforms.Compose([
        transforms.Resize((64, 64)),  # Back to original size
        transforms.RandomApply([
            transforms.RandomAffine(
                degrees=15,  # Reduced rotation
                translate=(0.1, 0.1),  # Less translation
                scale=(0.9, 1.1),  # Less scaling
                shear=10
            )
        ], p=0.5),
        transforms.RandomApply([
            transforms.ColorJitter(
                brightness=0.2,
                contrast=0.2,
                saturation=0.1,
                hue=0.05
            )
        ], p=0.3),
        transforms.RandomHorizontalFlip(p=0.3),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create base datasets
    full_dataset = TokiPonaDataset("img/sitelen_pona/augmented", transform=None)
    
    # Split with fixed seed for reproducibility
    torch.manual_seed(42)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size]
    )
    
    # Add transforms
    train_dataset.dataset.transform = train_transform
    val_dataset.dataset.transform = val_transform
    
    # Create pair datasets
    train_pairs = PairDataset(train_dataset.dataset)
    val_pairs = PairDataset(val_dataset.dataset)
    
    # Training parameters
    num_epochs = 50  # Reduced from 150
    batch_size = 16  # Reduced from 32
    learning_rate = 0.001
    early_stopping_patience = 10

    # Create data loaders with smaller batch size
    train_loader = DataLoader(
        train_pairs,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_pairs,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True
    )
    
    print(f"Training pairs: {len(train_pairs)}")
    print(f"Validation pairs: {len(val_pairs)}")
    
    # Initialize model and move to device
    model = SiameseNet()
    model = model.to(device)
    
    # Contrastive loss with smaller margin
    criterion = ContrastiveLoss(margin=1.0, hard_mining=True)
    
    # Optimizer with simpler learning rate schedule
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
    
    print("\nStarting training...")
    model = train_model(
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        num_epochs=num_epochs,
        device=device,
        scheduler=scheduler,
        early_stopping_patience=early_stopping_patience
    )
    
    # Save the final model
    print("\nSaving final model...")
    torch.save(model.state_dict(), 'models/toki_pona_ocr.pth')
    print("Model saved to models/toki_pona_ocr.pth")