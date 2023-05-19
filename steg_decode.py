import numpy as np
import soundfile as sf
from scipy import signal
import librosa

# Morse Code Dictionary 
MORSE_CODE_DICT = {
    'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 
    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 
    'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 
    'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 
    'Z':'--..', '1':'.----', '2':'..---', '3':'...--', 
    '4':'....-', '5':'.....', '6':'-....', '7':'--...', 
    '8':'---..', '9':'----.', '0':'-----', ',':'--..--', 
    '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', 
    '(':'-.--.', ')':'-.--.-'}

# Function to convert Morse code to text
def morse_to_text(symbols):
    reverse_morse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}  # Reverse the dictionary
    words = symbols.strip().split(' / ')  # Split the Morse code symbols into words
    return ' '.join(''.join(reverse_morse_dict.get(symbol, '') for symbol in word.split(' ')) for word in words)  # Convert each word from Morse code to text and join them with spaces

# Load the encoded audio
file_path = "Steg14.wav"
audio_data, sample_rate = librosa.load(file_path, sr=None)

# Parameters for band-pass Butterworth filter
FREQ = 13954  # Frequency of the Morse code signals
WPM = 20  # Words per minute
TIME_UNIT = 1.2 / WPM  # Time unit duration in seconds
TIME_UNIT_SAMPLES = TIME_UNIT * sample_rate  # Time unit duration in samples

dot_duration_samples = TIME_UNIT_SAMPLES  # Duration of a "dot" in samples
dash_duration_samples = 3 * TIME_UNIT_SAMPLES  # Duration of a "dash" in samples
inter_element_samples = TIME_UNIT_SAMPLES  # Space between elements in samples
inter_letter_samples = 3 * TIME_UNIT_SAMPLES  # Space between letters in samples
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

# Threshold the envelope to get the Morse code signals
threshold = 0.03
morse_code_signals = envelope > threshold

# Convert the Morse code signals and silence into chunks
chunks = []
current_chunk = []
current_state = morse_code_signals[0]
for sample, signal in enumerate(morse_code_signals):
    if signal == current_state:
        current_chunk.append(sample)
    else:
        chunks.append((current_state, current_chunk))
        current_chunk = [sample]
        current_state = signal
chunks.append((current_state, current_chunk))  # Append the last chunk

# Convert the chunks into Morse code symbols
morse_code_symbols = []
for state, chunk in chunks:
    if state == True:  # Morse code signal
        if len(chunk) > 1.5 * dot_duration_samples:
            morse_code_symbols.append('-')
        else:
            morse_code_symbols.append('.')
    else:  # Silence
        if len(chunk) > 1 * inter_word_samples:
            morse_code_symbols.append(' / ')  # Inter-word space
        elif len(chunk) > 1 * inter_letter_samples:
            morse_code_symbols.append(' ')  # Inter-letter space
        else:
            pass  # Ignore inter-element spaces

morse_code_string = ''.join(morse_code_symbols)
print("Morse symbols:", morse_code_string)

# Convert the Morse code symbols to text
message = morse_to_text(morse_code_string)
print("Decoded message:", message)
