# Import necessary libraries
import os
import pandas as pd
import numpy as np
from PIL import Image
import joblib  # For loading scikit-learn model

# Load the trained model from a file (in this case, using joblib)
model = joblib.load('trained_model.joblib')

# Function to preprocess an image before making predictions
def preprocess_image(image_path, target_size=(70, 70)):
    # Load image and convert it to RGB format
    image = Image.open(image_path).convert('RGB')
    
    # Resize the image to the specified target size
    resized_image = image.resize(target_size)
    
    # Normalize pixel values to the range [0, 1]
    preprocessed_image = np.array(resized_image) / 255.0  
    
    return preprocessed_image

# Function to predict the authenticity of a logo using the loaded model
def predict_logo_authenticity(image_path):
    # Preprocess the input image
    input_image = preprocess_image(image_path)
    
    # Flatten the input image if needed (depends on the model)
    flat_input = input_image.flatten().reshape(1, -1)
    
    # Make a prediction using the loaded model
    prediction = model.predict(flat_input)
    
    return prediction

# Example usage
genuine_logo_path = r'C:\Users\Soumyojyoti Saha\OneDrive - vit.ac.in\Desktop\logo-data-scraping-processing-main - Copy\genuinelogo.png'
result = predict_logo_authenticity(genuine_logo_path)

print("Raw model prediction:", result)  # Print the raw prediction

# Display the final prediction based on the model output
if result == 1:
    print("The logo is predicted to be genuine.")
else:
    print("The logo is predicted to be fake.")
