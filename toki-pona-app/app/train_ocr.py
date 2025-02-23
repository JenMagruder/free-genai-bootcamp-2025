from ocr_model import TokiPonaDataset, TokiPonaOCR
import torch
import torchvision.transforms as transforms

# Set up data transforms
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Create datasets
train_dataset = TokiPonaDataset('data/train', transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Initialize model
model = TokiPonaOCR(num_classes=len(train_dataset.classes))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
train_model(model, train_loader, criterion, optimizer, num_epochs=10)

# Save the model
torch.save(model.state_dict(), 'toki_pona_ocr.pth')