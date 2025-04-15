import streamlit as st import textwrap import base64 from io import BytesIO

--- Encoding dictionaries ---

word_to_digit = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'} digit_to_word = {v: k for k, v in word_to_digit.items()} quaternary_to_binary = {'0': '00', '1': '01', '2': '10', '3': '11'} binary_to_quaternary = {v: k for k, v in quaternary_to_binary.items()}

--- Core functions ---

def text_to_idli_code(text): try: binary_str = ''.join([format(ord(c), '08b') for c in text]) chunks = textwrap.wrap(binary_str, 2) quaternary = ''.join([binary_to_quaternary.get(chunk, '') for chunk in chunks]) words = [digit_to_word[d] for d in quaternary if d in digit_to_word] return ' '.join(words) except Exception as e: return f"Encryption error: {str(e)}"

def idli_code_to_text(code): try: code_words = code.strip().split() filtered_words = [w for w in code_words if w in word_to_digit] if len(filtered_words) != len(code_words): invalid_words = [w for w in code_words if w not in word_to_digit] raise ValueError(f"Invalid words found: {', '.join(invalid_words)}") quaternary = ''.join([word_to_digit[word] for word in filtered_words]) binary = ''.join([quaternary_to_binary[d] for d in quaternary]) bytes_ = textwrap.wrap(binary, 8) decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8]) return decoded except Exception as e: return f"Decryption error: {str(e)}"

def format_idli_code(code_str): words = code_str.split() lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)] return '\n'.join(lines)

def calculate_accuracy(original, converted): match = sum(o == c for o, c in zip(original, converted)) total = max(len(original), 1) return round((match / total) * 100, 2)

def generate_download_link(content, filename): b64 = base64.b64encode(content.encode()).decode() return f'<a style="color:#4CAF50;font-weight:600;text-decoration:none;" href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'

--- Streamlit UI ---

st.set_page_config(page_title="Idli Code Encryptor", layout="centered") st.markdown(""" <style> .main { background-color: #f9f9f9; padding: 20px; border-radius: 10px; } .stTextArea textarea { font-family: 'Courier New', monospace; font-size: 14px; } </style> """, unsafe_allow_html=True)

st.title("Idli Code Encryptor & Decryptor") st.caption("Encode and decode messages using the 4 secret ingredients: Idli, Dosa, Sambar, and Chutney.")

option = st.radio("Select Mode:", ['Encrypt', 'Decrypt'], horizontal=True) st.markdown("---")

if option == 'Encrypt': user_input = st.text_area("Enter text to encrypt:") if st.button("Encrypt"): if user_input.strip(): encrypted = text_to_idli_code(user_input) formatted = format_idli_code(encrypted) re_decrypted = idli_code_to_text(formatted) accuracy = calculate_accuracy(user_input, re_decrypted)

st.subheader("Encrypted Idli Code")
        st.code(formatted, language='text')
        st.markdown(generate_download_link(formatted, "idli_code.txt"), unsafe_allow_html=True)

        st.subheader("Re-Decrypted Text")
        st.code(re_decrypted, language='text')
        st.markdown(generate_download_link(re_decrypted, "redecrypted_text.txt"), unsafe_allow_html=True)

        if accuracy == 100:
            st.success("Success: input and encrypted-decrypted pair matched 100%")
        else:
            st.error(f"Error: {100 - accuracy}% mismatch between input and re-decrypted output")
    else:
        st.warning("Please enter text to encrypt.")

elif option == 'Decrypt': code_input = st.text_area("Enter your Idli Code (space-separated):") if st.button("Decrypt"): if code_input.strip(): decrypted = idli_code_to_text(code_input) re_encrypted = text_to_idli_code(decrypted) formatted_re_encrypted = format_idli_code(re_encrypted) accuracy = calculate_accuracy(code_input.replace("\n", "").strip(), formatted_re_encrypted.replace("\n", "").strip())

st.subheader("Decrypted Text")
        st.code(decrypted, language='text')
        st.markdown(generate_download_link(decrypted, "decrypted_text.txt"), unsafe_allow_html=True)

        st.subheader("Re-Encrypted Idli Code")
        st.code(formatted_re_encrypted, language='text')
        st.markdown(generate_download_link(formatted_re_encrypted, "reencrypted_code.txt"), unsafe_allow_html=True)

        if "error" not in decrypted.lower():
            if accuracy == 100:
                st.success("Success: decrypted text and re-encrypted pair matched 100%")
            else:
                st.error(f"Error: {100 - accuracy}% mismatch between decrypted and re-encrypted")
        else:
            st.error(decrypted)
    else:
        st.warning("Please enter Idli Code to decrypt.")

