import streamlit as st
import textwrap
import re
from typing import List, Dict, Tuple, Optional

# --- Constants --- (Keep as before)
WORD_TO_DIGIT: Dict[str, str] = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
DIGIT_TO_WORD: Dict[str, str] = {v: k for k, v in WORD_TO_DIGIT.items()}
QUATERNARY_TO_BINARY: Dict[str, str] = {'0': '00', '1': '01', '2': '10', '3': '11'}
BINARY_TO_QUATERNARY: Dict[str, str] = {v: k for k, v in QUATERNARY_TO_BINARY.items()}
VALID_WORDS = set(WORD_TO_DIGIT.keys())

# --- Core Logic Functions --- (Keep as before)
def text_to_idli_code_encrypt(text: str) -> str:
    if not text: return ""
    try:
        binary_str = ''.join([format(ord(c), '08b') for c in text])
        binary_chunks: List[str] = textwrap.wrap(binary_str, 2)
        quaternary_digits: List[str] = [BINARY_TO_QUATERNARY.get(chunk, '') for chunk in binary_chunks]
        quaternary_str = ''.join(quaternary_digits)
        words: List[str] = [DIGIT_TO_WORD[d] for d in quaternary_str if d in DIGIT_TO_WORD]
        return ' '.join(words)
    except Exception as e:
        st.error(f"Error during encryption: {e}")
        return "Error during encryption"

def idli_code_to_text_decrypt(code: str) -> Tuple[Optional[str], Optional[List[str]]]:
    if not code: return None, None
    potential_words = [word.strip().title() for word in re.split(r'\s+', code.strip()) if word]
    if not potential_words: return None, None
    quaternary_digits: List[str] = []
    invalid_words: List[str] = []
    for word in potential_words:
        digit = WORD_TO_DIGIT.get(word)
        if digit is not None:
            quaternary_digits.append(digit)
        else:
            original_word = next((w for w in re.split(r'\s+', code.strip()) if w.strip().title() == word), word)
            invalid_words.append(original_word)
    if invalid_words: return None, invalid_words
    quaternary_str = ''.join(quaternary_digits)
    try:
        binary_str = ''.join([QUATERNARY_TO_BINARY[d] for d in quaternary_str])
    except KeyError as e:
        return None, [f"Internal Error: Invalid quaternary digit '{e}'."]
    if len(binary_str) % 8 != 0:
        error_msg = (f"Error: Invalid 'Idli Code' structure. Binary length ({len(binary_str)}) "
                     f"not divisible by 8. Check sequence.")
        return None, [error_msg]
    try:
        byte_chunks = textwrap.wrap(binary_str, 8)
        decoded_chars = [chr(int(b, 2)) for b in byte_chunks]
        decrypted_text = "".join(decoded_chars)
        return decrypted_text, None
    except ValueError:
         return None, ["Error: Problem converting binary data to characters."]
    except Exception as e:
        return None, [f"Error during final decryption: {e}"]

# Use a moderate number of words per line for better density
def format_idli_code_output(code_str: str, words_per_line: int = 8) -> str:
    if not code_str: return ""
    words = code_str.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

# --- Streamlit UI ---
st.set_page_config(
    page_title="Idli Code Converter",
    layout="centered"
)

# --- Header ---
st.title("Idli Code Converter")
st.caption("Encrypt text into 'Idli Code' or decrypt it back.")
# Removed divider here to save space

# --- Operation Selection ---
# Reduced spacing before this section
st.radio(
    "Select Operation:",
    ('Encrypt Text', 'Decrypt Idli Code'),
    horizontal=True,
    key="operation_choice",
    label_visibility="collapsed" # Hide label, title is above
)
# Removed st.write("") spacer

# --- Main Content Area ---

# --- Encrypt ---
if option == 'Encrypt Text':
    # Reduced top margin implicitly by removing spacers above
    with st.container(border=True):
        st.subheader("Encrypt Text → Idli Code")
        # Removed markdown description to save space

        user_input = st.text_area(
            "Text to Encrypt",
            height=100,  # Reduced height
            key="encrypt_input",
            label_visibility="visible",
            placeholder="Type or paste text here..."
        )
        # Removed st.write("") spacer

        encrypt_pressed = st.button("Encrypt Text", key="encrypt_button", type="primary")

        if encrypt_pressed:
            input_text = user_input.strip()
            if input_text:
                with st.spinner("Encrypting..."):
                    encrypted_code = text_to_idli_code_encrypt(input_text)

                # Removed divider here to save space

                if "Error" not in encrypted_code:
                    formatted_code = format_idli_code_output(encrypted_code)

                    st.markdown("##### Encrypted Idli Code:")
                    # --- CHANGE: Use text_area for encrypted output ---
                    st.text_area(
                        "Encrypted Output",
                        value=formatted_code,
                        height=120, # Reduced height
                        key="encrypted_output_area",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    # --- Removed selection tip ---
                    # Removed st.write("") spacer

                    st.download_button(
                        label="Download Encrypted Code (.txt)",
                        data=formatted_code,
                        file_name="encrypted_idli_code.txt",
                        mime="text/plain",
                        key="download_encrypted"
                    )

                    # Verification Expander (kept concise)
                    with st.expander("Verification Details"): # Removed "(Optional)"
                        # Removed caption inside expander
                        re_decrypted_text, errors = idli_code_to_text_decrypt(encrypted_code)
                        if errors:
                            st.error(f"Verification Error: Decryption failed. Details: `{errors}`", icon="⚠️")
                        elif re_decrypted_text is not None:
                            # Use text_area here too for consistency
                            st.text_area("Re-decrypted Verify Area", value=re_decrypted_text, height=80, key="redecrypted_verify", disabled=True, label_visibility="collapsed")
                            if input_text == re_decrypted_text:
                                st.success("Verification Successful.", icon="✅")
                            else:
                                st.error("Verification Failed: Texts differ.", icon="❌")
                                # Comparison kept compact
                                v_col1, v_col2 = st.columns(2)
                                with v_col1: st.caption("Original:"); st.code(input_text, language=None)
                                with v_col2: st.caption("Re-decrypted:"); st.code(re_decrypted_text, language=None)
                        else:
                            st.warning("Verification could not be performed.", icon="ℹ️")
                else: pass
            else: st.warning("Please enter text to encrypt.", icon="⚠️")

# --- Decrypt ---
elif option == 'Decrypt Idli Code':
    with st.container(border=True):
        st.subheader("Decrypt Idli Code → Text")
        # Removed markdown description

        code_input = st.text_area(
            "Idli Code Sequence",
            height=120, # Reduced height
            key="decrypt_input",
            label_visibility="visible",
            placeholder="Paste Idli Code sequence here...",
            help="Sequence of specific words separated by spaces." # Made help shorter
        )
        # Removed st.write("") spacer

        decrypt_pressed = st.button("Decrypt Code", key="decrypt_button", type="primary")

        if decrypt_pressed:
            cleaned_input = code_input.strip()
            if cleaned_input:
                with st.spinner("Decrypting..."):
                    decrypted_text, errors = idli_code_to_text_decrypt(cleaned_input)

                # Removed divider here

                if errors:
                    is_structure_error = any("Invalid 'Idli Code' structure" in str(e) for e in errors)
                    if is_structure_error or any("Problem converting binary" in str(e) for e in errors) or any("Internal Error" in str(e) for e in errors):
                         st.error(f"Decryption Error: {errors[0]}", icon="⚠️")
                    else:
                         st.error(f"Invalid Input: Found non-code words: `{', '.join(errors)}`", icon="⚠️")
                         # Removed extra caption
                elif decrypted_text is not None:
                    st.markdown("##### Decrypted Text:")
                    # --- Use text_area for decrypted output (already was) ---
                    st.text_area(
                        "Decrypted Output",
                        value=decrypted_text,
                        height=120, # Reduced height
                        key="decrypted_output_area",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    # --- Removed selection tip ---
                    # Removed st.write("") spacer

                    st.download_button(
                        label="Download Decrypted Text (.txt)",
                        data=decrypted_text,
                        file_name="decrypted_text.txt",
                        mime="text/plain",
                        key="download_decrypted"
                    )

                    # Verification Expander (kept concise)
                    with st.expander("Verification Details"):
                        # Removed caption inside expander
                        re_encrypted_code = text_to_idli_code_encrypt(decrypted_text)
                        original_valid_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                        standardized_original_code = ' '.join(original_valid_words)
                        if "Error" in re_encrypted_code:
                            st.error(f"Verification Error: Re-encryption failed. Details: `{re_encrypted_code}`", icon="⚠️")
                        else:
                            formatted_reencrypted = format_idli_code_output(re_encrypted_code)
                            # Use text_area here too
                            st.text_area("Re-encrypted Verify Area", value=formatted_reencrypted, height=80, key="reencrypted_verify", disabled=True, label_visibility="collapsed")
                            if standardized_original_code == re_encrypted_code:
                                st.success("Verification Successful.", icon="✅")
                            else:
                                st.error("Verification Failed: Codes differ.", icon="❌")
                                st.caption("Mismatch may be due to invalid words/formatting in input.") # Shorter caption
                                v_col1, v_col2 = st.columns(2)
                                with v_col1: st.caption("Input (Valid):"); st.code(standardized_original_code, language=None)
                                with v_col2: st.caption("Re-encrypted:"); st.code(re_encrypted_code, language=None)
                elif decrypted_text is None and not errors:
                     st.warning("Input empty or no valid words.", icon="ℹ️") # Shorter message
            else:
                st.warning("Please enter 'Idli Code' to decrypt.", icon="⚠️")

# --- Footer ---
# Removed divider
st.caption("Idli Code Converter") # Keep footer minimal