import streamlit as st
import textwrap
# import base64 # No longer needed
import re  # Import regex for more robust splitting
from typing import List, Dict, Tuple, Optional


# --- Constants ---
WORD_TO_DIGIT: Dict[str, str] = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
DIGIT_TO_WORD: Dict[str, str] = {v: k for k, v in WORD_TO_DIGIT.items()}
QUATERNARY_TO_BINARY: Dict[str, str] = {'0': '00', '1': '01', '2': '10', '3': '11'}
BINARY_TO_QUATERNARY: Dict[str, str] = {v: k for k, v in QUATERNARY_TO_BINARY.items()}
VALID_WORDS = set(WORD_TO_DIGIT.keys())

# --- Core Logic Functions ---
# (Keep the core logic functions exactly as they were in the previous version)
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

        # Group binary string into 2-bit chunks
        binary_chunks: List[str] = textwrap.wrap(binary_str, 2)

        # Convert binary chunks to quaternary digits
        quaternary_digits: List[str] = [BINARY_TO_QUATERNARY.get(chunk, '') for chunk in binary_chunks]
        quaternary_str = ''.join(quaternary_digits)

        # Convert quaternary digits to Idli words
        words: List[str] = [DIGIT_TO_WORD[d] for d in quaternary_str if d in DIGIT_TO_WORD]

        return ' '.join(words) # Standard space separation
    except Exception as e:
        st.error(f"An unexpected error occurred during encryption: {e}")
        return "Error during encryption"

def idli_code_to_text(code: str) -> Tuple[Optional[str], Optional[List[str]]]:
    """
    Decodes Idli Code (space-separated words) back into text.
    Handles potential errors like invalid words or formatting.

    Returns:
        Tuple[Optional[str], Optional[List[str]]]: (decoded_text, list_of_invalid_words_or_error_msg)
        Returns (None, error_list) on error. Error list can contain invalid words or a specific error message.
    """
    if not code:
        return None, None # Indicate no input

    # 1. Clean and prepare input words
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
            original_word = next((w for w in re.split(r'\s+', code.strip()) if w.strip().title() == word), word)
            invalid_words.append(original_word)


    if invalid_words:
        return None, invalid_words # Error: Invalid words found

    quaternary_str = ''.join(quaternary_digits)

    # 3. Convert quaternary to binary
    try:
        binary_str = ''.join([QUATERNARY_TO_BINARY[d] for d in quaternary_str])
    except KeyError as e:
        return None, [f"Internal Error: Invalid quaternary digit '{e}' encountered."]

    # 4. Check if binary string length is a multiple of 8
    if len(binary_str) % 8 != 0:
        error_msg = (f"Error: Invalid Idli Code structure. "
                     f"The code translates to a binary sequence of length {len(binary_str)}, "
                     f"which is not divisible by 8 (needed for character bytes). "
                     f"This usually means the sequence of Idli Code words is incomplete or corrupted. "
                     f"Check for missing or extra words.")
        return None, [error_msg]

    # 5. Convert binary chunks (8 bits) back to characters
    try:
        byte_chunks = textwrap.wrap(binary_str, 8)
        decoded_chars = []
        for b in byte_chunks:
             byte_val = int(b, 2)
             decoded_chars.append(chr(byte_val))

        decoded_text = "".join(decoded_chars)
        return decoded_text, None # Success
    except ValueError:
         return None, ["Error: Problem decoding binary data to characters. The data might be corrupted or not represent valid text."]
    except Exception as e:
        return None, [f"An unexpected error occurred during final decoding: {e}"]

def format_idli_code_output(code_str: str, words_per_line: int = 10) -> str:
    """Formats the Idli Code string into lines with a specific number of words."""
    if not code_str:
        return ""
    words = code_str.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

# --- Streamlit UI ---
st.set_page_config(
    page_title="Idli Code Converter",
    page_icon="🍲",
    layout="wide" # Keep wide layout for potentially long code/text
)

# --- Header ---
st.title("🍲 Idli Code Encoder & Decoder 🔓")
st.markdown("Welcome! Convert your secret messages into a delicious sequence of South Indian breakfast items, or decode them back.")
st.write("") # Add a little vertical space

# --- Operation Selection ---
option = st.radio(
    "**Choose an operation:**", # Use markdown for bold
    ('Encode Text to Idli Code', 'Decode Idli Code to Text'),
    horizontal=True,
    key="operation_choice",
    # label_visibility="collapsed" # Hide the default label if the markdown works well
)

st.divider() # Visually separate selection from the main panels

# --- Encoder Section ---
if option == 'Encode Text to Idli Code':
    st.subheader("🔒 Encode Text")
    with st.container(border=True): # Use a container with border
        st.markdown("##### Enter text to encode:")
        user_input = st.text_area(
            "Text Input", # Short label, primary label is markdown above
            height=150,
            key="encode_input",
            label_visibility="collapsed", # Hide default label if markdown is used
            placeholder="Type or paste your text here..."
        )

        if st.button("Encode Text ➡️", key="encode_button", type="primary"): # Make button prominent
            if user_input.strip():
                with st.spinner("Encoding... Please wait..."):
                    encoded_code = text_to_idli_code(user_input)

                if "Error" not in encoded_code:
                    formatted_code = format_idli_code_output(encoded_code)

                    st.write("") # Space before output
                    st.markdown("##### Encoded Idli Code:")
                    # Use st.code for fixed-width font, good for code display
                    st.code(formatted_code, language=None)

                    st.download_button(
                        label="📥 Download Encoded Code (.txt)", # Add icon
                        data=formatted_code,
                        file_name="encoded_idli_code.txt",
                        mime="text/plain",
                        key="download_encoded"
                    )

                    # --- Verification Expander ---
                    with st.expander("🔍 Show Verification Details"):
                        st.write("_To ensure correctness, the encoded output was automatically decoded back:_")
                        re_decoded_text, errors = idli_code_to_text(encoded_code)

                        if errors:
                            st.error(f"**Verification Error:** Could not decode the generated code. Error details: `{errors}`")
                        elif re_decoded_text is not None:
                            st.markdown("**Re-decoded Text:**")
                            st.text_area("Verification Output", value=re_decoded_text, height=100, key="redecoded_verify", disabled=True, label_visibility="collapsed")
                            if user_input == re_decoded_text:
                                st.success("✅ **Verification Successful:** Original text and re-decoded text match perfectly.")
                            else:
                                st.error("❌ **Verification Failed:** Mismatch between original text and re-decoded text.")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.text("Original Text:")
                                    st.code(user_input, language=None)
                                with col2:
                                    st.text("Re-decoded Text:")
                                    st.code(re_decoded_text, language=None)
                        else:
                            st.warning("Verification couldn't be performed (Decoding returned None unexpectedly).")

                else:
                    # Error message already shown by text_to_idli_code via st.error
                    pass # Error handled in the function
            else:
                st.warning("Please enter some text to encode.")

# --- Decoder Section ---
elif option == 'Decode Idli Code to Text':
    st.subheader("🔓 Decode Idli Code")
    with st.container(border=True): # Use a container with border
        st.markdown("##### Enter your space-separated Idli Code:")
        code_input = st.text_area(
            "Idli Code Input", # Short label
            height=200,
            key="decode_input",
            label_visibility="collapsed",
            placeholder="Paste your Idli Dosa Sambar Chutney sequence here...",
            help="Accepts 'Idli', 'Dosa', 'Sambar', 'Chutney'. Case-insensitive. Extra spaces/newlines are ignored."
        )

        if st.button("Decode Idli Code ➡️", key="decode_button", type="primary"): # Make button prominent
            cleaned_input = code_input.strip()
            if cleaned_input:
                with st.spinner("Decoding... Patience is a virtue..."):
                    decoded_text, errors = idli_code_to_text(cleaned_input)

                if errors:
                    # Determine error type
                    is_structure_error = any("Invalid Idli Code structure" in str(e) for e in errors)
                    is_decoding_error = any("Problem decoding binary data" in str(e) for e in errors)
                    is_internal_error = any("Internal Error" in str(e) for e in errors)
                    is_unexpected_error = any("unexpected error occurred during final decoding" in str(e) for e in errors)

                    if is_structure_error or is_decoding_error or is_internal_error or is_unexpected_error:
                         st.error(f"**Decoding Error:** {errors[0]}") # Show the specific error clearly
                    else:
                         # Assume it's a list of invalid words
                         st.error(f"**Invalid Input:** Found words that are not part of the code: `{', '.join(errors)}`. Please use only Idli, Dosa, Sambar, Chutney (case-insensitive).")

                elif decoded_text is not None:
                    st.write("") # Space before output
                    st.markdown("##### Decoded Text:")
                    # Use text_area for regular text output
                    st.text_area("Decoded Output", value=decoded_text, height=150, key="decoded_output", disabled=True, label_visibility="collapsed")

                    st.download_button(
                        label="📥 Download Decoded Text (.txt)", # Add icon
                        data=decoded_text,
                        file_name="decoded_text.txt",
                        mime="text/plain",
                        key="download_decoded"
                    )

                    # --- Verification Expander ---
                    with st.expander("🔍 Show Verification Details"):
                        st.write("_To ensure correctness, the decoded text was automatically encoded back:_")
                        re_encoded_code = text_to_idli_code(decoded_text)
                        original_valid_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                        standardized_original_code = ' '.join(original_valid_words)

                        if "Error" in re_encoded_code:
                            st.error(f"**Verification Error:** Could not re-encode the decoded text. Error: `{re_encoded_code}`")
                        else:
                            formatted_reencoded = format_idli_code_output(re_encoded_code)
                            st.markdown("**Re-encoded Idli Code (from decoded text):**")
                            st.code(formatted_reencoded, language=None)

                            # Compare the re-encoded version with the standardized valid words from the input
                            if standardized_original_code == re_encoded_code:
                                st.success("✅ **Verification Successful:** The valid code words in your input match the code generated by re-encoding the decoded text.")
                            else:
                                st.error("❌ **Verification Failed:** Mismatch between the standardized valid input code and the re-encoded code.")
                                st.caption("This might happen if the original input contained invalid words/formatting that were ignored, or potentially due to subtle encoding/decoding inconsistencies.")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.text("Standardized Valid Input:")
                                    st.code(standardized_original_code, language=None)
                                with col2:
                                    st.text("Re-encoded Output:")
                                    st.code(re_encoded_code, language=None) # Show unformatted for direct comparison
                elif decoded_text is None and not errors:
                     st.warning("Input was empty or contained no valid Idli Code words after cleaning.")

            else:
                st.warning("Please enter Idli Code to decode.")

# --- Footer ---
st.divider()
st.caption("Made with Streamlit & 🍲 | Check your inputs carefully!")