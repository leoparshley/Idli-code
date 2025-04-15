import streamlit as st
import textwrap
import base64

# Mapping 2-bit binary to idli words
bit_to_word = {
    '00': 'Idli',
    '01': 'Dosa',
    '10': 'Sambar',
    '11': 'Chutney'
}
word_to_bit = {v: k for k, v in bit_to_word.items()}

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

def compare_texts(original, recovered):
    total = max(len(original), len(recovered))
    if total == 0:
        return 0
    mismatch = sum(o != r for o, r in zip(original, recovered)) + abs(len(original) - len(recovered))
    error_percent = (mismatch / total) * 100
    return round(error_percent, 2)

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

# Streamlit UI
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            decrypted = idli_code_to_text(encrypted)

            error_percent = compare_texts(user_input, decrypted)

            st.text_area("Encrypted Idli Code:", value=encrypted, height=250)
            st.text_area("Encrypt-Decryption Pair:", value=decrypted, height=200)
            st.write(f"Character Mismatch: **{error_percent}%**")

            if error_percent == 0:
                st.success("Success: Input and encrypt-decrypt pair matched 100%.")
            else:
                st.error("Warning: Decryption mismatch detected.")
        else:
            st.warning("Please enter text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip():
            result = idli_code_to_text(code_input)
            st.text_area("Decrypted Output:", value=result, height=200)
        else:
            st.warning("Please enter Idli Code to decrypt.")