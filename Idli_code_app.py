import streamlit as st

# Function to encrypt the text
def encrypt(text):
    # Simple encryption logic (you can change this)
    encrypted_text = ''.join([chr(ord(c) + 3) for c in text])  # Shift each char by 3
    return encrypted_text

# Function to decrypt the text
def decrypt(text):
    try:
        decrypted_text = ''.join([chr(ord(c) - 3) for c in text])  # Reverse the shift
        return decrypted_text
    except Exception as e:
        return f"Error during decryption: {str(e)}"

# Streamlit app UI
st.title("Encryption/Decryption App")

# User input
input_text = st.text_area("Enter your text to encrypt", height=200)

# Encrypt button
if st.button("Encrypt"):
    encrypted_text = encrypt(input_text)
    st.subheader("Encrypted Text:")
    st.text_area("Encrypted Text", encrypted_text, height=200)
    st.write("You can copy the encrypted text for decryption.")

# Decrypt button
if st.button("Decrypt"):
    encrypted_input = st.text_area("Enter encrypted text to decrypt", height=200)
    if encrypted_input:
        decrypted_text = decrypt(encrypted_input)
        if "Error during decryption" in decrypted_text:
            st.error(decrypted_text)  # Show error if decryption fails
        else:
            st.subheader("Decrypted Text:")
            st.text_area("Decrypted Text", decrypted_text, height=200)
            if decrypted_text == input_text:
                st.success("Decryption successful! The text matches the original.")
            else:
                st.error("Decryption mismatch! The text does not match the original.")