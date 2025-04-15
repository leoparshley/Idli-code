import streamlit as st
import textwrap
import base64

# Encoding dictionary
word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
digit_to_word = {v: k for k, v in word_to_digit.items()}
quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'}
binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

def text_to_idli_code(text):
    try:
        binary_str = ''.join([format(ord(c), '08b') for c in text])
        chunks = textwrap.wrap(binary_str, 2)
        quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks])
        words = [digit_to_word[d] for d in quaternary if d in digit_to_word]
        return ' '.join(words)
    except Exception as e:
        return f"Encryption error: {str(e)}"

def idli_code_to_text(code):
    try:
        code_words = code.strip().split()
        quaternary = ''.join([word_to_digit[word] for word in code_words if word in word_to_digit])
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8])
        return decoded
    except Exception as e:
        return f"Decryption error: {str(e)}"

def generate_download_link(content, filename):
    try:
        b64 = base64.b64encode(content.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    except Exception as e:
        return f"Download link error: {str(e)}"

def compute_accuracy(original, result):
    original = ''.join(original.strip().split())
    result = ''.join(result.strip().split())
    matches = sum(1 for a, b in zip(original, result) if a == b)
    total = max(len(original), len(result))
    return round((matches / total) * 100, 2) if total > 0 else 0

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

st.set_page_config(page_title="Idli Code", layout="wide")
st.markdown("<h1 style='text-align: center;'>Idli Code</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])

with tab1:
    st.subheader("Enter text to encrypt:")
    user_input = st.text_area("Text input:", key="enc_input")

    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            re_decrypted = idli_code_to_text(formatted)
            accuracy = compute_accuracy(user_input, re_decrypted)

            st.text_area("Encrypted Output:", value=formatted, height=250)
            st.markdown(generate_download_link(formatted, "encrypted_idli_code.txt"), unsafe_allow_html=True)

            with st.expander("Check accuracy"):
                st.text_area("Re-Decrypted Output:", value=re_decrypted, height=150)
                if accuracy == 100:
                    st.success("Success: input and encrypted-decrypted pair matched 100%")
                else:
                    st.error(f"Warning: Only {accuracy}% match between input and encrypted-decrypted pair")
        else:
            st.warning("Please enter some text to encrypt.")

with tab2:
    st.subheader("Enter your Idli Code to decrypt:")
    code_input = st.text_area("Idli Code input:", key="dec_input")

    if st.button("Decrypt"):
        if code_input.strip():
            decrypted = idli_code_to_text(code_input)
            re_encrypted = text_to_idli_code(decrypted)
            formatted = format_idli_code(re_encrypted)
            accuracy = compute_accuracy(' '.join(code_input.split()), ' '.join(formatted.split()))

            st.text_area("Decrypted Output:", value=decrypted, height=200)
            st.markdown(generate_download_link(decrypted, "decrypted_text.txt"), unsafe_allow_html=True)

            with st.expander("Check accuracy"):
                st.text_area("Re-Encrypted Output:", value=formatted, height=150)
                if accuracy == 100:
                    st.success("Success: original and decrypted-re-encrypted pair matched 100%")
                else:
                    st.error(f"Warning: Only {accuracy}% match between original and decrypted-re-encrypted pair")
        else:
            st.warning("Please enter the Idli Code to decrypt.")