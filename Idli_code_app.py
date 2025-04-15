import streamlit as st
import textwrap

# Encoding dictionaries
bit_to_word = {
    '000': 'Idli',
    '001': 'Dosa',
    '010': 'Sambar',
    '011': 'Chutney',
    '100': 'Rasam',
    '101': 'Vada',
    '110': 'Pongal',
    '111': 'Payasam'
}
word_to_bit = {v: k for k, v in bit_to_word.items()}

# Functions
def text_to_idli_code(text):
    try:
        binary = ''.join([format(ord(c), '08b') for c in text])
        padded_binary = binary + '0' * ((3 - len(binary) % 3) % 3)  # Pad to make it multiple of 3
        chunks = textwrap.wrap(padded_binary, 3)
        words = [bit_to_word[chunk] for chunk in chunks]
        return ' '.join(words)
    except Exception as e:
        return f"Error during encryption: {e}"

def idli_code_to_text(code):
    try:
        words = code.strip().split()
        invalid_words = [w for w in words if w not in word_to_bit]
        if invalid_words:
            return f"Invalid word(s) found at: {', '.join(invalid_words)}. Only use: {', '.join(word_to_bit.keys())}"
        binary = ''.join([word_to_bit[w] for w in words])
        full_bytes = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in full_bytes if len(b) == 8])
        return decoded
    except Exception as e:
        return f"Error during decryption: {e}"

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

# Streamlit UI
st.title("Idli Code Encryptor & Decryptor (8 Word Robust Mode)")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip() != "":
            encrypted = text_to_idli_code(user_input)
            decrypted_back = idli_code_to_text(encrypted)
            if decrypted_back != user_input:
                st.error("Error: Decryption mismatch. Please check the encryption and decryption process.")
            else:
                formatted = format_idli_code(encrypted)
                st.text_area("Encrypted Idli Code:", value=formatted, height=300)
                st.success("Encryption and decryption are consistent.")
        else:
            st.warning("Please enter text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip() != "":
            result = idli_code_to_text(code_input)
            st.text_area("Decrypted Text:", value=result, height=200)
        else:
            st.warning("Please enter Idli Code to decrypt.")