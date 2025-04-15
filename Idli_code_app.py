import streamlit as st
import textwrap

# Encoding and decoding dictionaries
word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
digit_to_word = {v: k for k, v in word_to_digit.items()}
quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'}
binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

def text_to_idli_code(text):
    binary_str = ''.join([format(ord(c), '08b') for c in text])
    chunks = textwrap.wrap(binary_str, 2)
    quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks])
    words = [digit_to_word[d] for d in quaternary if d in digit_to_word]
    return ' '.join(words)

def idli_code_to_text(code):
    try:
        code_words = code.strip().split()
        quaternary = ''.join([word_to_digit[word] for word in code_words])
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8])
        return decoded
    except Exception as e:
        return "Invalid Idli Code format. Please check spacing and try again."

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

def generate_download_link(content, filename):
    """Generate download link for given content."""
    return f'<a href="data:file/txt;base64,{base64.b64encode(content.encode()).decode()}" download="{filename}">Download {filename}</a>'

# Streamlit UI
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip() != "":
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            re_decrypted = idli_code_to_text(formatted)
            accuracy = (user_input == re_decrypted)
            st.text_area("Encrypted Idli Code:", value=formatted, height=300)
            st.markdown(generate_download_link(formatted, "idli_code.txt"), unsafe_allow_html=True)

            st.text_area("Re-Decrypted Encrypt Output:", value=re_decrypted, height=200)
            st.markdown(generate_download_link(re_decrypted, "redecrypted_output.txt"), unsafe_allow_html=True)

            if accuracy:
                st.success("Success: input and re-decrypted encrypt matched 100%")
            else:
                st.error(f"Error: {100 - accuracy}% mismatch between input and encrypted-decrypted pair")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip() != "":
            decrypted = idli_code_to_text(code_input)
            re_encrypted = text_to_idli_code(decrypted)
            accuracy = (code_input.strip() == re_encrypted.strip())
            st.text_area("Decrypted Text:", value=decrypted, height=200)
            st.markdown(generate_download_link(decrypted, "decrypted_text.txt"), unsafe_allow_html=True)

            st.text_area("Re-Decrypted Encrypt Output:", value=re_encrypted, height=200)
            st.markdown(generate_download_link(re_encrypted, "reencrypted_output.txt"), unsafe_allow_html=True)

            if accuracy:
                st.success("Success: decrypted text and re-encrypted encrypt matched 100%")
            else:
                st.error(f"Error: {100 - accuracy}% mismatch in round-trip encryption")

        else:
            st.warning("Please enter Idli Code to decrypt.")