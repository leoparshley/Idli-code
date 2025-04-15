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

def format_idli_code_output(code_str: str, words_per_line: int = 10) -> str:
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
st.caption("Encrypt text into a special 'Idli Code' format or decrypt it back.")
st.write("---")

# --- Operation Selection ---
st.markdown("##### Select Operation")
option = st.radio(
    "Select Operation:",
    ('Encrypt Text', 'Decrypt Idli Code'),
    horizontal=True,
    key="operation_choice",
    label_visibility="collapsed"
)
st.write("")

# --- Main Content Area ---

# --- Encrypt ---
if option == 'Encrypt Text':
    with st.container(border=True):
        st.subheader("Encrypt Text → Idli Code")
        st.markdown("Enter text below to convert it into 'Idli Code'.")

        user_input = st.text_area(
            "Text to Encrypt",
            height=140,
            key="encrypt_input",
            label_visibility="visible",
            placeholder="Type or paste text here..."
        )
        st.write("")

        encrypt_pressed = st.button("Encrypt Text", key="encrypt_button", type="primary")

        if encrypt_pressed:
            input_text = user_input.strip()
            if input_text:
                with st.spinner("Encrypting..."):
                    encrypted_code = text_to_idli_code_encrypt(input_text)

                st.markdown("---")

                if "Error" not in encrypted_code:
                    formatted_code = format_idli_code_output(encrypted_code)

                    st.markdown("##### Encrypted Idli Code:")
                    # --- CHANGE HERE: Use st.code for encrypted output ---
                    st.code(formatted_code, language=None, line_numbers=False)
                    # ------------------------------------------------------
                    st.write("")

                    st.download_button(
                        label="Download Encrypted Code (.txt)",
                        data=formatted_code,
                        file_name="encrypted_idli_code.txt",
                        mime="text/plain",
                        key="download_encrypted"
                    )

                    # --- Verification Expander ---
                    with st.expander("Verification Details (Optional)"):
                        st.caption("_The encrypted code was automatically decrypted back to check consistency._")
                        re_decrypted_text, errors = idli_code_to_text_decrypt(encrypted_code)
                        if errors:
                            st.error(f"Verification Error: Could not decrypt the generated code. Details: `{errors}`")
                        elif re_decrypted_text is not None:
                            st.caption("**Text After Round-Trip:**")
                            # Use disabled text area for verification output (plain text)
                            st.text_area("Re-decrypted Text Area Verify", value=re_decrypted_text, height=100, key="redecrypted_verify", disabled=True, label_visibility="collapsed")
                            if input_text == re_decrypted_text:
                                st.success("Verification Successful: Original and re-decrypted text match.")
                            else:
                                st.error("Verification Failed: Original and re-decrypted text differ.")
                                v_col1, v_col2 = st.columns(2)
                                with v_col1: st.caption("Original:"); st.code(input_text, language=None)
                                with v_col2: st.caption("Re-decrypted:"); st.code(re_decrypted_text, language=None)
                        else:
                            st.warning("Verification could not be performed (decryption failed).")
                else:
                    pass # Error already shown
            else:
                st.warning("Please enter text to encrypt.")

# --- Decrypt ---
elif option == 'Decrypt Idli Code':
    with st.container(border=True):
        st.subheader("Decrypt Idli Code → Text")
        st.markdown("Enter an 'Idli Code' sequence to convert it back to text.")

        code_input = st.text_area(
            "Idli Code Sequence",
            height=160,
            key="decrypt_input",
            label_visibility="visible",
            placeholder="Paste Idli Code sequence here...",
            help="The code should be a sequence of specific words separated by spaces."
        )
        st.write("")

        decrypt_pressed = st.button("Decrypt Code", key="decrypt_button", type="primary")

        if decrypt_pressed:
            cleaned_input = code_input.strip()
            if cleaned_input:
                with st.spinner("Decrypting..."):
                    decrypted_text, errors = idli_code_to_text_decrypt(cleaned_input)

                st.markdown("---")

                if errors:
                    is_structure_error = any("Invalid 'Idli Code' structure" in str(e) for e in errors)
                    is_conversion_error = any("Problem converting binary" in str(e) for e in errors)
                    is_internal_error = any("Internal Error" in str(e) for e in errors)
                    if is_structure_error or is_conversion_error or is_internal_error:
                         st.error(f"Decryption Error: {errors[0]}")
                    else:
                         st.error(f"Invalid Input: Found words not part of the 'Idli Code' format: `{', '.join(errors)}`")
                         st.caption("Please ensure the input contains only the allowed code words.")
                elif decrypted_text is not None:
                    st.markdown("##### Decrypted Text:")
                    # --- KEEP USING st.text_area for decrypted output ---
                    st.text_area("Decrypted Text Area Output", value=decrypted_text, height=140, key="decrypted_output", disabled=True, label_visibility="collapsed")
                    # -----------------------------------------------------
                    st.write("")

                    st.download_button(
                        label="Download Decrypted Text (.txt)",
                        data=decrypted_text,
                        file_name="decrypted_text.txt",
                        mime="text/plain",
                        key="download_decrypted"
                    )

                    # --- Verification Expander ---
                    with st.expander("Verification Details (Optional)"):
                        st.caption("_The decrypted text was re-encrypted to check consistency with the input code._")
                        re_encrypted_code = text_to_idli_code_encrypt(decrypted_text)
                        original_valid_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                        standardized_original_code = ' '.join(original_valid_words)
                        if "Error" in re_encrypted_code:
                            st.error(f"Verification Error: Could not re-encrypt the result. Details: `{re_encrypted_code}`")
                        else:
                            st.caption("**Re-encrypted Code (from decrypted text):**")
                            # Use st.code for verification output (Idli code)
                            formatted_reencrypted = format_idli_code_output(re_encrypted_code)
                            st.code(formatted_reencrypted, language=None, line_numbers=False) # Consistent with main encrypted output
                            if standardized_original_code == re_encrypted_code:
                                st.success("Verification Successful: Input code matches re-encrypted text.")
                            else:
                                st.error("Verification Failed: Input code differs from re-encrypted text.")
                                st.caption("Mismatch may be due to invalid words/formatting in original input.")
                                v_col1, v_col2 = st.columns(2)
                                with v_col1: st.caption("Standardized Input:"); st.code(standardized_original_code, language=None)
                                with v_col2: st.caption("Re-encrypted:"); st.code(re_encrypted_code, language=None)
                elif decrypted_text is None and not errors:
                     st.warning("Input is empty or contains no valid 'Idli Code' words.")
            else:
                st.warning("Please enter 'Idli Code' to decrypt.")

# --- Footer ---
st.write("---")
st.caption("Idli Code Converter")