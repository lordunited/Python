from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "/Users/lordunited/Downloads/hello.jpg"  # Replace with your image path
image = Image.open(image_path).convert('L')  # Convert to grayscale

# Convert the image to a numpy array
image_array = np.array(image)

# Find the bounding box of non-zero pixels
non_zero_coords = np.argwhere(image_array > 0)  # Find non-zero pixel coordinates
top_left = non_zero_coords.min(axis=0)  # Top-left corner of the bounding box
bottom_right = non_zero_coords.max(axis=0)  # Bottom-right corner of the bounding box
print(f"Top-left: {top_left}, Bottom-right: {bottom_right}")
# Crop the image to the bounding box
cropped_image = image.crop((top_left[1], top_left[0], bottom_right[1] + 1, bottom_right[0] + 1))

# Display the cropped image
plt.imshow(cropped_image, cmap='gray')
plt.title("Cropped Image")
plt.show()
