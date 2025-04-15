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
    # Clean the input by removing extra spaces and line breaks
    code = code.replace('\n', ' ').replace('  ', ' ').strip()
    
    try:
        # Convert the idli code back to quaternary
        words = code.split()
        quaternary = [word_to_quat[word] for word in words]
        # Convert quaternary to binary
        binary = ''.join(quat_to_bin[q] for q in quaternary)
        # Convert binary to text
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    except Exception as e:
        return "Invalid Idli Code! Please ensure the input is correct."

# Streamlit settings
st.set_page_config(page_title="Idli Code Encryptor", layout="centered")
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option", ["Encrypt", "Decrypt"])

if option == "Encrypt":
    text = st.text_area("Enter text to encrypt", height=200)
    if st.button("Encrypt"):
        encrypted_text = encrypt(text)
        # Add line breaks in encrypted text for better display
        wrapped_encrypted_text = '\n'.join([encrypted_text[i:i+60] for i in range(0, len(encrypted_text), 60)])
        # Display the formatted output in a text area
        st.text_area("Encrypted Idli Code (Copyable Version)", value=wrapped_encrypted_text, height=300)

else:
    code = st.text_area("Enter Idli code to decrypt", height=200)
    if st.button("Decrypt"):
        decrypted_text = decrypt(code)
        # Display the decrypted text
        st.text_area("Decrypted text", value=decrypted_text, height=200)
