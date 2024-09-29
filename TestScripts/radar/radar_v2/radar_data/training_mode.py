import tensorflow as tf
from tensorflow.keras import layers, models
from PIL import Image
import numpy as np
import pandas as pd
import os

# Define image size for resizing
image_size = (60, 60)

# Path to the directory containing training images
image_dir = './training_data'

# Path to the CSV file
csv_file = './labels.csv'

# Load the CSV file
data = pd.read_csv(csv_file)


# Function to load and preprocess images
def load_and_preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    return img_array


# Function to map angle to categorical index
def map_angle_to_label(angle):
    # Round the angle to the nearest multiple of 10
    rounded_angle = round(angle / 10) * 10

    # Ensure the rounded angle is within the valid range of 0 to 350
    if rounded_angle < 0 or rounded_angle >= 360:
        raise ValueError(f"Angle {angle} is out of bounds. Must be between 0 and 350.")

    # Create a mapping from angles (0, 10, 20, ..., 350) to labels (0, 1, 2, ..., 35)
    angle_map = {i: idx for idx, i in enumerate(range(0, 360, 10))}

    return angle_map[rounded_angle]


# Load and preprocess images and labels from the CSV
images = []
labels = []

for index, row in data.iterrows():
    image_path = os.path.join(image_dir, row['image_filename'])
    angle = row['angle']

    # Load and preprocess the image
    img_array = load_and_preprocess_image(image_path)
    images.append(img_array)

    # Convert angle to label
    label = map_angle_to_label(angle)
    labels.append(label)

# Convert to numpy arrays
images = np.array(images)
labels = np.array(labels)

# Build a simple CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(60, 60, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(36)  # Output layer for 36 classes (0 to 350 in increments of 10)
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model
model.fit(images, labels, epochs=10)

# Evaluate model performance
loss, accuracy = model.evaluate(images, labels)

print(f"Loss: {loss}, Accuracy: {accuracy}")
model.save('angle_classification_model.h5')
