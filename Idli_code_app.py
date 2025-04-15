import streamlit as st

# Dictionaries
char_to_quat = {'0': 'Idli', '1': 'Dosa', '2': 'Sambar', '3': 'Chutney'}
quat_to_bin = {'Idli': '00', 'Dosa': '01', 'Sambar': '10', 'Chutney': '11'}

# Encryption
def encrypt_text(text):
    binary = ''.join([format(ord(char), '08b') for char in text])
    quaternary = [str(int(binary[i:i+2], 2)) for i in range(0, len(binary), 2)]
    encrypted = [char_to_quat[q] for q in quaternary]
    
    # Break lines to 10 words per line
    formatted = ''
    for i in range(0, len(encrypted), 10):
        formatted += ' '.join(encrypted[i:i+10]) + '\n'
    return formatted.strip()

# Decryption
def decrypt_text(code):
    code_words = code.strip().split()
    binary = ''
    for index, word in enumerate(code_words):
        if word not in quat_to_bin:
            return f"Error: Invalid word '{word}' at position {index + 1}."
        binary += quat_to_bin[word]
    
    # 8-bit chunks
    if len(binary) % 8 != 0:
        return "Error: Binary stream is not aligned in 8-bit chunks. Check your code."
    
    decoded = ''
    for i in range(0, len(binary), 8):
        decoded += chr(int(binary[i:i+8], 2))
    return decoded

# Streamlit UI
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an action", ("Encrypt", "Decrypt"))

if option == "Encrypt":
    user_input = st.text_area("Enter the message to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            result = encrypt_text(user_input)
            st.text_area("Encrypted Idli Code (copy this)", result, height=200)
            st.download_button("Download Encrypted Code", result, file_name="idli_code.txt")
        else:
            st.warning("Please enter some text to encrypt.")

else:
    code_input = st.text_area("Enter your Idli Code to decrypt:")
    if st.button("Decrypt"):
        if code_input.strip():
            result = decrypt_text(code_input)
            st.text_area("Decrypted Message", result, height=200)
        else:
            st.warning("Please enter the Idli code.")