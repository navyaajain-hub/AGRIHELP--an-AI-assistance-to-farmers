import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV3Large

# 1. Image Settings and Path Configuration
BATCH_SIZE = 32
IMG_SIZE = (224, 224)
DATASET_DIR = "./plantvillage dataset/color" 

print("⚡ Loading datasets from folders...")

# Load training data (80%)
train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

# Load validation data (20%)
val_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

# Extract and save the class names to a text file for your backend to read later
class_names = train_dataset.class_names
num_classes = len(class_names)
print(f"✅ Found {num_classes} folders/classes.")

with open("class_names.txt", "w") as f:
    for name in class_names:
        f.write(f"{name}\n")
print("📝 Saved 'class_names.txt'")

# Optimize data loading pipeline for performance
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
val_dataset = val_dataset.prefetch(buffer_size=AUTOTUNE)

# 2. Build the CNN Model Architecture (Transfer Learning via MobileNetV3)
def build_model(num_classes):
    # Load MobileNetV3 pre-trained on ImageNet without the top classification layer
    base_model = MobileNetV3Large(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze base weights
    
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = layers.Rescaling(1./255)(inputs)  # Normalize pixel inputs between 0 and 1
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)             # Drop out to prevent overfitting
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    return models.Model(inputs, outputs)

model = build_model(num_classes)

# 3. Compile the Model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 4. Start the Training Run
EPOCHS = 10  # You can increase this to 20 or 30 for higher accuracy later
print(f"🚀 Starting model training for {EPOCHS} epochs...")

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS
)

# 5. Save the trained weights file
model.save("agrobot_cnn_model.keras")
print("🎉 Model successfully trained and saved as 'agrobot_cnn_model.keras'!")
