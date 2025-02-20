import os
import random
import csv
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw

# Parameters
output_dir = "captchas_noise_dataset_two"
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
        
        # Add noise
        noisy_image = add_noise(image)
        
        # Save noisy CAPTCHA image
        image_path = os.path.join(output_dir, f"{i}.png")
        noisy_image.save(image_path)
        
        # Write the label as a string to the CSV
        writer.writerow([f"{i}.png", captcha_text])

        if i % 1000 == 0:
            print(f"Generated {i}/{num_images} images.")


print(f"CAPTCHA generation complete! Labels saved to {csv_file}.")
