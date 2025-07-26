import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Print TensorFlow version
print("TensorFlow version:", tf.__version__)

# Load the image from your PC
image_path = "/Users/lordunited/Downloads/hello.jpg"  # Replace with your image path
image = Image.open(image_path).convert('L')  # Convert to grayscale

# Convert the image to a numpy array
image_array = np.array(image)

# Convert to TensorFlow tensor
tensor_image = tf.convert_to_tensor(image_array, dtype=tf.float32)
print(f"Tensor shape: {tensor_image.shape}")

# Find black pixels using TensorFlow
# Define what we consider "black" (pixel values close to 0)
black_threshold = 50  # Pixels with value <= 50 are considered black

# Create a boolean mask for black pixels
black_pixels_mask = tensor_image <= black_threshold
black_pixels_count = tf.reduce_sum(tf.cast(black_pixels_mask, tf.int32))

# Find coordinates of black pixels
black_pixel_coords = tf.where(black_pixels_mask)
print (black_pixel_coords)
print(f"\nTensorFlow Black Pixel Analysis:")
print(f"Total pixels: {tf.size(tensor_image)}")
print(f"Black pixels (≤{black_threshold}): {black_pixels_count.numpy()}")
print(f"Percentage of black pixels: {(black_pixels_count / tf.size(tensor_image) * 100).numpy():.2f}%")

# Find the bounding box of black pixels using TensorFlow
if tf.greater(black_pixels_count, 0):
    try:
        # Get min and max coordinates of black pixels
        min_coords = tf.reduce_min(black_pixel_coords, axis=0)
        max_coords = tf.reduce_max(black_pixel_coords, axis=0)
        
        print(f"Black pixel bounding box:")
        print(f"  Top-left: ({min_coords[0].numpy()}, {min_coords[1].numpy()})")
        print(f"  Bottom-right: ({max_coords[0].numpy()}, {max_coords[1].numpy()})")
        
        # Crop the image to the black pixel bounding box
        cropped_image = image.crop((min_coords[1].numpy(), min_coords[0].numpy(), 
                                   max_coords[1].numpy() + 1, max_coords[0].numpy() + 1))
        
        # Display the images
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.imshow(image_array, cmap='gray')
        plt.title("Original Image")
        
        plt.subplot(1, 3, 2)
        # Show black pixels highlighted
        black_pixels_highlighted = image_array.copy()
        black_pixels_highlighted[black_pixels_mask.numpy()] = 255  # Make black pixels white for visibility
        plt.imshow(black_pixels_highlighted, cmap='gray')
        plt.title("Black Pixels Highlighted")
        
        plt.subplot(1, 3, 3)
        plt.imshow(cropped_image, cmap='gray')
        plt.title("Cropped to Black Content")
        plt.show()
        
        # Resize the cropped image for analysis
        resized_image = cropped_image.resize((100, 100))
        normalized_image = np.array(resized_image) / 255.0
        
        # Print image statistics
        print(f"\nImage Statistics:")
        print(f"Original image shape: {image_array.shape}")
        print(f"Cropped image shape: {np.array(cropped_image).shape}")
        print(f"Resized image shape: {normalized_image.shape}")
        print(f"Min pixel value: {normalized_image.min():.3f}")
        print(f"Max pixel value: {normalized_image.max():.3f}")
        print(f"Mean pixel value: {normalized_image.mean():.3f}")
        
    except Exception as e:
        print(f"Error processing black pixels: {e}")
        print(f"black_pixel_coords shape: {black_pixel_coords.shape}")
        print(f"black_pixels_count: {black_pixels_count.numpy()}")
else:
    print("No black pixels found in the image!")
    plt.imshow(image_array, cmap='gray')
    plt.title("Original Image (No Black Pixels Detected)")
    plt.show()

# Additional TensorFlow operations on the image
print(f"\nTensorFlow Operations:")
print(f"Image tensor shape: {tensor_image.shape}")
print(f"Image tensor dtype: {tensor_image.dtype}")
print(f"Min value in tensor: {tf.reduce_min(tensor_image).numpy()}")
print(f"Max value in tensor: {tf.reduce_max(tensor_image).numpy()}")
print(f"Mean value in tensor: {tf.reduce_mean(tensor_image).numpy():.2f}")
