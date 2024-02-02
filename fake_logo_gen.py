import os
import cv2
import pandas as pd

# Set input and output folders, and transformation parameters
logo_folder = 'output'
output = 'genLogoOutput'
scale_factor = 0.8
rotation_angle = 30

# Data list to store information about the transformed images
data = []

# Iterate through the logo images in the specified folder
for root, dirs, files in os.walk(logo_folder):
    for filename in files:
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust file extensions based on your logo image format
            logo_path = os.path.join(root, filename)
            brand_name = root.replace('output\\', '')

            brand_folder = os.path.join(output, brand_name)
            if not os.path.exists(brand_folder):
                os.makedirs(brand_folder)
            
            # Load the logo image
            image = cv2.imread(logo_path)
            
            # Apply rotation transformation
            rows, cols = image.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), rotation_angle, 1)
            rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
            
            # Save the rotated image
            cv2.imwrite(os.path.join(brand_folder, filename), rotated_image)
            
            # Update data list with information about the rotated image
            data.append({'Filename': os.path.join(brand_folder, filename), 'Brand Name': brand_name, 'Label': 'Fake'})

# Iterate through the logo images again to apply scaling transformation
for root, dirs, files in os.walk(logo_folder):
    for filename in files:
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust file extensions based on your logo image format
            logo_path = os.path.join(root, filename)
            brand_name = root.replace('output\\', '')

            brand_folder = os.path.join(output, brand_name)
            if not os.path.exists(brand_folder):
                os.makedirs(brand_folder)
            
            # Load the logo image
            image = cv2.imread(logo_path)
            
            # Apply scaling transformation
            scaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
            
            # Save the scaled image
            cv2.imwrite(os.path.join(brand_folder, 'scal_'+filename), scaled_image)
            
            # Update data list with information about the scaled image
            data.append({'Filename': os.path.join(brand_folder, 'scal_'+filename), 'Brand Name': brand_name, 'Label': 'Fake'})

# Read the existing CSV file containing original images information
df = pd.read_csv('file_map.csv')

# Concatenate the existing DataFrame with the new data
n_df = pd.concat([df, pd.DataFrame(data)], axis=0)

# Save the updated DataFrame to a new CSV file
n_df.to_csv('file_mapping.csv', index=False)

print("Done")
