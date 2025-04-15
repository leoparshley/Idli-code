import streamlit as st

# Mappings
word_to_quat = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
quat_to_word = {v: k for k, v in word_to_quat.items()}
quat_to_bin = {'0': '00', '1': '01', '2': '10', '3': '11'}
bin_to_quat = {v: k for k, v in quat_to_bin.items()}

def encrypt(text):
    # Convert text to binary
    binary = ''.join(format(ord(c), '08b') for c in text)
    # Convert binary to quaternary
    quaternary = [bin_to_quat[binary[i:i+2]] for i in range(0, len(binary), 2)]
    # Return as space-separated code
    return ' '.join(quat_to_word[q] for q in quaternary)

def decrypt(code):
    # Clean the input by removing extra spaces, line breaks, and empty characters
    code = ' '.join(code.split())  # This removes all unnecessary spaces and newlines
    
    try:
        # Convert the idli code back to quaternary
        words =