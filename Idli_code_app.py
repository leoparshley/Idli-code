import streamlit as st
import textwrap
import re
from typing import List, Dict, Tuple, Optional

# --- Constants ---
WORD_TO_DIGIT = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
DIGIT_TO_WORD = {v: k for k, v in WORD_TO_DIGIT.items()}
QUATERNARY_TO_BINARY = {'0': '00', '1': '01', '2': '10', '3': '11'}
BINARY_TO_QUATERNARY = {v: k for k, v in QUATERNARY_TO_BINARY.items()}
VALID_WORDS = set(WORD_TO_DIGIT.keys())

# --- Core Logic ---
def text_to_idli_code_encrypt(text: str) -> str:
    if not text: return ""
    try:
        binary_str = "".join(map(lambda c: f"{ord(c):08b}", text))
        binary_chunks = textwrap.wrap(binary_str, 2)
        quaternary_digits = [BINARY_TO_QUATERNARY.get(chunk, '') for chunk in binary_chunks]
        words = [DIGIT_TO_WORD[d] for d in quaternary_digits if d in DIGIT_TO_WORD]
        return " ".join(words)
    except Exception as e:
        st.error(f"Error during encryption: {e}")
        return "Error during encryption"

def idli_code_to_text_decrypt(code: str) -> Tuple[Optional[str], Optional[List[str]]]:
    if not code: return None, None
    potential_words = [word.strip().title() for word in re.split(r'\s+', code.strip()) if word]
    if not potential_words: return None, None
    quaternary_digits = []
    invalid_words = []
    for word in potential_words:
        digit = WORD_TO_DIGIT.get(word)
        if digit is not None:
            quaternary_digits.append(digit)
        else:
            invalid_words.append(word)
    if invalid_words: return None, invalid_words
    quaternary_str = "".join(quaternary_digits)
    try:
        binary_str = "".join([QUATERNARY_TO_BINARY[d] for d in quaternary_str])
    except KeyError as e:
        return None, [f"Internal Error: Invalid quaternary digit '{str(e)}'."]
    if len(binary_str) % 8 != 0:
        return None, ["Invalid Idli Code structure. Check sequence."]
    try:
        decoded_text = "".join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
        return decoded_text, None
    except ValueError:
        return None, ["Error converting binary to characters."]

# --- Streamlit UI ---
st.set_page_config(page_title="Idli Code Converter", layout="centered")

st.title("Idli Code Converter")
st.caption("Encrypt text into 'Idli Code' or decrypt it back.")

option = st.radio(
    "Select Operation:",
    ('Encrypt Text', 'Decrypt Idli Code'),
    horizontal=True,
    key="operation_choice",
    label_visibility="collapsed"
)

if option == 'Encrypt Text':
    with st.container():
        st.subheader