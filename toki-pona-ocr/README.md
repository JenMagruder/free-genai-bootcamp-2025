# Toki Pona Learning Platform: Interactive Language Education

## Business Value Proposition

### Market Opportunity
- Growing interest in constructed languages and alternative writing systems
- Educational technology market valued at $342.4B (2025)
- Rising demand for interactive language learning tools
- Unique positioning in the Toki Pona community (~30,000 speakers)

### Key Features
1. **OCR Symbol Recognition**
   - Real-time sitelen pona recognition
   - High accuracy (85.27%) symbol detection
   - User-friendly drawing interface
   - Instant feedback system

2. **Interactive Text Adventure**
   - Gamified learning experience
   - Contextual vocabulary practice
   - Story-driven engagement
   - Progressive difficulty levels

3. **Sentence Constructor**
   - Hands-on grammar practice
   - Real-time syntax validation
   - Vocabulary reinforcement
   - Structured learning path

4. **Translation Services**
   - Real-time symbol recognition
   - Document digitization
   - Cross-script communication tools
   - Cultural exchange platforms

### Competitive Advantages
- Complete Toki Pona learning ecosystem
- Multiple learning modalities (visual, interactive, gamified)
- High-accuracy OCR capabilities
- Engaging text adventure system
- Practical sentence construction tools
- Real-time processing capability
- User-friendly Streamlit interface

### Growth Potential
1. **Market Expansion**
   - Integration with language learning apps
   - API services for developers
   - Custom enterprise solutions
   - Mobile application development
   - Expansion to other constructed languages

2. **Technology Enhancement**
   - Support for additional scripts
   - Advanced game narratives
   - Mobile-optimized interface
   - Cloud deployment options
   - Enhanced multiplayer features

### Implementation Timeline
- **Phase 1** Core OCR functionality
- **Phase 2** Web interface development
- **Phase 3** Performance optimization
- **Phase 4** Mobile deployment
- **Phase 5** Enterprise integration

## Toki Pona OCR Model

An Optical Character Recognition (OCR) model for Toki Pona sitelen pona script using Siamese Neural Networks and Streamlit.

## Overview

This project implements an OCR system that can recognize Toki Pona sitelen pona symbols. It uses a Siamese Neural Network architecture with ResNet34 backbone for feature extraction and similarity-based recognition.

## Supported Symbols

Currently, the model can recognize the following Toki Pona symbols:
- `ike` (bad, negative)
- `lili` (small, little)
- `ma` (land, earth, territory)
- `mi` (I, me, we)
- `moku` (food, eat)
- `ona` (he, she, it, they)
- `pona` (good, positive)
- `sina` (you)
- `suli` (big, important)
- `tawa` (to, for, moving)
- `tomo` (house, building, structure)

Each symbol has 100 augmented training images with various rotations, scales, and transformations.

## Technical Details

### Model Architecture
- **Backbone Network**: 
  - ResNet34 pretrained on ImageNet
  - Removed final avgpool and fc layers
  - Output channels: 512
  - Input image size: 224x224x3

- **Embedding Network**:
  - Layer 1: Linear(512 → 256) - Dimensionality reduction
  - Layer 2: Linear(256 → 512) - Feature expansion
  - Layer 3: BatchNorm1d(512) + ReLU
  - Layer 4: Linear(512 → 512) - Feature refinement
  - Layer 5: Linear(512 → 512) - Final embedding
  - Layer 6: BatchNorm1d(512) + ReLU
  - Output: L2-normalized 512-dimensional embeddings

### Architecture Diagrams

#### Model Architecture Overview
```
Input Image
    │
    ▼
┌─────────────┐
│  ResNet34   │ 
│  Backbone   │ ◄── Pretrained weights
└─────────────┘
    │ (512 channels)
    ▼
┌─────────────┐
│  Embedding  │
│  Network    │
└─────────────┘
    │ (512-dim)
    ▼
L2 Normalized
Embedding
```

#### Embedding Network Detail
```
512 channels
    │
    ▼
┌───────────┐
│ Linear    │──► 256
└───────────┘
    │
┌───────────┐
│ Linear    │──► 512
└───────────┘
    │
┌───────────┐
│ BatchNorm │
│ + ReLU    │──► 512
└───────────┘
    │
┌───────────┐
│ Linear    │──► 512
└───────────┘
    │
┌───────────┐
│ Linear    │──► 512
└───────────┘
    │
┌───────────┐
│ BatchNorm │
│ + ReLU    │──► 512
└───────────┘
```

#### Training Pipeline
```
Reference Symbol    Query Symbol
       │                │
       ▼                ▼
   ResNet34         ResNet34
       │                │
       ▼                ▼
   Embedding       Embedding
       │                │
       ▼                ▼
    L2 Norm         L2 Norm
       │                │
       └────┐      ┌────┘
            ▼      ▼
        Contrastive Loss
            │
            ▼
      Backpropagation
```

#### Inference Process
```
Database Symbols    Query Symbol
      │                │
      ▼                ▼
  Embeddings        ResNet34
  (Precomputed)         │
      │                 ▼
      │             Embedding
      │                 │
      │                 ▼
      │              L2 Norm
      │                 │
      └──────┐   ┌─────┘
             ▼   ▼
      Cosine Similarity
             │
             ▼
    Top-K Most Similar
         Symbols
```

### Training Details
- **Loss Function**: 
  - Contrastive Loss with margin=2.0
  - Pulls similar pairs closer, pushes dissimilar pairs apart
  - Distance metric: Euclidean distance

- **Optimizer**: 
  - Adam optimizer
  - Learning rate: 0.001
  - Beta1: 0.9, Beta2: 0.999

- **Training Process**:
  - Batch size: 32 pairs (16 positive, 16 negative)
  - Epochs: 100
  - Early stopping patience: 10
  - Validation split: 20%
  - Best validation accuracy: 85.27%

- **Data Augmentation Pipeline**:
  - Random rotation: ±15 degrees
  - Random scaling: 0.9 to 1.1
  - Random translation: ±10% of image size
  - Random brightness/contrast adjustment
  - Gaussian noise: σ=0.01
  - Normalization: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]

### Inference
- Input preprocessing matches training augmentation
- Cosine similarity used for symbol matching
- Confidence threshold: 0.75
- Real-time inference (~100ms on CPU)

### Performance Metrics
- Training time on Colab GPU: ~2 hours
- Model size: 21.3MB
- Average inference time:
  - CPU (Intel i5): 102ms
  - Google Colab GPU: 23ms
- Memory usage: ~200MB during inference

## Development Challenges

1. **CPU Performance Issues**
   - Initial training on local CPU was very slow
   - CPU overheating during extended training sessions
   - Solved by moving training to Google Colab's free GPU

2. **Model Architecture Evolution**
   - Initially used Feature Pyramid Network (FPN)
   - Removed FPN due to compatibility issues with state dictionary
   - Simplified to direct ResNet34 features for better maintainability

3. **Symbol Recognition Challenges**
   - Some symbols (e.g., "ala") were misclassified
   - Identified missing symbols in training data
   - Need to expand dataset with more symbols

## Setup and Usage

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit App**
```bash
streamlit run app/main.py
```

3. **Using the OCR**
- Launch the Streamlit app
- Draw or upload a Toki Pona symbol
- The model will predict the most similar symbol from its training set

## Future Improvements

1. **Dataset Expansion**
   - Add missing symbols (e.g., `ala`, `jan`, `li`, `o`)
   - Increase training examples per symbol
   - Improve data augmentation techniques

2. **Model Enhancements**
   - Experiment with different backbones (e.g., EfficientNet)
   - Implement attention mechanisms
   - Try triplet loss instead of contrastive loss

3. **Performance Optimization**
   - Implement model quantization
   - Cache intermediate features
   - Add progressive resizing

## Contributing

Feel free to contribute by:
1. Adding new symbols to the training data
2. Improving model architecture
3. Enhancing the Streamlit interface
4. Fixing bugs and issues

## License

This project is open source and available under the MIT License.
