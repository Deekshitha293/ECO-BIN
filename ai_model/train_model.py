import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load & Preprocess Data
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_data = datagen.flow_from_directory('dataset', target_size=(64, 64), class_mode='binary', subset='training')
val_data = datagen.flow_from_directory('dataset', target_size=(64, 64), class_mode='binary', subset='validation')

# Define AI Model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(64,64,3)),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile & Train
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_data, epochs=10, validation_data=val_data)

# Save Model
model.save("C:\Users\deeks\OneDrive\Desktop\ECO-BIN\ai_model/model.h5")
