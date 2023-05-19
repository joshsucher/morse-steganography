import numpy as np
import soundfile as sf
from scipy import signal
import librosa

# Load the encoded audio
file_path = "audio_with_binary.wav"
audio_data, sample_rate = librosa.load(file_path, sr=None)

# Parameters for band-pass Butterworth filter
FREQ = 14000  # Frequency of the binary code signals
WPM = 20  # Words per minute
TIME_UNIT = 1.2 / WPM  # Time unit duration in seconds
TIME_UNIT_SAMPLES = TIME_UNIT * sample_rate  # Time unit duration in samples

dit_duration_samples = TIME_UNIT_SAMPLES  # Duration of a "0" (dit) in samples
dah_duration_samples = 3 * TIME_UNIT_SAMPLES  # Duration of a "1" (dah) in samples
inter_bit_samples = TIME_UNIT_SAMPLES  # Space between bits in samples
inter_char_samples = 3 * TIME_UNIT_SAMPLES  # Space between characters in samples
inter_word_samples = 7 * TIME_UNIT_SAMPLES  # Space between words in samples

# Design the Butterworth filter
N  = 2    # Filter order
Wn = [FREQ-100, FREQ+100]  # Cutoff frequency
b, a = signal.butter(N, Wn, fs=sample_rate, btype='band')

# Apply the filter
filtered_audio = signal.filtfilt(b, a, audio_data)

# Get the envelope of the signal
analytic_signal = signal.hilbert(filtered_audio)
envelope = np.abs(analytic_signal)

# Threshold the envelope to get the binary code signals
threshold = 0.03
binary_code_signals = envelope > threshold

# Convert the binary code signals and silence into chunks
chunks = []
current_chunk = []
current_state = binary_code_signals[0]
for sample, signal in enumerate(binary_code_signals):
    if signal == current_state:
        current_chunk.append(sample)
    else:
        chunks.append((current_state, current_chunk))
        current_chunk = [sample]
        current_state = signal
chunks.append((current_state, current_chunk))  # Append the last chunk

# Convert the chunks into binary code symbols
binary_code_symbols = []
for state, chunk in chunks:
    if state == True:  # Binary code signal
        if len(chunk) > 1.5 * dit_duration_samples:
            binary_code_symbols.append('1')
        else:
            binary_code_symbols.append('0')
    else:  # Silence
        if len(chunk) > 1 * inter_word_samples:
            binary_code_symbols.append(' ')  # Inter-word space
        elif len(chunk) > 1 * inter_char_samples:
            binary_code_symbols.append(' ')  # Inter-character space
        else:
            pass  # Ignore inter-bit spaces

binary_code_string = ''.join(binary_code_symbols)
print("Binary symbols:", binary_code_string)

# Convert the binary code symbols to text
binary_codes = binary_code_string.split()
binary_codes = [code for code in binary_codes if len(code) == 8]  # Only keep 8-bit codes
message = ''.join(chr(int(code, 2)) for code in binary_codes)
print("Decoded message:", message)
