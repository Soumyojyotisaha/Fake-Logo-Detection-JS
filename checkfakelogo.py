import os
import pandas as pd
import numpy as np
from PIL import Image
import joblib  # For loading scikit-learn model

# Load the trained model
model = joblib.load('trained_model.joblib')

def preprocess_image(image_path, target_size=(70, 70)):
    # Load image and preprocess
    image = Image.open(image_path).convert('RGB')
    resized_image = image.resize(target_size)
    preprocessed_image = np.array(resized_image) / 255.0  # Normalize pixel values
    return preprocessed_image

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

if result == 1:
    print("The logo is predicted to be genuine.")
else:
    print("The logo is predicted to be fake.")