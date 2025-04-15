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

# Padding helper
def pad_to_multiple_of_8(bits):
    pad_len = (8 - len(bits) % 8) % 8
    return bits + ('0' * pad_len), pad_len

def text_to_idli_code(text):
    try:
        binary = ''.join(format(ord(c), '08b') for c in text)  # 8-bit per char
        binary, pad_len = pad_to_multiple_of_8(binary)
        chunks = textwrap.wrap(binary, 2)
        words = [bit_to_word[b] for b in chunks]
        words.append(f"PAD_{pad_len}")  # Store padding length as word
        return ' '.join(words)
    except Exception as e:
        return f"Error during encryption: {e}"

def idli_code_to_text(code):
    try:
        words = code.strip().split()

        # Check for valid words & retrieve pad info
        pad_word = words[-1]
        if not pad_word.startswith("PAD_"):
            return "Missing padding info. Invalid or incomplete Idli Code."

        try:
            pad_len = int(pad_word.split("_")[1])
        except:
            return "Invalid padding info. Corrupted Idli Code."

        words = words[:-1]  # remove pad word

        invalid = [w for w in words if w not in word_to_bit]
        if invalid:
            return f"Invalid word(s): {', '.join(invalid)}. Only use: Idli, Dosa, Sambar, Chutney"

        bits = ''.join([word_to_bit[w] for w in words])
        if pad_len > 0:
            bits = bits[:-pad_len]

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
st.title("Idli Code (4-Word Only) Encryptor & Decryptor")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            decrypted_back = idli_code_to_text(encrypted)
            if decrypted_back != user_input:
                st.error("Error: Decryption mismatch! Encryption failed safely.")
                st.text("Debug Decrypted Output:\n" + decrypted_back)
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