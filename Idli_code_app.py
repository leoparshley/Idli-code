import streamlit as st
import textwrap
import base64

# --- Mappings ---
word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
digit_to_word = {v: k for k, v in word_to_digit.items()}
quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'}
binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

# --- Utilities ---
def generate_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download</a>'

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

def text_to_idli_code(text):
    try:
        binary_str = ''.join([format(ord(c), '08b') for c in text])
        chunks = textwrap.wrap(binary_str, 2)
        quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks])
        words = [digit_to_word[d] for d in quaternary if d in digit_to_word]
        return ' '.join(words)
    except Exception:
        return None

def idli_code_to_text(code):
    try:
        code_words = [w.strip() for w in code.strip().split() if w.strip()]
        if not all(word in word_to_digit for word in code_words):
            return None, "Invalid word detected. Only specific vocabulary is accepted."
        quaternary = ''.join([word_to_digit[word] for word in code_words])
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8])
        return decoded, None
    except Exception as e:
        return None, str(e)

def compute_accuracy(original, result):
    if not original or not result:
        return 0
    match_count = sum(1 for a, b in zip(original, result) if a == b)
    return round((match_count / len(original)) * 100, 2) if original else 0

# --- Streamlit Config ---
st.set_page_config(page_title="Idli Code Translator", layout="centered")
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    textarea {
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    .download-btn {
        margin-top: -10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Idli Code Translator")
option = st.radio("Select mode", ["Encrypt", "Decrypt"], horizontal=True)

# --- Encryption ---
if option == "Encrypt":
    user_input = st.text_area("Enter text to encrypt:", height=150)
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            decrypted, _ = idli_code_to_text(encrypted)
            accuracy = compute_accuracy(user_input, decrypted)

            st.subheader("Encrypted Output")
            st.text_area("Encrypted Code:", value=formatted, height=200, label_visibility="collapsed")
            st.markdown(generate_download_link(formatted, "encrypted_idli_code.txt"), unsafe_allow_html=True)

            with st.expander("Check Accuracy"):
                st.subheader("Re-Decrypted Text")
                st.text_area("Decrypted from Code:", value=decrypted, height=150, label_visibility="collapsed")
                st.markdown(generate_download_link(decrypted, "re_decrypted_output.txt"), unsafe_allow_html=True)

                if user_input == decrypted:
                    st.success("Success: input and encrypted-decrypted pair matched 100%")
                else:
                    st.warning(f"Match Accuracy: {accuracy}%")

        else:
            st.warning("Please enter text to encrypt.")

# --- Decryption ---
elif option == "Decrypt":
    code_input = st.text_area("Enter code to decrypt:", height=150)
    if st.button("Decrypt"):
        if code_input.strip():
            decrypted, error = idli_code_to_text(code_input)
            if decrypted:
                re_encrypted = text_to_idli_code(decrypted)
                formatted = format_idli_code(re_encrypted)
                acc = compute_accuracy(code_input.replace('\n', ' ').strip(), re_encrypted.strip())

                st.subheader("Decrypted Text")
                st.text_area("Plain Text:", value=decrypted, height=150, label_visibility="collapsed")
                st.markdown(generate_download_link(decrypted, "decrypted_output.txt"), unsafe_allow_html=True)

                with st.expander("Check Accuracy"):
                    st.subheader("Re-Encrypted Code")
                    st.text_area("From Decrypted Text:", value=formatted, height=200, label_visibility="collapsed")
                    st.markdown(generate_download_link(formatted, "re_encrypted_idli_code.txt"), unsafe_allow_html=True)

                    if acc == 100:
                        st.success("Success: input and encrypted-decrypted pair matched 100%")
                    else:
                        st.warning(f"Match Accuracy: {acc}%")
            else:
                st.error(f"Decryption Error: {error}")
        else:
            st.warning("Please enter code to decrypt.")