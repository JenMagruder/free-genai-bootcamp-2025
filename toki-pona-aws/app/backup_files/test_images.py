import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def display_images():
    # Directory containing PNGs
    png_dir = "img/sitelen_pona/png"
    
    # Get all PNG files
    png_files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
    
    # Calculate grid size
    n = len(png_files)
    cols = 4
    rows = (n + cols - 1) // cols
    
    # Create figure
    plt.figure(figsize=(12, 3 * rows))
    
    # Display each image
    for i, png_file in enumerate(sorted(png_files)):
        img_path = os.path.join(png_dir, png_file)
        img = Image.open(img_path)
        
        plt.subplot(rows, cols, i + 1)
        plt.imshow(np.array(img), cmap='gray')
        plt.title(png_file.replace('.png', ''))
        plt.axis('off')
    
    plt.tight_layout()
    
    # Save the plot instead of displaying it
    output_dir = "img/preview"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "symbols_preview.png"))
    print("✓ Saved preview to img/preview/symbols_preview.png")

if __name__ == "__main__":
    display_images()
