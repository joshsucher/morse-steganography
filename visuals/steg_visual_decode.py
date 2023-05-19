import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from PIL import Image

# Load the sound data
wav_path = "happy_mac.wav"  # Replace with the path to your .wav file
sample_rate, sound_data = wavfile.read(wav_path)

# Reshape the sound data back into a 2D array
image_shape = (258, 195)  # Replace with the original shape of your image
sound_data = sound_data[:np.product(image_shape)]
sound_data = sound_data.reshape(image_shape)

# Create a 2D sinusoidal pattern with the same shape as the image
x = np.linspace(0, 2 * np.pi, image_shape[1])  # x-coordinates
y = np.linspace(0, 2 * np.pi, image_shape[0])  # y-coordinates
X, Y = np.meshgrid(x, y)  # Create a 2D grid of coordinates
sinusoid = np.sin(X) * np.sin(Y)  # Create a 2D sinusoidal pattern

# Add a small constant to avoid division by zero
EPSILON = 1e-7
sinusoid += EPSILON

# Demodulate the sound data with the sinusoidal pattern
image_data = sound_data / sinusoid

# Normalize pixel values to the range 0-255
image_data = (image_data * 255).astype(np.uint8)

# Create an image from the data
decoded_image = Image.fromarray(image_data, 'L')

# Save the image
decoded_image.save('decoded_happy_mac.png')
