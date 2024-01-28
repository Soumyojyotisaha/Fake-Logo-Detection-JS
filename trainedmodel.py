import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import joblib

# Load data from the CSV file
df = pd.read_csv('file_mapping.csv')

# Adjust rotation angle and scaling factor in preprocess_image function
def preprocess_image(image_path, target_size=(70, 70), rotation_angle=45, scale_factor=0.7):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")

    rows, cols = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), rotation_angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    scaled_image = cv2.resize(rotated_image, target_size)
    flattened_image = scaled_image.flatten()
    return flattened_image

# Apply preprocessing to each image and create feature matrix X and labels y
X = np.array([preprocess_image(row['Filename']) for _, row in df.iterrows()])
y = df['Label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest classifier with adjusted parameters
clf = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))

# Train the classifier
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = metrics.accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the trained model to a file
joblib.dump(clf, 'trained_model.joblib')

# Now you can use the trained model for predictions on new data
# For example, you can predict the label for a new image as follows:
new_image_path = os.path.join(os.getcwd(), 'path', 'to', 'your', 'new_image.png')
try:
    new_image = np.array([preprocess_image(new_image_path)])
    predicted_label = clf.predict(new_image)
    print(f"Predicted Label for the new image: {predicted_label}")
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
