import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import subprocess
result = subprocess.check_output(['python3', './Image_real_frame.py'], text=True).strip()
# Print TensorFlow version
print("TensorFlow version:", tf.__version__)

# Load MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize the data
x_train, x_test = x_train / 255.0, x_test / 255.0

# Load the image from your PC
image_path = "/Users/lordunited/Downloads/hello.jpg"  # Replace with your image path
image = Image.open(image_path).convert('L')  # Convert to grayscale

# Resize the image to 28x28 (MNIST size)
image = image.resize((2500, 2500))

# Normalize the image
image_array = np.array(image) / 255.0

# Display the image
plt.imshow(image_array, cmap='gray')
plt.title("Input Image")
plt.show()


# Reshape the image to match the model input shape
# Show the first image and its labe

# # Build a simple neural network model
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),      # Flatten 28x28 images to 1D
#     tf.keras.layers.Dense(128, activation='relu'),      # Hidden layer with 128 neurons
#     tf.keras.layers.Dense(10, activation='softmax')     # Output layer for 10 classes
# ])
#
# # Compile the model
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])
#
# # Train the model
# model.fit(x_train, y_train, epochs=5)
#
# # Evaluate the model
# test_loss, test_acc = model.evaluate(x_test, y_test)
# print('\nTest accuracy:', test_acc)