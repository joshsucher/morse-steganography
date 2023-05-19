import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from PIL import Image

# Load the image
image_path = "happy_mac.png"  # Replace with the path to your image
image = Image.open(image_path).convert('L')  # Convert the image to grayscale

# Normalize pixel values to the range 0-1
image_data = np.array(image) / 255

# Create a 2D sinusoidal pattern with the same shape as the image
x = np.linspace(0, 2 * np.pi, image_data.shape[1])  # x-coordinates
y = np.linspace(0, 2 * np.pi, image_data.shape[0])  # y-coordinates
X, Y = np.meshgrid(x, y)  # Create a 2D grid of coordinates
sinusoid = np.sin(X) * np.sin(Y)  # Create a 2D sinusoidal pattern

# Modulate the sinusoidal pattern with the image data
sound_data = image_data * sinusoid

# Convert the sound data into a 1D signal
sound_data = sound_data.flatten()

# Save the sound data as a .wav file
wavfile.write('happy_mac.wav', 44100, sound_data)
