import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

file_path = 'CropRecommendationApp/Model/Crop_recommendation.csv'

# Load the dataset
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# Check class balance
counts = df['label'].value_counts()
print("Original class counts:")
print(counts)

# Upsample minority classes (the new crops have 5, old have 100)
# Let's find all classes with less than 100 samples and duplicate them to reach 100
max_count = 100
frames = [df]

for label, count in counts.items():
    if count < max_count:
        # Get the subset for this label
        subset = df[df['label'] == label]
        # Calculate how many more we need
        needed = max_count - count
        # Sample with replacement to get exactly 'needed' samples
        upsampled = subset.sample(n=needed, replace=True, random_state=42)
        frames.append(upsampled)

# Combine all frames
balanced_df = pd.concat(frames, ignore_index=True)

print("\nBalanced class counts:")
print(balanced_df['label'].value_counts())

X = balanced_df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = balanced_df['label']

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"\nModel accuracy after balancing: {accuracy*100:.2f}%")

with open('CropRecommendationApp/Model/Crop_Recommendation.pkl', 'wb') as f:
    pickle.dump((model, encoder, accuracy), f)
    
print("Model retrained and saved successfully.")