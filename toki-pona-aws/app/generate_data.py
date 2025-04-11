import os
import random
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import numpy as np
from torchvision import transforms
import torch

def apply_random_background(image, size=(64, 64)):
    # Create background
    bg = Image.new('RGB', size, (random.randint(200, 255),) * 3)
    
    # Add some noise
    bg_array = np.array(bg)
    noise = np.random.randint(0, 30, bg_array.shape)
    bg_array = np.clip(bg_array + noise, 0, 255).astype(np.uint8)
    bg = Image.fromarray(bg_array)
    
    # Paste the original image
    bg.paste(image, mask=image.split()[3])  # Use alpha channel as mask
    return bg

def generate_augmented_samples(image_path, output_dir, num_samples=100):
    # Load image
    img = Image.open(image_path)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define transformations
    basic_transform = transforms.Compose([
        transforms.Resize((48, 48)),
        transforms.Pad(8, fill=255),  # Add padding for rotations
    ])
    
    # Apply basic transform
    img = basic_transform(img)
    
    for i in range(num_samples):
        # Start with a copy of the processed image
        aug_img = img.copy()
        
        # Random rotation (-15 to 15 degrees)
        angle = random.uniform(-15, 15)
        aug_img = aug_img.rotate(angle, Image.BICUBIC, expand=False)
        
        # Random scale (0.8 to 1.2)
        scale = random.uniform(0.8, 1.2)
        new_size = tuple(int(dim * scale) for dim in aug_img.size)
        aug_img = aug_img.resize(new_size, Image.BICUBIC)
        
        # Random translation
        translate = (random.randint(-5, 5), random.randint(-5, 5))
        aug_img = ImageOps.expand(aug_img, border=(0,0,0,0), fill=255)
        aug_img = aug_img.transform(aug_img.size, Image.AFFINE, (1, 0, translate[0], 0, 1, translate[1]))
        
        # Random brightness and contrast
        enhancer = ImageEnhance.Brightness(aug_img)
        aug_img = enhancer.enhance(random.uniform(0.8, 1.2))
        enhancer = ImageEnhance.Contrast(aug_img)
        aug_img = enhancer.enhance(random.uniform(0.8, 1.2))
        
        # Apply random background
        aug_img = apply_random_background(aug_img)
        
        # Save augmented image
        output_path = os.path.join(output_dir, f"{base_name}_{i:03d}.png")
        aug_img.save(output_path, "PNG")
        
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1} samples for {base_name}")

def main():
    # Source and destination directories
    src_dir = "img/sitelen_pona/png"
    output_dir = "data/augmented"
    
    # Process each PNG file
    for filename in os.listdir(src_dir):
        if filename.endswith('.png'):
            image_path = os.path.join(src_dir, filename)
            print(f"\nProcessing {filename}...")
            generate_augmented_samples(image_path, output_dir)

if __name__ == '__main__':
    main()
    print("\nData generation complete!")
