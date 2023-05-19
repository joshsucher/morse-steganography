import numpy as np
import soundfile as sf
import librosa

# Morse Code Dictionary 
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ',':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

# Load audio
file_path = "Sample_BeeMoved_96kHz24bit.wav"
audio_data, sample_rate = librosa.load(file_path, sr=None)

# Message to encode
message = "PAUL IS DEAD"

# Function to generate Morse code signals
def morse_encode(message, sample_rate):
    WPM = 20  # Words per minute
    FREQ = 14000  # Frequency of the Morse code signals
    dot_duration = 1.2 / WPM  # Duration of a "dot"
    dash_duration = dot_duration * 3  # Duration of a "dash"

    morse_signal = []

    for char in message:
        if char == ' ':
            # Add a longer pause for a space
            morse_signal.extend([0] * int(sample_rate * dot_duration * 7))
        elif char.upper() in MORSE_CODE_DICT:
            morse_code = MORSE_CODE_DICT[char.upper()]
            for signal in morse_code:
                t = np.linspace(0, dot_duration if signal == '.' else dash_duration, int(dot_duration * sample_rate if signal == '.' else dash_duration * sample_rate), False)
                sine_wave = 0.3 * np.sin(2 * np.pi * FREQ * t)
                morse_signal.extend(sine_wave)
                # Add a short pause after every signal (dot/dash)
                morse_signal.extend([0] * int(sample_rate * dot_duration))
            # Add a longer pause after each character
            morse_signal.extend([0] * int(sample_rate * dot_duration * 3))
    return np.array(morse_signal)

morse_signal = morse_encode(message, sample_rate)

# Add 2 seconds delay before Morse code starts
morse_signal = np.pad(morse_signal, (2 * sample_rate, 0), 'constant')

# Overlay Morse code signals onto the audio
new_audio_data = np.copy(audio_data)
new_audio_data[:len(morse_signal)] += morse_signal

# Save to a new .wav file
sf.write('audio_with_morse.wav', new_audio_data, sample_rate)
