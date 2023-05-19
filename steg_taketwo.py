import numpy as np
import soundfile as sf
import librosa

# Load audio
file_path = "Sample_BeeMoved_96kHz24bit.wav"
audio_data, sample_rate = librosa.load(file_path, sr=None)

# Message to encode
message = "PAUL IS DEAD"

# Function to generate binary code signals
def binary_encode(message, sample_rate):
    WPM = 20  # Words per minute
    FREQ = 14000  # Frequency of the binary code signals
    dit_duration = 1.2 / WPM  # Duration of a "0" (dit)
    dah_duration = dit_duration * 3  # Duration of a "1" (dah)

    binary_signal = []

    for char in message:
        binary = format(ord(char), '08b')  # Convert the character to binary
        for bit in binary:
            signal_duration = dit_duration if bit == '0' else dah_duration
            num_samples = int(signal_duration * sample_rate)
            t = np.linspace(0, signal_duration, num_samples, False)
            sine_wave = 0.3 * np.sin(2 * np.pi * FREQ * t)
            binary_signal.extend(sine_wave)
            # Add a short pause after every bit
            binary_signal.extend([0] * int(dit_duration * sample_rate))
        # Add a longer pause after each character
        binary_signal.extend([0] * int(dit_duration * sample_rate * 3))
    return np.array(binary_signal)

binary_signal = binary_encode(message, sample_rate)

# Add 2 seconds delay before binary code starts
binary_signal = np.pad(binary_signal, (2 * sample_rate, 0), 'constant')

# Repeat original audio to match the length of the binary signal
audio_repeated = np.tile(audio_data, int(np.ceil(len(binary_signal) / len(audio_data))))
new_audio_data = np.copy(audio_repeated)

# Overlay binary code signals onto the audio
new_audio_data[:len(binary_signal)] += binary_signal

# Save to a new .wav file
sf.write('audio_with_binary.wav', new_audio_data, sample_rate)
