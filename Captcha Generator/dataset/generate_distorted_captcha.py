import os
import random
import csv
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw
import numpy as np
import scipy

# Parameters
output_dir = "captchas_distorted_test"
num_images = 50000
captcha_length = 5
characters = "0123456789"
csv_file = "captcha_labels.csv"  # CSV file to store labels

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(output_dir):
    print("Output directory does not exist. Something is wrong!")

# Initialize CAPTCHA generator
image_captcha = ImageCaptcha(width=200, height=80)

def add_noise(image):
    """Add random noise to the image."""
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for _ in range(random.randint(300, 500)):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = x1 + random.randint(1, 3), y1 + random.randint(1, 3)
        draw.rectangle([x1, y1, x2, y2], fill="black")
    return image

def add_distortion(image, amplitude = 6, frequency=0.025):
    width, height = image.size
    img_array = np.array(image)
    distorted_array = np.zeros_like(img_array)

    for y in range(height):
        offset = int(amplitude * np.sin(2*np.pi*frequency*y))
        distorted_array[y] = np.roll(img_array[y], offset, axis=0)

    return Image.fromarray(distorted_array)

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["filename", "label"])  # Write header

    # Generate Captchas
    for i in range(num_images):
        # Generate random CAPTCHA text (5 digits, allowing leading zeros)
        captcha_text = ''.join(random.choices(characters, k=captcha_length))
        
        # Generate CAPTCHA image
        image = image_captcha.generate_image(captcha_text)
       
        # Add distortion
        distorted_image = add_distortion(image)
        
        # Add noise
        noisy_image = add_noise(distorted_image)

        # Save CAPTCHA image
        image_path = os.path.join(output_dir, f"{captcha_text}.png")
        noisy_image.save(image_path)
        
        # Write the label as a string to the CSV
        writer.writerow([f"{captcha_text}.png", captcha_text])

        if i % 1000 == 0:
            print(f"Generated {i}/{num_images} images.")


print(f"CAPTCHA generation complete! Labels saved to {csv_file}.")
