import streamlit as st
import textwrap
import base64

# Encoding maps
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
    code_words = code.strip().split()
    errors = []
    valid_digits = []

    for i, word in enumerate(code_words):
        if word not in word_to_digit:
            errors.append(f"Line ~{(i // 10) + 1}: Invalid word '{word}'")
        else:
            valid_digits.append(word_to_digit[word])

    quaternary = ''.join(valid_digits)

    try:
        binary = ''.join([quaternary_to_binary[d] for d in quaternary])
        # Truncate to 8-bit blocks
        binary = binary[:len(binary) - (len(binary) % 8)]
        bytes_ = textwrap.wrap(binary, 8)
        decoded = ''.join([chr(int(b, 2)) for b in bytes_ if len(b) == 8 and int(b, 2) < 256])
        return decoded, errors
    except Exception:
        return "[Decryption error: malformed input]", ["Decryption failed due to corrupt code."]

def format_idli_code(code_str):
    words = code_str.split()
    lines = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return '\n'.join(lines)

def compare_accuracy(original, result):
    matches = sum(1 for o, r in zip(original, result) if o == r)
    total = len(original)
    accuracy = (matches / total * 100) if total > 0 else 0
    return round(accuracy, 2)

def generate_download_link(data, filename):
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'

# Streamlit UI
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option:", ['Encrypt', 'Decrypt'])

if option == 'Encrypt':
    user_input = st.text_area("Enter text to encrypt:")
    if st.button("Encrypt"):
        if user_input.strip():
            encrypted = text_to_idli_code(user_input)
            formatted = format_idli_code(encrypted)
            re_decrypted, _ = idli_code_to_text(encrypted)
            accuracy = compare_accuracy(user_input, re_decrypted)

            st.text_area("Encrypted Idli Code:", value=formatted, height=300)
            st.text_area("Re-Decrypted Encrypt Output:", value=re_decrypted, height=200)
            if accuracy == 100:
                st.success("Success: input and re-decrypted encrypt matched 100%")
            else:
                st.error(f"Error: {100 - accuracy}% mismatch between input and encrypted-decrypted pair")

            st.markdown(generate_download_link(formatted, "idli_code.txt"), unsafe_allow_html=True)
            st.markdown(generate_download_link(re_decrypted, "redecrypted_output.txt"), unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to encrypt.")

elif option == 'Decrypt':
    code_input = st.text_area("Enter your Idli Code:")
    if st.button("Decrypt"):
        if code_input.strip():
            decrypted, error_list = idli_code_to_text(code_input)
            re_encrypted = text_to_idli_code(decrypted)
            formatted_re_enc = format_idli_code(re_encrypted)
            re_decrypted, _ = idli_code_to_text(re_encrypted)
            accuracy = compare_accuracy(decrypted, re_decrypted)

            st.text_area("Decrypted Text:", value=decrypted, height=200)
            st.text_area("Re-Decrypted Encrypt Output:", value=re_decrypted, height=200)
            if accuracy == 100:
                st.success("Success: decrypted text and re-decrypted encrypt matched 100%")
            else:
                st.error(f"Error: {100 - accuracy}% mismatch in round-trip decryption")

            if error_list:
                st.warning("Issues found:\n" + "\n".join(error_list))

            st.markdown(generate_download_link(decrypted, "decrypted_text.txt"), unsafe_allow_html=True)
            st.markdown(generate_download_link(re_decrypted, "redecrypted_output.txt"), unsafe_allow_html=True)
        else:
            st.warning("Please enter Idli Code to decrypt.")