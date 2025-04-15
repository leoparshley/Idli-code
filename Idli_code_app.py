import streamlit as st
import textwrap
import base64

# Encoding dictionaries
word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
digit_to_word = {v: k for k, v in word_to_digit.items()}
quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'}
binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

# Functions
def text_to_idli_code(text):
    binary_str = ''.join([format(ord(c), '08b') for c in text])
    chunks = textwrap.wrap(binary_str, 2)
    quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks])
    words = [digit_to_word[d] for d in quaternary if d in digit_to_word]
    return ' '.join(words)

def idli_code_to_text(code):
    try:
        code_words = code.strip().split()
        quaternary = ''.join([word_to_digit[word] for word in code_words if word in word_to_digit])
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8])
        return decoded
    except Exception as e:
        return f"Decryption error: {e}"

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

def generate_download_link(content, filename):
    b64 = base64.b64encode(content.encode("utf-8")).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def calculate_accuracy(original, result):
    cleaned_original = ''.join(original.split())
    cleaned_result = ''.join(result.split())
    total = max(len(cleaned_original), 1)
    matches = sum(o == r for o, r in zip(cleaned_original, cleaned_result))
    return (matches / total) * 100

# UI
st.set_page_config(page_title="Idli Code", layout="centered")
st.title("Idli Code")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:", height=150)
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            re_decrypted = idli_code_to_text(formatted)
            accuracy = calculate_accuracy(user_input, re_decrypted)

            st.subheader("Encrypted Output")
            st.text_area("Idli Code", value=formatted, height=250)
            st.markdown(generate_download_link(formatted, "idli_code.txt"), unsafe_allow_html=True)

            with st.expander("Check encryption accuracy"):
                st.subheader("Re-Decrypted Output")
                st.text_area("Re-Decrypted Text", value=re_decrypted, height=200)
                st.markdown(generate_download_link(re_decrypted, "re_decrypted.txt"), unsafe_allow_html=True)
                if accuracy == 100:
                    st.success("Success: Input and encrypted-decrypted pair matched 100%")
                else:
                    st.error(f"Warning: Only {accuracy:.2f}% of characters matched.")

        else:
            st.warning("Please enter some text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter Idli Code to decrypt:", height=200)
    if st.button("Decrypt"):
        if code_input.strip():
            decrypted = idli_code_to_text(code_input)
            re_encrypted = text_to_idli_code(decrypted)
            formatted_re_encrypted = format_idli_code(re_encrypted)
            accuracy = calculate_accuracy(code_input.replace('\n', '').replace('  ', ' '), re_encrypted)

            st.subheader("Decrypted Output")
            st.text_area("Text", value=decrypted, height=200)
            st.markdown(generate_download_link(decrypted, "decrypted_text.txt"), unsafe_allow_html=True)

            with st.expander("Check decryption accuracy"):
                st.subheader("Re-Encrypted Output")
                st.text_area("Re-Encrypted Idli Code", value=formatted_re_encrypted, height=250)
                st.markdown(generate_download_link(formatted_re_encrypted, "re_encrypted.txt"), unsafe_allow_html=True)
                if accuracy == 100:
                    st.success("Success: Input and re-encrypted-decrypted pair matched 100%")
                else:
                    st.error(f"Warning: Only {accuracy:.2f}% of characters matched.")
        else:
            st.warning("Please enter Idli Code to decrypt.")