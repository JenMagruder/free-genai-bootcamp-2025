import streamlit as st
import torch
from PIL import Image
import torchvision.transforms as transforms
from ocr_model import SiameseNet
import os

# Update model path to use absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'toki_pona_ocr_model_85acc.pth')
DATA_DIR = os.path.join(BASE_DIR, 'data', 'augmented')

def load_model(model_path):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    checkpoint = torch.load(model_path, map_location=device)
    model = SiameseNet()
    
    # Convert state dict keys to match the new model
    state_dict = checkpoint['model_state_dict']
    new_state_dict = {}
    
    for k, v in state_dict.items():
        if k.startswith('backbone.'):
            # Extract the layer number and rest of the path
            parts = k.split('.')
            if len(parts) > 2 and parts[1].isdigit():
                layer_num = int(parts[1])
                if layer_num <= 3:  # First 4 layers map directly
                    new_state_dict[k] = v
                else:  # Adjust layer numbers for the rest
                    new_key = f"backbone.{layer_num-4}.{'.'.join(parts[2:])}"
                    new_state_dict[new_key] = v
            else:
                new_state_dict[k] = v
        else:
            new_state_dict[k] = v
    
    # Load the converted state dict
    model.load_state_dict(new_state_dict, strict=False)
    model.to(device)
    model.eval()
    return model, checkpoint['normalize_params'], checkpoint['val_accuracy'], device

def process_image(image, transform):
    return transform(image).unsqueeze(0)

def get_symbol_database():
    symbols = {}
    if os.path.exists(DATA_DIR):
        for file in os.listdir(DATA_DIR):
            if file.endswith('.png'):
                symbol_name = file.split('_')[0]  # Get symbol name before underscore
                if symbol_name not in symbols:
                    symbols[symbol_name] = os.path.join(DATA_DIR, file)
    else:
        st.error(f"Data directory not found: {DATA_DIR}")
    return symbols

def main():
    st.title("Toki Pona OCR Practice")
    st.markdown("""
    Upload an image containing a Toki Pona symbol to recognize it.
    The model will compare it with known symbols and find the closest match.
    Model Accuracy: 85.27% (validation)
    """)

    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model file not found: {MODEL_PATH}")
        st.info("Please ensure the model file is in the correct location.")
        return

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Display uploaded image
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption='Uploaded Image', width=200)
            
            # Add predict button
            if st.button('Recognize Symbol'):
                with st.spinner('Processing...'):
                    # Load model
                    model, normalize_params, val_accuracy, device = load_model(MODEL_PATH)
                    
                    # Prepare transforms
                    transform = transforms.Compose([
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                        transforms.Normalize(
                            mean=normalize_params['mean'],
                            std=normalize_params['std']
                        )
                    ])
                    
                    # Process uploaded image
                    input_tensor = process_image(image, transform).to(device)
                    
                    # Load and compare with reference symbols
                    symbols = get_symbol_database()
                    if not symbols:
                        st.error("No reference symbols found in the database.")
                        return
                        
                    best_match = None
                    lowest_distance = float('inf')
                    
                    for symbol_name, symbol_path in symbols.items():
                        ref_image = Image.open(symbol_path).convert('RGB')
                        ref_tensor = process_image(ref_image, transform).to(device)
                        
                        with torch.no_grad():
                            input_embedding = model(input_tensor)
                            ref_embedding = model(ref_tensor)
                            distance = torch.nn.functional.pairwise_distance(
                                input_embedding, ref_embedding
                            ).item()
                            
                            if distance < lowest_distance:
                                lowest_distance = distance
                                best_match = symbol_name
                    
                    if best_match:
                        st.success(f"Recognized symbol: {best_match}")
                        st.info(f"Confidence: {1.0 / (1.0 + lowest_distance):.2%}")
                    else:
                        st.error("Could not recognize the symbol.")
                        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            raise e

if __name__ == "__main__":
    main()
