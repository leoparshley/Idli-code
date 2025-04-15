import streamlit as st
import textwrap
import base64

# Encoding dictionaries
word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
digit_to_word = {v: k for k, v in word_to_digit.items()}
quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'}
binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

# Helper: Download link generator
def generate_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download</a>'

# Helper: Format Idli code with 10 words per line
def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

# Encryption function
def text_to_idli_code(text):
    try:
        binary_str = ''.join([format(ord(c), '08b') for c in text])
        chunks = textwrap.wrap(binary_str, 2)
        quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks])
        words = [digit_to_word[d] for d in quaternary if d in digit_to_word]
        return ' '.join(words)
    except Exception:
        return None

# Decryption function
def idli_code_to_text(code):
    try:
        code_words = code.strip().split()
        code_words = [w.strip() for w in code_words if w.strip()]
        if not all(word in word_to_digit for word in code_words):
            return None, "Invalid word detected. Use only Idli, Dosa, Sambar, Chutney."
        quaternary = ''.join([word_to_digit[word] for word in code_words])
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8])
        return decoded, None
    except Exception as e:
        return None, str(e)

# Accuracy checker
def compute_accuracy(original, result):
    if not original or not result:
        return 0
    match_count = sum(1 for a, b in zip(original, result) if a == b)
    return round((match_count / len(original)) * 100, 2) if original else 0

# --- Streamlit UI ---
st.set_page_config(page_title="Idli Code App", layout="centered")
st.title("Idli Code Encryptor & Decryptor")
st.markdown("Encrypt any message using only four words: **Idli**, **Dosa**, **Sambar**, **Chutney**")

option = st.radio("Choose an option:", ["Encrypt", "Decrypt"])

# --- Encrypt UI ---
if option == "Encrypt":
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            decrypted, _ = idli_code_to_text(encrypted)
            accuracy = compute_accuracy(user_input, decrypted)

            st.subheader("Encrypted Idli Code")
            st.text_area("Idli Code:", value=formatted, height=200)
            st.markdown(generate_download_link(formatted, "encrypted_idli_code.txt"), unsafe_allow_html=True)

            st.subheader("Re-Decrypted Output")
            st.text_area("Decrypted Text:", value=decrypted, height=150)
            st.markdown(generate_download_link(decrypted, "re_decrypted_output.txt"), unsafe_allow_html=True)

            if user_input == decrypted:
                st.success("Success: input and encrypted-decrypted pair matched 100%")
            else:
                st.warning(f"Warning: Match Accuracy = {accuracy}%")
        else:
            st.warning("Please enter text to encrypt.")

# --- Decrypt UI ---
elif option == "Decrypt":
    code_input = st.text_area("Enter space-separated Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip():
            decrypted, error = idli_code_to_text(code_input)
            if decrypted:
                re_encrypted = text_to_idli_code(decrypted)
                formatted = format_idli_code(re_encrypted)
                acc = compute_accuracy(code_input.replace('\n', ' ').strip(), re_encrypted.strip())

                st.subheader("Decrypted Text")
                st.text_area("Plain Text:", value=decrypted, height=150)
                st.markdown(generate_download_link(decrypted, "decrypted_output.txt"), unsafe_allow_html=True)

                st.subheader("Re-Encrypted Idli Code")
                st.text_area("Re-Encrypted:", value=formatted, height=200)
                st.markdown(generate_download_link(formatted, "re_encrypted_idli_code.txt"), unsafe_allow_html=True)

                if acc == 100:
                    st.success("Success: input and encrypted-decrypted pair matched 100%")
                else:
                    st.warning(f"Warning: Match Accuracy = {acc}%")
            else:
                st.error(f"Decryption Error: {error}")
        else:
            st.warning("Please enter Idli Code to decrypt.")