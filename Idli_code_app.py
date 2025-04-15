import streamlit as st
import textwrap

# 2-bit to word mapping
bit_to_word = {
    '00': 'Idli',
    '01': 'Dosa',
    '10': 'Sambar',
    '11': 'Chutney'
}
word_to_bit = {v: k for k, v in bit_to_word.items()}

# Functions
def text_to_idli_code(text):
    try:
        binary = ''.join(format(ord(c), '08b') for c in text)  # 8-bit per character
        chunks = textwrap.wrap(binary, 2)  # Break into 2-bit pieces
        words = [bit_to_word[b] for b in chunks]
        return ' '.join(words)
    except Exception as e:
        return f"Error during encryption: {e}"

def idli_code_to_text(code):
    try:
        words = code.strip().split()
        invalid = [w for w in words if w not in word_to_bit]
        if invalid:
            return f"Invalid word(s): {', '.join(invalid)}. Only use: Idli, Dosa, Sambar, Chutney"
        bits = ''.join([word_to_bit[w] for w in words])
        byte_chunks = textwrap.wrap(bits, 8)
        decoded = ''.join(chr(int(b, 2)) for b in byte_chunks if len(b) == 8)
        return decoded
    except Exception as e:
        return f"Error during decryption: {e}"

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

# Streamlit UI
st.title("Idli Code (4-Word Edition) Encryptor & Decryptor")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            decrypted_back = idli_code_to_text(encrypted)
            if decrypted_back != user_input:
                st.error("Error: Decryption mismatch! Encryption failed safely.")
            else:
                formatted = format_idli_code(encrypted)
                st.text_area("Encrypted Idli Code:", value=formatted, height=300)
                st.success("Encryption & decryption matched.")
        else:
            st.warning("Please enter text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip():
            result = idli_code_to_text(code_input)
            st.text_area("Decrypted Text:", value=result, height=200)
        else:
            st.warning("Please enter Idli Code to decrypt.")