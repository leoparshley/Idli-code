import streamlit as st
import textwrap
import base64
import re  # Import regex for more robust splitting
from typing import List, Dict, Tuple, Optional

# --- Constants ---
WORD_TO_DIGIT: Dict[str, str] = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
DIGIT_TO_WORD: Dict[str, str] = {v: k for k, v in WORD_TO_DIGIT.items()}
QUATERNARY_TO_BINARY: Dict[str, str] = {'0': '00', '1': '01', '2': '10', '3': '11'}
BINARY_TO_QUATERNARY: Dict[str, str] = {v: k for k, v in QUATERNARY_TO_BINARY.items()}
VALID_WORDS = set(WORD_TO_DIGIT.keys())

# --- Core Logic Functions ---

def text_to_idli_code(text: str) -> str:
    """
    Encodes a string into Idli Code.
    Text -> Bytes -> Binary String -> Quaternary String -> Idli Words.
    """
    if not text:
        return ""
    try:
        # Convert text to a single binary string (each char as 8 bits)
        binary_str = ''.join([format(ord(c), '08b') for c in text])

        # Ensure binary string length is even for chunking into 2-bit pairs
        if len(binary_str) % 2 != 0:
             # This case shouldn't happen with ord() -> 08b, but safety first
             binary_str += '0' # Pad with '0' if necessary

        # Group binary string into 2-bit chunks
        binary_chunks: List[str] = textwrap.wrap(binary_str, 2)

        # Convert binary chunks to quaternary digits
        quaternary_digits: List[str] = [BINARY_TO_QUATERNARY.get(chunk, '') for chunk in binary_chunks]
        quaternary_str = ''.join(quaternary_digits)

        # Convert quaternary digits to Idli words
        words: List[str] = [DIGIT_TO_WORD[d] for d in quaternary_str if d in DIGIT_TO_WORD]

        return ' '.join(words)
    except Exception as e:
        st.error(f"An unexpected error occurred during encryption: {e}")
        return "Error during encryption"

def idli_code_to_text(code: str) -> Tuple[Optional[str], Optional[List[str]]]:
    """
    Decodes Idli Code (space-separated words) back into text.
    Handles potential errors like invalid words or formatting.

    Returns:
        Tuple[Optional[str], Optional[List[str]]]: (decoded_text, list_of_invalid_words)
        Returns (None, invalid_words) on error.
    """
    if not code:
        return None, None # Indicate no input

    # 1. Clean and prepare input words
    #    - Strip whitespace, split by any whitespace, filter empty strings
    #    - Convert to Title Case for case-insensitivity
    potential_words = [word.strip().title() for word in re.split(r'\s+', code.strip()) if word]

    if not potential_words:
        return None, None # Indicate effectively empty input after cleaning

    quaternary_digits: List[str] = []
    invalid_words: List[str] = []

    # 2. Convert words to quaternary digits, tracking errors
    for word in potential_words:
        digit = WORD_TO_DIGIT.get(word)
        if digit is not None:
            quaternary_digits.append(digit)
        else:
            invalid_words.append(word)

    if invalid_words:
        return None, invalid_words # Error: Invalid words found

    quaternary_str = ''.join(quaternary_digits)

    # 3. Convert quaternary to binary
    try:
        binary_str = ''.join([QUATERNARY_TO_BINARY[d] for d in quaternary_str])
    except KeyError as e:
        # This shouldn't happen if WORD_TO_DIGIT and QUATERNARY_TO_BINARY are correct
        return f"Internal Error: Invalid quaternary digit '{e}' encountered.", None

    # 4. Check if binary string length is a multiple of 8
    if len(binary_str) % 8 != 0:
        error_msg = (f"Error: Invalid Idli Code structure. "
                     f"The code translates to a binary sequence of length {len(binary_str)}, "
                     f"which is not divisible by 8 (needed for character bytes). "
                     f"Check for missing or extra words.")
        return None, [error_msg] # Use list to signal error type

    # 5. Convert binary chunks (8 bits) back to characters
    try:
        byte_chunks = textwrap.wrap(binary_str, 8)
        decoded_chars = [chr(int(b, 2)) for b in byte_chunks]
        decoded_text = "".join(decoded_chars)
        return decoded_text, None # Success
    except ValueError:
        # Error converting binary chunk to integer (shouldn't happen with '0'/'1')
         return "Error: Problem decoding binary data to characters.", None
    except Exception as e:
        # Catch any other unexpected errors during final decoding
        return f"An unexpected error occurred during final decoding: {e}", None


def format_idli_code_output(code_str: str, words_per_line: int = 10) -> str:
    """Formats the Idli Code string into lines with a specific number of words."""
    if not code_str:
        return ""
    words = code_str.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

def generate_download_link(content: str, filename: str, link_text: str) -> str:
    """Generates a base64 encoded download link for text content."""
    try:
        b64 = base64.b64encode(content.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'
    except Exception as e:
        st.error(f"Failed to generate download link for {filename}: {e}")
        return "<span>Error generating download link</span>"

# --- Streamlit UI ---
st.set_page_config(layout="wide") # Use wider layout

st.title("🍲 Idli Code Encoder & Decoder 🍲")
st.caption("Convert text to a sequence of Idli, Dosa, Sambar, and Chutney!")

option = st.radio(
    "Choose an operation:",
    ('Encode Text to Idli Code', 'Decode Idli Code to Text'),
    horizontal=True,
    key="operation_choice"
)

st.divider()

if option == 'Encode Text to Idli Code':
    st.subheader("Encoder")
    user_input = st.text_area("Enter text to encode:", height=150, key="encode_input")

    if st.button("Encode Text", key="encode_button"):
        if user_input.strip():
            with st.spinner("Encoding..."):
                encoded_code = text_to_idli_code(user_input)

            if "Error" not in encoded_code:
                formatted_code = format_idli_code_output(encoded_code)
                st.text_area("Encoded Idli Code:", value=formatted_code, height=250, key="encoded_output", disabled=True)
                st.markdown(
                    generate_download_link(formatted_code, "encoded_idli_code.txt", "Download Encoded Code (.txt)"),
                    unsafe_allow_html=True
                )

                # --- Verification Expander ---
                with st.expander("Show Verification Details"):
                    st.write("To ensure correctness, the encoded output was automatically decoded back:")
                    re_decoded_text, errors = idli_code_to_text(encoded_code) # Use unformatted code for accuracy check

                    if errors:
                         st.error(f"Verification Error: Could not decode the generated code. Error: {errors}")
                    elif re_decoded_text is not None:
                        st.text_area("Re-decoded Text:", value=re_decoded_text, height=150, key="redecoded_verify", disabled=True)
                        if user_input == re_decoded_text:
                            st.success("✅ Verification Successful: Original text and re-decoded text match perfectly.")
                        else:
                            st.error("❌ Verification Failed: Mismatch between original text and re-decoded text.")
                            # Optionally show differences for debugging (can be long)
                            # st.code(f"Original:\n{user_input}\n\nRe-decoded:\n{re_decoded_text}", language=None)
                    else:
                         st.warning("Verification couldn't be performed (Decoding returned None).")

            else:
                # Error message already shown by text_to_idli_code
                pass
        else:
            st.warning("Please enter some text to encode.")

elif option == 'Decode Idli Code to Text':
    st.subheader("Decoder")
    code_input = st.text_area(
        "Enter your space-separated Idli Code:",
        height=250,
        key="decode_input",
        help="Accepts Idli, Dosa, Sambar, Chutney. Case-insensitive. Extra spaces are ignored."
        )

    if st.button("Decode Idli Code", key="decode_button"):
        cleaned_input = code_input.strip()
        if cleaned_input:
            with st.spinner("Decoding..."):
                decoded_text, errors = idli_code_to_text(cleaned_input)

            if errors:
                if isinstance(errors[0], str) and "Invalid Idli Code structure" in errors[0]:
                     st.error(errors[0]) # Show structure error clearly
                else:
                     st.error(f"Found invalid words in the input: {', '.join(errors)}. Please use only Idli, Dosa, Sambar, Chutney.")
            elif decoded_text is not None:
                st.text_area("Decoded Text:", value=decoded_text, height=150, key="decoded_output", disabled=True)
                st.markdown(
                    generate_download_link(decoded_text, "decoded_text.txt", "Download Decoded Text (.txt)"),
                    unsafe_allow_html=True
                )

                # --- Verification Expander ---
                with st.expander("Show Verification Details"):
                    st.write("To ensure correctness, the decoded text was automatically encoded back:")
                    # Re-encode the result
                    re_encoded_code = text_to_idli_code(decoded_text)

                    # Prepare the original input for comparison (standard format)
                    original_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                    standardized_original_code = ' '.join(original_words)

                    if "Error" in re_encoded_code:
                         st.error(f"Verification Error: Could not re-encode the decoded text. Error: {re_encoded_code}")
                    else:
                        st.text_area("Re-encoded Idli Code:", value=format_idli_code_output(re_encoded_code), height=200, key="reencoded_verify", disabled=True)
                        # Compare the re-encoded version with a standardized version of the input
                        if standardized_original_code == re_encoded_code:
                            st.success("✅ Verification Successful: Input code (standardized) and re-encoded code match.")
                        else:
                            st.error("❌ Verification Failed: Mismatch between input code and re-encoded code.")
                            # Optionally show differences
                            # st.code(f"Standardized Input:\n{standardized_original_code}\n\nRe-encoded Output:\n{re_encoded_code}", language=None)
            elif decoded_text is None and not errors:
                 st.warning("Input was empty or contained no valid Idli Code words after cleaning.")

        else:
            st.warning("Please enter Idli Code to decode.")

st.divider()
st.caption("Made with Streamlit")