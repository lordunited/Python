import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

image_path = "/Users/lordunited/Downloads/hello.jpg" 

####Find the number of white Pixels 
def find_white_pixels(image_path, colour):
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)
    colour_pixel_number = colour
    colour_mask = image_tensor <= colour_pixel_number
    colour_pixel_count = tf.reduce_sum(tf.cast(colour_mask, tf.int32))
    colour_pixel_coords = tf.where(image_tensor <= colour_pixel_number)

    return image_array, colour_mask, colour_pixel_count, colour_pixel_coords, image_tensor

def crop_image(image, min_coords, max_coords):
    # Crop the image to the black pixel bounding box
    cropped_image = image.crop((min_coords[1].numpy(), min_coords[0].numpy(), 
                                max_coords[1].numpy() + 1, max_coords[0].numpy() + 1))
    return cropped_image

# Get the results from the function
white_result = find_white_pixels(image_path, 200)

if tf.greater(white_result[2], 0):  # Check if there are white pixels
    try:
        # Get min and max coordinates of white pixels
        min_coords = tf.reduce_min(white_result[3], axis=0)
        max_coords = tf.reduce_max(white_result[3], axis=0)
        
        # Load image for cropping
        image = Image.open(image_path).convert('L')
        
        # Crop the image
        cropped_image = crop_image(image, min_coords, max_coords)
        
        print(f"White pixel bounding box:")
        print(f"  Top-left: ({min_coords[0].numpy()}, {min_coords[1].numpy()})")
        print(f"  Bottom-right: ({max_coords[0].numpy()}, {max_coords[1].numpy()})")
        
        # Display the images
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.imshow(white_result[0], cmap='gray')
        plt.title("Original Image")
        
        plt.subplot(1, 3, 2)
        # Show white pixels highlighted
        white_pixels_highlighted = white_result[0].copy()
        white_pixels_highlighted[white_result[1].numpy()] = 0  # Make white pixels black for visibility
        plt.imshow(white_pixels_highlighted, cmap='gray')
        plt.title("White Pixels Highlighted")
        
        plt.subplot(1, 3, 3)
        plt.imshow(cropped_image, cmap='gray')
        plt.title("Cropped to White Content")
        plt.show()
        
        # Resize the cropped image for analysis
        resized_image = cropped_image.resize((100, 100))
        normalized_image = np.array(resized_image) / 255.0
        
        # Print image statistics
        print(f"\nImage Statistics:")
        print(f"Original image shape: {white_result[0].shape}")
        print(f"Cropped image shape: {np.array(cropped_image).shape}")
        print(f"Resized image shape: {normalized_image.shape}")
        print(f"Min pixel value: {normalized_image.min():.3f}")
        print(f"Max pixel value: {normalized_image.max():.3f}")
        print(f"Mean pixel value: {normalized_image.mean():.3f}")
        
    except Exception as e:
        print(f"Error processing white pixels: {e}")
        print(f"white_pixel_coords shape: {white_result[3].shape}")
        print(f"white_pixels_count: {white_result[2].numpy()}")
        
else:
    print("No white pixels found in the image!")
    plt.imshow(white_result[0], cmap='gray')
    plt.title("Original Image (No White Pixels Detected)")
    plt.show()

# Additional TensorFlow operations on the image
print(f"\nTensorFlow Operations:")
print(f"Image tensor shape: {white_result[4].shape}")
print(f"Image tensor dtype: {white_result[4].dtype}")
print(f"Min value in tensor: {tf.reduce_min(white_result[4]).numpy()}")
print(f"Max value in tensor: {tf.reduce_max(white_result[4]).numpy()}")
print(f"Mean value in tensor: {tf.reduce_mean(white_result[4]).numpy():.2f}")