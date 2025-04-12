import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from ocr_model import SiameseNet, TokiPonaDataset
import numpy as np

class TokiPonaClassifier:
    def __init__(self, model_path='models/toki_pona_ocr.pth', device=None):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
        
        # Load support set (training examples)
        self.support_dataset = TokiPonaDataset(
            "img/sitelen_pona/augmented",
            transform=transforms.Compose([
                transforms.Resize((64, 64)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
        )
        
        # Create prototype embeddings for each class
        self.model = SiameseNet().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        
        self.class_prototypes = {}
        self.class_to_idx = self.support_dataset.class_to_idx
        self.idx_to_class = self.support_dataset.idx_to_class
        
        # Calculate prototypes
        self._calculate_prototypes()
        
        # Transform for new images
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def _calculate_prototypes(self):
        """Calculate mean embeddings for each class"""
        class_embeddings = {cls: [] for cls in self.class_to_idx.keys()}
        
        with torch.no_grad():
            for img, label in self.support_dataset:
                img = img.unsqueeze(0).to(self.device)
                embedding = self.model(img)
                class_name = self.idx_to_class[label]
                class_embeddings[class_name].append(embedding.cpu())
        
        # Calculate mean embeddings
        for cls in class_embeddings:
            if class_embeddings[cls]:
                embeddings = torch.cat(class_embeddings[cls], dim=0)
                self.class_prototypes[cls] = torch.mean(embeddings, dim=0)
    
    def predict(self, image, k=3):
        """Predict top-k classes for an image"""
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        
        # Prepare image
        if self.transform:
            image = self.transform(image)
        image = image.unsqueeze(0).to(self.device)
        
        # Get embedding
        self.model.eval()
        with torch.no_grad():
            embedding = self.model(image)
        
        # Calculate distances to all prototypes
        distances = {}
        for cls, prototype in self.class_prototypes.items():
            prototype = prototype.to(self.device)
            distance = F.pairwise_distance(embedding, prototype.unsqueeze(0))
            distances[cls] = distance.item()
        
        # Sort by distance (closest first)
        sorted_predictions = sorted(distances.items(), key=lambda x: x[1])
        
        # Convert distances to probabilities using softmax
        distances = torch.tensor([d for _, d in sorted_predictions])
        probabilities = F.softmax(-distances, dim=0)  # Negative distances for correct probability order
        
        # Return top-k predictions with probabilities
        results = []
        for i in range(min(k, len(sorted_predictions))):
            class_name = sorted_predictions[i][0]
            prob = probabilities[i].item()
            results.append((class_name, prob))
        
        return results

def main():
    # Example usage
    classifier = TokiPonaClassifier()
    
    # Test on a few images
    test_images = [
        "img/sitelen_pona/png/ike.png",
        "img/sitelen_pona/png/pona.png",
        "img/sitelen_pona/png/tawa.png"
    ]
    
    for img_path in test_images:
        predictions = classifier.predict(img_path)
        print(f"\nPredictions for {img_path}:")
        for class_name, prob in predictions:
            print(f"  {class_name}: {prob:.2%}")

if __name__ == "__main__":
    main()