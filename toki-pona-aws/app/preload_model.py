import logging
import os
from huggingface_hub import snapshot_download

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_model():
    """
    Downloads the Toki Pona OCR model from the Hugging Face Hub if it doesn't already exist locally.
    This model is specifically trained to recognize sitelen pona symbols.
    """
    model_dir = "/models/toki-pona-ocr"
    temp_model_dir = "/models/manga-ocr"  # Temporary fallback since toki pona model is hypothetical

    if not os.path.exists(model_dir):
        try:
            logging.info("Attempting to download Toki Pona OCR model...")
            # Note: This is a hypothetical model ID - would need to be replaced with actual model
            snapshot_download(
                repo_id="toki-pona/sitelen-pona-ocr-base",
                local_dir=model_dir,
                ignore_patterns=[".*", "*.md"]
            )
            logging.info("Toki Pona OCR model downloaded successfully")
        except Exception as e:
            logging.warning(f"Could not download Toki Pona model: {e}")
            logging.info("Falling back to manga-ocr model as temporary solution...")
            
            if not os.path.exists(temp_model_dir):
                snapshot_download(
                    repo_id="TareHimself/manga-ocr-base",
                    local_dir=temp_model_dir,
                    ignore_patterns=[".*", "*.md"]
                )
                logging.info("Manga OCR model downloaded as temporary fallback")
            else:
                logging.info("Fallback model already exists")
    else:
        logging.info("Toki Pona OCR model already exists. Skipping download.")

def verify_model():
    """
    Verifies that the model files exist and have the expected structure.
    """
    required_files = [
        "config.json",
        "pytorch_model.bin",
        "tokenizer.json"
    ]
    
    model_dir = "/models/toki-pona-ocr"
    temp_model_dir = "/models/manga-ocr"
    
    # Check primary model directory
    if os.path.exists(model_dir):
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(model_dir, f))]
        if missing_files:
            logging.warning(f"Missing files in Toki Pona model: {missing_files}")
            return False
        return True
    
    # Check fallback model directory
    if os.path.exists(temp_model_dir):
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(temp_model_dir, f))]
        if missing_files:
            logging.warning(f"Missing files in fallback model: {missing_files}")
            return False
        return True
    
    logging.error("No model directory found")
    return False

if __name__ == "__main__":
    download_model()
    if verify_model():
        logging.info("Model verification successful")
    else:
        logging.error("Model verification failed")