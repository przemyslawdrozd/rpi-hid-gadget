import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained model
model = load_model('angle_classification_model.h5')

# Define the size for resizing images
image_size = (60, 60)


# Function to load and preprocess images
def load_and_preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    return img_array


# Function to predict the direction
def predict_direction(image_path):
    img = load_and_preprocess_image(image_path)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    prediction = model.predict(img)
    direction_label = np.argmax(prediction)  # Get the class with the highest score
    return direction_label * 10  # Convert label back to angle


# Function to iterate over the directory and make predictions
def iterate_and_predict(data_lake_dir):
    images = []
    predictions = []

    # Iterate over files in the directory
    for filename in os.listdir(data_lake_dir):
        if filename.endswith('.png'):  # Check if it's a PNG image
            image_path = os.path.join(data_lake_dir, filename)
            predicted_angle = predict_direction(image_path)
            images.append(image_path)
            predictions.append(predicted_angle)

    return images, predictions


# Function to plot images with predictions
def plot_predictions(images, predictions):
    plt.figure(figsize=(12, 12))
    for i, (image_path, prediction) in enumerate(zip(images, predictions)):
        img = Image.open(image_path)
        plt.subplot(5, 5, i + 1)  # Assuming a maximum of 25 images per plot
        plt.imshow(img)
        plt.title(f"Predicted: {prediction}°")
        plt.axis('off')
        plt.tight_layout()
        plt.show()



# Main function to run the process
def main():
    data_lake_dir = 'data_lake'  # Directory containing the test images
    images, predictions = iterate_and_predict(data_lake_dir)
    plot_predictions(images, predictions)


# Run the main function
if __name__ == "__main__":
    main()
