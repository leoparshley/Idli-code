import streamlit as st

# Mappings
word_to_quat = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
quat_to_word = {v: k for k, v in word_to_quat.items()}
quat_to_bin = {'0': '00', '1': '01', '2': '10', '3': '11'}
bin_to_quat = {v: k for k, v in quat_to_bin.items()}

def encrypt(text):
    binary = ''.join(format(ord(c), '08b') for c in text)
    quaternary = [bin_to_quat[binary[i:i+2]] for i in range(0, len(binary), 2)]
    return ' '.join(quat_to_word[q] for q in quaternary)

def decrypt(code):
    code = ' '.join(code.split())
    try:
        words = code.split()
        quaternary = [word_to_quat[word] for word in words]
        binary = ''.join(quat_to_bin[q] for q in quaternary)
        text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return text
    except:
        return "Invalid Idli Code! Please ensure the input is correct."

def format_output(text, words_per_line=10):
    words = text.split()
    lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

# Streamlit UI
st.set_page_config(page_title="Idli Code Encryptor", layout="centered")
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option", ["Encrypt", "Decrypt"])

if option == "Encrypt":
    text = st.text_area("Enter text to encrypt", height=200)
    if st.button("Encrypt"):
        encrypted_text = encrypt(text)
        formatted = format_output(encrypted_text, words_per_line=10)
        st.code(formatted)
        st.download_button("Download Encrypted Text", formatted, "encrypted.txt")

else:
    code = st.text_area("Enter Idli code to decrypt", height=200)
    if st.button("Decrypt"):
        decrypted_text = decrypt(code)
        st.code(decrypted_text)
        st.download_button("Download Decrypted Text", decrypted_text, "decrypted.txt")