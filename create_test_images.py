# create_test_images.py
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def create_professional_product():
    """Create a professional-looking product image."""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a clean product (like a shoe or watch)
    draw.rectangle([250, 150, 550, 450], fill='lightblue', outline='darkblue', width=3)
    draw.ellipse([350, 250, 450, 350], fill='white', outline='darkblue', width=2)
    
    # Add subtle shadow
    draw.rectangle([255, 455, 545, 460], fill='lightgray')
    
    # Save
    if not os.path.exists('samples'):
        os.makedirs('samples')
    img.save('samples/professional_product.jpg')
    print("Created: samples/professional_product.jpg")

def create_blurry_image():
    """Create a blurry version of an image."""
    # Create a sharp image first
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([200, 200, 600, 400], fill='red', outline='black', width=3)
    
    # Convert to numpy and blur
    img_np = np.array(img)
    blurred = cv2.GaussianBlur(img_np, (51, 51), 0)
    
    # Save
    blur_img = Image.fromarray(blurred)
    blur_img.save('samples/blurry_test.jpg')
    print("Created: samples/blurry_test.jpg")

def create_cluttered_image():
    """Create an image with many objects."""
    img = Image.new('RGB', (800, 600), color='lightyellow')
    draw = ImageDraw.Draw(img)
    
    # Draw multiple random objects
    objects = [
        ((100, 100, 200, 200), 'blue'),    # Object 1
        ((300, 150, 400, 250), 'green'),   # Object 2
        ((500, 100, 600, 200), 'red'),     # Object 3
        ((150, 350, 250, 450), 'orange'),  # Object 4
        ((400, 350, 500, 450), 'purple'),  # Object 5
    ]
    
    for (x1, y1, x2, y2), color in objects:
        draw.rectangle([x1, y1, x2, y2], fill=color, outline='black', width=2)
    
    # Add some text
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 500), "My random stuff collection", fill='black', font=font)
    
    img.save('samples/cluttered_image.jpg')
    print("Created: samples/cluttered_image.jpg")

if __name__ == "__main__":
    print("Creating test images...")
    create_professional_product()
    create_blurry_image()
    create_cluttered_image()
    print("\nTest images created in 'samples' folder!")