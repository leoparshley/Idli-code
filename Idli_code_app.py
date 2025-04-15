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

# --- Core Logic Functions --- (Keep as before, maybe adjust error messages slightly)
def text_to_idli_code(text: str) -> str:
    if not text: return ""
    try:
        binary_str = ''.join([format(ord(c), '08b') for c in text])
        binary_chunks: List[str] = textwrap.wrap(binary_str, 2)
        quaternary_digits: List[str] = [BINARY_TO_QUATERNARY.get(chunk, '') for chunk in binary_chunks]
        quaternary_str = ''.join(quaternary_digits)
        words: List[str] = [DIGIT_TO_WORD[d] for d in quaternary_str if d in DIGIT_TO_WORD]
        return ' '.join(words)
    except Exception as e:
        st.error(f"Error during encryption: {e}") # Simplified error
        return "Error during encryption"

def idli_code_to_text(code: str) -> Tuple[Optional[str], Optional[List[str]]]:
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
        return None, [f"Internal Error: Invalid quaternary digit '{e}'."] # Simplified error
    if len(binary_str) % 8 != 0:
        error_msg = (f"Error: Invalid code structure. Binary length ({len(binary_str)}) "
                     f"not divisible by 8. Check input code.") # Simplified error
        return None, [error_msg]
    try:
        byte_chunks = textwrap.wrap(binary_str, 8)
        decoded_chars = [chr(int(b, 2)) for b in byte_chunks]
        decoded_text = "".join(decoded_chars)
        return decoded_text, None
    except ValueError:
         return None, ["Error: Problem decoding binary data to characters."] # Simplified error
    except Exception as e:
        return None, [f"Error during final decoding: {e}"] # Simplified error

def format_idli_code_output(code_str: str, words_per_line: int = 10) -> str: # Maybe increase words per line slightly
    if not code_str: return ""
    words = code_str.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

# --- Streamlit UI ---
st.set_page_config(
    page_title="Idli Code Converter",
    page_icon="🍲", # Optional: keep or remove this subtle icon
    layout="centered"
)

# --- Header ---
st.title("Idli Code Converter")
st.caption("Encode text to Idli Code (Idli, Dosa, Sambar, Chutney) and decode it back.")

st.markdown("---") # Divider

# --- Operation Selection ---
st.markdown("##### Select Operation") # Slightly smaller heading
option = st.radio(
    "Select Operation:",
    ('Encode Text', 'Decode Idli Code'), # Simplified labels
    horizontal=True,
    key="operation_choice",
    label_visibility="collapsed"
)

st.write("") # Add space

# --- Main Content Area ---

if option == 'Encode Text':
    with st.container(border=True):
        st.subheader("Encode Text to Idli Code")

        user_input = st.text_area(
            "Text to Encode:",
            height=150,
            key="encode_input",
            label_visibility="collapsed",
            placeholder="Enter text here..." # Neutral placeholder
        )

        encode_pressed = st.button("Encode", key="encode_button", type="primary") # Simple label

        if encode_pressed:
            input_text = user_input.strip()
            if input_text:
                with st.spinner("Encoding..."): # Simple spinner text
                    encoded_code = text_to_idli_code(input_text)

                if "Error" not in encoded_code:
                    formatted_code = format_idli_code_output(encoded_code)

                    st.markdown("---") # Divider before output
                    st.markdown("##### Encoded Idli Code:") # Simple label
                    st.code(formatted_code, language=None)

                    st.download_button(
                        label="Download Code (.txt)", # Simple label
                        data=formatted_code,
                        file_name="encoded_idli_code.txt",
                        mime="text/plain",
                        key="download_encoded"
                        # Removed use_container_width, default behavior is often fine
                    )

                    # --- Verification Expander ---
                    with st.expander("Show Verification Details"):
                        re_decoded_text, errors = idli_code_to_text(encoded_code)

                        if errors:
                            st.error(f"Verification Error: Could not decode the generated code. Details: `{errors}`")
                        elif re_decoded_text is not None:
                            st.markdown("**Text After Round-Trip:**")
                            st.text_area("Re-decoded Text", value=re_decoded_text, height=100, key="redecoded_verify", disabled=True, label_visibility="collapsed")
                            if input_text == re_decoded_text:
                                st.success("Verification Successful: Texts match.") # Simple message
                            else:
                                st.error("Verification Failed: Texts differ.") # Simple message
                                # Use columns for side-by-side comparison on wider screens
                                v_col1, v_col2 = st.columns(2)
                                with v_col1:
                                    st.text("Original:")
                                    st.code(input_text, language=None)
                                with v_col2:
                                    st.text("Re-decoded:")
                                    st.code(re_decoded_text, language=None)
                        else:
                            st.warning("Verification could not be performed.")

                # Error case handled by st.error within the function
            else:
                st.warning("Please enter text to encode.")

elif option == 'Decode Idli Code':
    with st.container(border=True):
        st.subheader("Decode Idli Code to Text")

        code_input = st.text_area(
            "Idli Code Sequence:",
            height=200,
            key="decode_input",
            label_visibility="collapsed",
            placeholder="Enter Idli Code sequence here (e.g., Idli Dosa Sambar...)" # Neutral placeholder
        )

        decode_pressed = st.button("Decode", key="decode_button", type="primary") # Simple label

        if decode_pressed:
            cleaned_input = code_input.strip()
            if cleaned_input:
                with st.spinner("Decoding..."): # Simple spinner text
                    decoded_text, errors = idli_code_to_text(cleaned_input)

                if errors:
                    # Simplified Error Handling
                    error_message = errors[0] if isinstance(errors, list) and errors else "Unknown decoding error."
                    if "Invalid code structure" in error_message or "Problem decoding" in error_message or "Internal Error" in error_message:
                         st.error(f"Decoding Error: {error_message}")
                    else:
                         # Assume list of invalid words
                         st.error(f"Invalid Input: Found non-code words: `{', '.join(errors)}`")
                         st.caption("Please use only: Idli, Dosa, Sambar, Chutney")

                elif decoded_text is not None:
                    st.markdown("---") # Divider before output
                    st.markdown("##### Decoded Text:") # Simple label
                    st.text_area("Decoded Text Output", value=decoded_text, height=150, key="decoded_output", disabled=True, label_visibility="collapsed")

                    st.download_button(
                        label="Download Text (.txt)", # Simple label
                        data=decoded_text,
                        file_name="decoded_text.txt",
                        mime="text/plain",
                        key="download_decoded"
                    )

                    # --- Verification Expander ---
                    with st.expander("Show Verification Details"):
                        re_encoded_code = text_to_idli_code(decoded_text)
                        original_valid_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                        standardized_original_code = ' '.join(original_valid_words)

                        if "Error" in re_encoded_code:
                            st.error(f"Verification Error: Could not re-encode the result. Details: `{re_encoded_code}`")
                        else:
                            st.markdown("**Re-encoded Code (from decoded text):**")
                            formatted_reencoded = format_idli_code_output(re_encoded_code)
                            st.code(formatted_reencoded, language=None)

                            if standardized_original_code == re_encoded_code:
                                st.success("Verification Successful: Input code matches re-encoded text.") # Simple message
                            else:
                                st.error("Verification Failed: Input code differs from re-encoded text.") # Simple message
                                st.caption("This can happen if the input had invalid words/formatting.")
                                # Use columns for side-by-side comparison
                                v_col1, v_col2 = st.columns(2)
                                with v_col1:
                                    st.text("Valid Input Code:")
                                    st.code(standardized_original_code, language=None)
                                with v_col2:
                                    st.text("Re-encoded Result:")
                                    st.code(re_encoded_code, language=None)
                elif decoded_text is None and not errors:
                     st.warning("Input is empty or contains no valid Idli Code words.")

            else:
                st.warning("Please enter Idli Code to decode.")

# --- Footer ---
st.markdown("---")
st.caption("Idli Code Converter") # Simplified footer