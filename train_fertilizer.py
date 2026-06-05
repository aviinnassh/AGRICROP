import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('CropRecommendationApp/Model/Fertilizer Prediction.csv')

# Strip whitespace from column names just in case
df.columns = df.columns.str.strip()

# Encoding categorical variables
soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()
fertilizer_encoder = LabelEncoder()

df['Soil Type'] = soil_encoder.fit_transform(df['Soil Type'])
df['Crop Type'] = crop_encoder.fit_transform(df['Crop Type'])
df['Fertilizer Name'] = fertilizer_encoder.fit_transform(df['Fertilizer Name'])

X = df[['Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']]
y = df['Fertilizer Name']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate accuracy
accuracy = model.score(X_test, y_test)
print(f"Model trained with accuracy: {accuracy*100:.2f}%")

# Save the model and encoders
with open('CropRecommendationApp/Model/Fertilizer_Recommendation.pkl', 'wb') as f:
    pickle.dump((model, soil_encoder, crop_encoder, fertilizer_encoder), f)

print("Model saved to CropRecommendationApp/Model/Fertilizer_Recommendation.pkl")
