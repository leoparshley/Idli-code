import streamlit as st
import textwrap

# Encoding dictionary
word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
digit_to_word = {v: k for k, v in word_to_digit.items()}
quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'}
binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

def text_to_idli_code(text):
    # Convert each character in text to binary, then group by 2 bits
    binary_str = ''.join([format(ord(c), '08b') for c in text])
    chunks = textwrap.wrap(binary_str, 2)
    
    # Convert binary chunks to quaternary, then to Idli words
    quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks])
    words = [digit_to_word[d] for d in quaternary if d in digit_to_word]
    
    # Check if all characters are valid
    if len(words) != len(quaternary):
        raise ValueError("Invalid characters detected. Please use only valid words: Idli, Dosa, Sambar, Chutney.")
    
    return ' '.join(words)

def idli_code_to_text(code):
    try:
        code_words = code.strip().split()
        
        # Convert words to quaternary digits
        quaternary = ''.join([word_to_digit[word] for word in code_words if word in word_to_digit])
        
        # Ensure all words are valid
        if len(quaternary) != len(code_words):
            raise ValueError("Invalid Idli Code format. Please use only valid words: Idli, Dosa, Sambar, Chutney.")
        
        # Convert quaternary to binary
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        
        # Convert binary back to text
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8])
        return decoded
    except Exception as e:
        return f"Error: {str(e)}"

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
        if user_input.strip() != "":
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            st.text_area("Encrypted Idli Code:", value=formatted, height=300)
            
            # Decrypt back to verify encryption-decryption pair
            decrypted = idli_code_to_text(encrypted)
            if decrypted == user_input:
                st.success("Encryption and Decryption successful! The text matches.")
            else:
                st.error("Error: Decryption mismatch. Please check the encryption and decryption process.")
        else:
            st.warning("Please enter text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip() != "":
            result = idli_code_to_text(code_input)
            st.text_area("Decrypted Text:", value=result, height=200)
            
            # Check if decrypted text matches the original code
            encrypted_check = text_to_idli_code(result)
            if encrypted_check == code_input.strip():
                st.success("Decryption and encryption matched!")
            else:
                st.error("Decryption mismatch detected.")
        else:
            st.warning("Please enter Idli Code to decrypt.")