import streamlit as st
import textwrap
import base64

# Mapping
bit_to_word = {'00': 'Idli', '01': 'Dosa', '10': 'Sambar', '11': 'Chutney'}
word_to_bit = {v: k for k, v in bit_to_word.items()}

# Core functions
def binary_to_words(binary):
    if len(binary) % 2 != 0:
        binary += '0'
    return ' '.join([bit_to_word[binary[i:i+2]] for i in range(0, len(binary), 2)])

def words_to_binary(words):
    parts = words.strip().split()
    try:
        return ''.join([word_to_bit[w] for w in parts])
    except KeyError as e:
        raise ValueError(f"Invalid word found: {e}. Only Idli, Dosa, Sambar, Chutney are allowed.")

def text_to_idli_code(text):
    try:
        b64_encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        binary = ''.join(format(ord(c), '08b') for c in b64_encoded)
        return binary_to_words(binary)
    except Exception as e:
        return f"Encryption error: {e}"

def idli_code_to_text(code):
    try:
        binary = words_to_binary(code)
        byte_chunks = textwrap.wrap(binary, 8)
        chars = [chr(int(b, 2)) for b in byte_chunks if len(b) == 8]
        b64_text = ''.join(chars)
        decoded_bytes = base64.b64decode(b64_text)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"Decryption error: {e}"

def compare_texts(text1, text2):
    total = max(len(text1), len(text2))
    if total == 0:
        return 0.0
    mismatch = sum(a != b for a, b in zip(text1, text2)) + abs(len(text1) - len(text2))
    return round((mismatch / total) * 100, 2)

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

def download_button(data, filename, label):
    st.download_button(label=label, data=data, file_name=filename, mime="text/plain")

# Streamlit UI
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            decrypted = idli_code_to_text(encrypted)
            mismatch = compare_texts(user_input, decrypted)

            formatted_encrypted = format_idli_code(encrypted)
            st.text_area("Encrypted Idli Code:", value=formatted_encrypted, height=250)
            download_button(formatted_encrypted, "encrypted_idli_code.txt", "Download Encrypted Idli Code")

            st.text_area("Re-decrypted Encrypt:", value=decrypted, height=200)
            download_button(decrypted, "re_decrypted_text.txt", "Download Re-decrypted Output")

            st.write(f"Character Mismatch: **{mismatch}%**")
            if mismatch == 0:
                st.success("Success: input and encrypted-decrypted pair matched 100%.")
            else:
                st.error("Warning: Input and re-decrypted text do not match perfectly.")
        else:
            st.warning("Please enter text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip():
            decrypted_text = idli_code_to_text(code_input)
            re_encrypted = text_to_idli_code(decrypted_text)
            formatted_re_encrypted = format_idli_code(re_encrypted)
            mismatch = compare_texts(code_input.strip(), re_encrypted.strip())

            st.text_area("Decrypted Output:", value=decrypted_text, height=200)
            download_button(decrypted_text, "decrypted_text.txt", "Download Decrypted Text")

            st.text_area("Re-encrypted Decrypt:", value=formatted_re_encrypted, height=250)
            download_button(formatted_re_encrypted, "re_encrypted_code.txt", "Download Re-encrypted Output")

            st.write(f"Character Mismatch: **{mismatch}%**")
            if mismatch == 0:
                st.success("Success: Idli code and re-encrypted text matched 100%.")
            else:
                st.error("Warning: Idli code and re-encrypted output differ.")
        else:
            st.warning("Please enter Idli Code to decrypt.")