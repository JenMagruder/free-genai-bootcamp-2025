import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import random
import torchvision.models as models
from torchvision.models import ResNet34_Weights

class SiameseNet(nn.Module):
    def __init__(self, embedding_dim=512):
        super().__init__()
        
        # Use ResNet34 as backbone
        resnet = models.resnet34(weights=ResNet34_Weights.DEFAULT)
        modules = list(resnet.children())[:-2]  # Remove avgpool and fc
        self.backbone = nn.Sequential(*modules)
        
        # Embedding network
        self.embedding = nn.Sequential(
            nn.Linear(512, 256),  # First layer reduces to 256
            nn.Linear(256, 512),  # Second layer expands to 512
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 512),  # Third layer maintains 512
            nn.Linear(512, 512),  # Fourth layer maintains 512
            nn.BatchNorm1d(512),
            nn.ReLU()
        )
        
    def forward(self, x):
        # Extract features
        x = self.backbone(x)
        
        # Global average pooling
        x = F.adaptive_avg_pool2d(x, 1)
        x = x.view(x.size(0), -1)
        
        # Embedding
        x = self.embedding(x)
        
        return F.normalize(x, p=2, dim=1)

class TripletLoss(nn.Module):
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin
        
    def forward(self, anchor, positive, negative):
        distance_positive = (anchor - positive).pow(2).sum(1)
        distance_negative = (anchor - negative).pow(2).sum(1)
        losses = F.relu(distance_positive - distance_negative + self.margin)
        return losses.mean()

class CombinedLoss(nn.Module):
    def __init__(self, contrastive_margin=2.0, triplet_margin=1.0, alpha=0.5):
        super().__init__()
        self.contrastive = ContrastiveLoss(margin=contrastive_margin)
        self.triplet = TripletLoss(margin=triplet_margin)
        self.alpha = alpha
    
    def forward(self, output1, output2, label, negative=None):
        contrastive_loss = self.contrastive(output1, output2, label)
        if negative is not None:
            triplet_loss = self.triplet(output1, output2, negative)
            return self.alpha * contrastive_loss + (1 - self.alpha) * triplet_loss
        return contrastive_loss

class ContrastiveLoss(nn.Module):
    def __init__(self, margin=2.0, hard_mining=True):
        super().__init__()
        self.margin = margin
        self.hard_mining = hard_mining
    
    def forward(self, embeddings1, embeddings2, labels):
        distances = F.pairwise_distance(embeddings1, embeddings2)
        losses = labels.float() * distances.pow(2) + (1 - labels.float()) * F.relu(self.margin - distances).pow(2)
        return losses.mean()

class TokiPonaDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        self.class_to_idx = {}
        self.idx_to_class = {}
        
        # Load dataset
        self._load_dataset()
        
        # Create reverse mapping
        self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}
    
    def _load_dataset(self):
        import os
        from PIL import Image
        
        # Collect all valid image files
        for item in os.listdir(self.data_dir):
            if item.endswith('.png'):
                class_name = item.split('_')[0]
                
                # Add class if not seen before
                if class_name not in self.class_to_idx:
                    self.class_to_idx[class_name] = len(self.class_to_idx)
                
                # Try to load image
                try:
                    img_path = os.path.join(self.data_dir, item)
                    img = Image.open(img_path).convert('RGB')
                    
                    # Only add if image is valid
                    self.images.append(img_path)
                    self.labels.append(self.class_to_idx[class_name])
                except:
                    print(f"Warning: Could not load {item}")
    
    def get_pair(self, index):
        """Get a pair of images and their similarity label"""
        img1_path = self.images[index]
        img1_label = self.labels[index]
        
        # 50% chance of getting same class (positive pair)
        if torch.rand(1) > 0.5:
            # Find all indices of the same class
            same_class_indices = [i for i, label in enumerate(self.labels) if label == img1_label and i != index]
            if same_class_indices:
                img2_idx = same_class_indices[torch.randint(len(same_class_indices), (1,)).item()]
                label = 1
            else:
                # Fallback to different class if no other images of same class
                diff_class_indices = [i for i, label in enumerate(self.labels) if label != img1_label]
                img2_idx = diff_class_indices[torch.randint(len(diff_class_indices), (1,)).item()]
                label = 0
        else:
            # Get image from different class (negative pair)
            diff_class_indices = [i for i, label in enumerate(self.labels) if label != img1_label]
            img2_idx = diff_class_indices[torch.randint(len(diff_class_indices), (1,)).item()]
            label = 0
        
        # Load images
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(self.images[img2_idx]).convert('RGB')
        
        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)
        
        return img1, img2, label
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, index):
        img_path = self.images[index]
        label = self.labels[index]
        
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        
        return img, label

def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=100, device='cpu', scheduler=None, early_stopping_patience=10):
    best_val_loss = float('inf')
    best_model_state = None
    epochs_without_improvement = 0
    
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for batch_idx, (img1, img2, labels) in enumerate(train_loader):
            img1, img2, labels = img1.to(device), img2.to(device), labels.to(device)
            
            optimizer.zero_grad()
            output1, output2 = model(img1), model(img2)
            loss = criterion(output1, output2, labels)
            loss.backward()
            optimizer.step()
            
            # Calculate accuracy
            distances = F.pairwise_distance(output1, output2)
            predictions = (distances < criterion.margin / 2).float()
            train_correct += (predictions == labels).sum().item()
            train_total += labels.size(0)
            train_loss += loss.item()
        
        # Validation phase
        model.eval()
        val_loss = 0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for img1, img2, labels in val_loader:
                img1, img2, labels = img1.to(device), img2.to(device), labels.to(device)
                output1, output2 = model(img1), model(img2)
                loss = criterion(output1, output2, labels)
                
                # Calculate accuracy
                distances = F.pairwise_distance(output1, output2)
                predictions = (distances < criterion.margin / 2).float()
                val_correct += (predictions == labels).sum().item()
                val_total += labels.size(0)
                val_loss += loss.item()
        
        # Calculate average metrics
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        train_accuracy = 100 * train_correct / train_total
        val_accuracy = 100 * val_correct / val_total
        
        print(f"Epoch [{epoch+1}/{num_epochs}]:")
        print(f"  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.2f}%")
        print(f"  Val Loss: {avg_val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")
        
        # Learning rate scheduling
        if scheduler is not None:
            if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                scheduler.step(avg_val_loss)
            else:
                scheduler.step()
        
        # Save best model
        if avg_val_loss < best_val_loss:
            print("  New best validation loss! Model saved.")
            best_val_loss = avg_val_loss
            best_model_state = model.state_dict().copy()
            epochs_without_improvement = 0
            torch.save(model.state_dict(), 'best_model.pth')
        else:
            epochs_without_improvement += 1
            
        # Early stopping
        if epochs_without_improvement >= early_stopping_patience:
            print(f"\nEarly stopping triggered after {epoch+1} epochs")
            break
    
    # Load best model
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    return model