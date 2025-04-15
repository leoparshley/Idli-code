import streamlit as st
import textwrap
import re
from typing import List, Dict, Tuple, Optional

# --- Constants --- (Keep as before - essential for logic)
WORD_TO_DIGIT: Dict[str, str] = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
DIGIT_TO_WORD: Dict[str, str] = {v: k for k, v in WORD_TO_DIGIT.items()}
QUATERNARY_TO_BINARY: Dict[str, str] = {'0': '00', '1': '01', '2': '10', '3': '11'}
BINARY_TO_QUATERNARY: Dict[str, str] = {v: k for k, v in QUATERNARY_TO_BINARY.items()}
VALID_WORDS = set(WORD_TO_DIGIT.keys())

# --- Core Logic Functions --- (Keep as before - functional logic is sound)
# Renaming functions slightly for consistency with UI, although not strictly necessary
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
    # Prepare potential words, check validity against the known set
    potential_words = [word.strip().title() for word in re.split(r'\s+', code.strip()) if word]
    if not potential_words: return None, None

    quaternary_digits: List[str] = []
    invalid_words: List[str] = []
    valid_input_words_standardized = [] # Keep track of the valid part of input

    for word in potential_words:
        digit = WORD_TO_DIGIT.get(word)
        if digit is not None:
            quaternary_digits.append(digit)
            valid_input_words_standardized.append(word) # Add the title-cased valid word
        else:
            # Find original casing if possible for better error message
            original_word = next((w for w in re.split(r'\s+', code.strip()) if w.strip().title() == word), word)
            invalid_words.append(original_word)

    if invalid_words:
        # Return the list of invalid words found
        return None, invalid_words

    quaternary_str = ''.join(quaternary_digits)
    try:
        binary_str = ''.join([QUATERNARY_TO_BINARY[d] for d in quaternary_str])
    except KeyError as e:
        # This indicates an internal logic error if WORD_TO_DIGIT keys are valid
        return None, [f"Internal Error: Invalid quaternary digit '{e}'."]
    if len(binary_str) % 8 != 0:
        error_msg = (f"Error: Invalid 'Idli Code' structure. The sequence length results "
                     f"in a binary string ({len(binary_str)} bits) not divisible by 8. "
                     f"Check if the code sequence is complete or corrupted.")
        return None, [error_msg]
    try:
        byte_chunks = textwrap.wrap(binary_str, 8)
        decoded_chars = [chr(int(b, 2)) for b in byte_chunks]
        decrypted_text = "".join(decoded_chars)
        # Also return the standardized valid input for comparison later if needed
        # For simplicity in the main UI, we might recalculate it there, but could return it
        # return decrypted_text, None # Original return on success
        return decrypted_text, None # Return None for errors list on success
    except ValueError:
         return None, ["Error: Problem converting binary data to characters. Input might be corrupted."]
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
    # page_icon="🍲", # Removed emoji
    layout="centered"
)

# --- Header ---
st.title("Idli Code Converter")
st.caption("Encrypt text into a special 'Idli Code' format or decrypt it back.") # Obscured words
st.write("---")

# --- Operation Selection ---
st.markdown("##### Select Operation")
option = st.radio(
    "Select Operation:",
    ('Encrypt Text', 'Decrypt Idli Code'), # Changed terminology, removed emojis
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
        st.markdown("Enter text below to convert it into 'Idli Code'.") # Changed terminology

        user_input = st.text_area(
            "Text to Encrypt", # Changed terminology
            height=140,
            key="encrypt_input",
            label_visibility="visible",
            placeholder="Type or paste text here..."
        )
        st.write("")

        encrypt_pressed = st.button("Encrypt Text", key="encrypt_button", type="primary") # Changed terminology

        if encrypt_pressed:
            input_text = user_input.strip()
            if input_text:
                with st.spinner("Encrypting..."): # Changed terminology
                    encrypted_code = text_to_idli_code_encrypt(input_text) # Use renamed function

                st.markdown("---")

                if "Error" not in encrypted_code:
                    formatted_code = format_idli_code_output(encrypted_code)

                    st.markdown("##### Encrypted Idli Code:") # Changed terminology
                    st.code(formatted_code, language=None)
                    st.write("")

                    st.download_button(
                        label="Download Encrypted Code (.txt)", # Changed terminology
                        data=formatted_code,
                        file_name="encrypted_idli_code.txt",
                        mime="text/plain",
                        key="download_encrypted"
                    )

                    # --- Verification Expander ---
                    with st.expander("Verification Details (Optional)"):
                        st.caption("_The encrypted code was automatically decrypted back to check consistency._") # Changed terminology
                        # Use decrypt function here
                        re_decrypted_text, errors = idli_code_to_text_decrypt(encrypted_code)
                        if errors:
                            st.error(f"Verification Error: Could not decrypt the generated code. Details: `{errors}`") # Changed terminology
                        elif re_decrypted_text is not None:
                            st.caption("**Text After Round-Trip:**")
                            st.text_area("Re-decrypted Text Area", value=re_decrypted_text, height=100, key="redecrypted_verify", disabled=True, label_visibility="collapsed") # Changed terminology
                            if input_text == re_decrypted_text:
                                st.success("Verification Successful: Original and re-decrypted text match.") # Changed terminology
                            else:
                                st.error("Verification Failed: Original and re-decrypted text differ.") # Changed terminology
                                v_col1, v_col2 = st.columns(2)
                                with v_col1:
                                    st.caption("Original:")
                                    st.code(input_text, language=None)
                                with v_col2:
                                    st.caption("Re-decrypted:") # Changed terminology
                                    st.code(re_decrypted_text, language=None)
                        else:
                            st.warning("Verification could not be performed (decryption failed).") # Changed terminology

                else:
                    # Error is displayed by the function call using st.error
                    pass
            else:
                st.warning("Please enter text to encrypt.") # Changed terminology

# --- Decrypt ---
elif option == 'Decrypt Idli Code':
    with st.container(border=True):
        st.subheader("Decrypt Idli Code → Text") # Changed terminology
        st.markdown("Enter an 'Idli Code' sequence to convert it back to text.") # Changed terminology

        code_input = st.text_area(
            "Idli Code Sequence",
            height=160,
            key="decrypt_input",
            label_visibility="visible",
            placeholder="Paste Idli Code sequence here...", # Removed specific word examples
            help="The code should be a sequence of specific words separated by spaces." # Generic help text
        )
        st.write("")

        decrypt_pressed = st.button("Decrypt Code", key="decrypt_button", type="primary") # Changed terminology

        if decrypt_pressed:
            cleaned_input = code_input.strip()
            if cleaned_input:
                with st.spinner("Decrypting..."): # Changed terminology
                    decrypted_text, errors = idli_code_to_text_decrypt(cleaned_input) # Use renamed function

                st.markdown("---")

                if errors:
                    # Error handling: Check if it's an invalid word list vs. a structural error message
                    is_structure_error = any("Invalid 'Idli Code' structure" in str(e) for e in errors)
                    is_conversion_error = any("Problem converting binary" in str(e) for e in errors)
                    is_internal_error = any("Internal Error" in str(e) for e in errors)

                    if is_structure_error or is_conversion_error or is_internal_error:
                         # Display specific structural/conversion error messages
                         st.error(f"Decryption Error: {errors[0]}") # Changed terminology
                    else:
                         # Assume 'errors' is a list of invalid words found in the input
                         st.error(f"Invalid Input: Found words not part of the 'Idli Code' format: `{', '.join(errors)}`")
                         st.caption("Please ensure the input contains only the allowed code words.") # Generic hint

                elif decrypted_text is not None:
                    st.markdown("##### Decrypted Text:") # Changed terminology
                    st.text_area("Decrypted Text Area", value=decrypted_text, height=140, key="decrypted_output", disabled=True, label_visibility="collapsed") # Changed terminology
                    st.write("")

                    st.download_button(
                        label="Download Decrypted Text (.txt)", # Changed terminology
                        data=decrypted_text,
                        file_name="decrypted_text.txt",
                        mime="text/plain",
                        key="download_decrypted"
                    )

                    # --- Verification Expander ---
                    with st.expander("Verification Details (Optional)"):
                        st.caption("_The decrypted text was re-encrypted to check consistency with the input code._") # Changed terminology
                        # Re-encrypt the result
                        re_encrypted_code = text_to_idli_code_encrypt(decrypted_text) # Use renamed function

                        # Get the standardized *valid* words from the original input for comparison
                        original_valid_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                        standardized_original_code = ' '.join(original_valid_words)

                        if "Error" in re_encrypted_code:
                            st.error(f"Verification Error: Could not re-encrypt the result. Details: `{re_encrypted_code}`") # Changed terminology
                        else:
                            st.caption("**Re-encrypted Code (from decrypted text):**") # Changed terminology
                            formatted_reencrypted = format_idli_code_output(re_encrypted_code)
                            st.code(formatted_reencrypted, language=None)

                            if standardized_original_code == re_encrypted_code:
                                st.success("Verification Successful: Input code matches re-encrypted text.") # Changed terminology
                            else:
                                st.error("Verification Failed: Input code differs from re-encrypted text.") # Changed terminology
                                st.caption("Mismatch may be due to invalid words/formatting in original input.")
                                v_col1, v_col2 = st.columns(2)
                                with v_col1:
                                    st.caption("Standardized Input:")
                                    st.code(standardized_original_code, language=None)
                                with v_col2:
                                    st.caption("Re-encrypted:") # Changed terminology
                                    st.code(re_encrypted_code, language=None)
                elif decrypted_text is None and not errors:
                     st.warning("Input is empty or contains no valid 'Idli Code' words.")

            else:
                st.warning("Please enter 'Idli Code' to decrypt.") # Changed terminology

# --- Footer ---
st.write("---")
st.caption("Idli Code Converter") # Simplified footer