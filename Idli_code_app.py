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
        st.error(f"💥 An unexpected error occurred during encryption: {e}")
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
        return None, [f"Internal Error: Invalid quaternary digit '{e}' encountered."]
    if len(binary_str) % 8 != 0:
        error_msg = (f"Error: Invalid Idli Code structure. Binary length ({len(binary_str)}) "
                     f"is not divisible by 8. Check for missing/extra words.")
        return None, [error_msg]
    try:
        byte_chunks = textwrap.wrap(binary_str, 8)
        decoded_chars = [chr(int(b, 2)) for b in byte_chunks]
        decoded_text = "".join(decoded_chars)
        return decoded_text, None
    except ValueError:
         return None, ["Error: Problem decoding binary data to characters. Data might be corrupted."]
    except Exception as e:
        return None, [f"An unexpected error occurred during final decoding: {e}"]

def format_idli_code_output(code_str: str, words_per_line: int = 8) -> str: # Reduce words per line slightly
    if not code_str: return ""
    words = code_str.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)

# --- Streamlit UI ---
st.set_page_config(
    page_title="Idli Code Converter",
    page_icon="🍲",
    layout="centered" # Use centered layout for better mobile/readability
)

# --- Header ---
col_icon, col_title = st.columns([1, 5])
with col_icon:
    st.image("https://em-content.zobj.net/source/google/387/steaming-bowl_1f35c.png", width=80) # Use a steaming bowl image
with col_title:
    st.title("Idli Code Converter")
    st.caption("Encode text to Idli Code & Decode it back!")

st.markdown("---") # Divider

# --- Operation Selection ---
st.markdown("#### Select Operation:")
option = st.radio(
    "Select Operation:", # Label for screen readers
    ('🔒 Encode Text', '🔓 Decode Idli Code'),
    horizontal=True,
    key="operation_choice",
    label_visibility="collapsed" # Hide label as markdown is above
)

st.write("") # Add space

# --- Main Content Area ---

if option == '🔒 Encode Text':
    with st.container(border=True):
        st.subheader("🔒 Encode Text to Idli Code")
        st.markdown("Enter the text you want to convert into Idli Code below.")

        user_input = st.text_area(
            "Text to Encode:",
            height=150,
            key="encode_input",
            label_visibility="collapsed",
            placeholder="Type or paste your secret message here..."
        )

        # Button centered using columns (a common trick)
        col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
        with col_btn2:
             encode_pressed = st.button("Convert to Idli Code ➡️", key="encode_button", type="primary", use_container_width=True)

        if encode_pressed:
            if user_input.strip():
                with st.spinner("🥣 Cooking up your Idli Code..."):
                    encoded_code = text_to_idli_code(user_input)

                if "Error" not in encoded_code:
                    formatted_code = format_idli_code_output(encoded_code)

                    st.markdown("---") # Divider before output
                    st.markdown("##### ✨ Your Idli Code:")
                    # Use code block for better formatting control
                    st.code(formatted_code, language=None)

                    st.download_button(
                        label="📄 Download Code (.txt)",
                        data=formatted_code,
                        file_name="encoded_idli_code.txt",
                        mime="text/plain",
                        key="download_encoded",
                        use_container_width=True # Make download button fill width
                    )

                    # --- Verification Expander ---
                    with st.expander("🔍 Verify Accuracy (Optional)"):
                        st.caption("_The encoded code was automatically decoded back to check for consistency._")
                        re_decoded_text, errors = idli_code_to_text(encoded_code)

                        if errors:
                            st.error(f"**Verification Error:** Could not decode the generated code. Details: `{errors}`")
                        elif re_decoded_text is not None:
                            st.markdown("**Text After Round-Trip:**")
                            st.text_area("Re-decoded Text", value=re_decoded_text, height=100, key="redecoded_verify", disabled=True, label_visibility="collapsed")
                            if user_input == re_decoded_text:
                                st.success("✅ **Success!** Original and re-decoded text match.")
                            else:
                                st.error("❌ **Mismatch!** Original and re-decoded text differ.")
                                # Use columns for side-by-side comparison on wider screens
                                v_col1, v_col2 = st.columns(2)
                                with v_col1:
                                    st.text("Original:")
                                    st.code(user_input, language=None)
                                with v_col2:
                                    st.text("Re-decoded:")
                                    st.code(re_decoded_text, language=None)
                        else:
                            st.warning("Verification couldn't be performed (Decoding returned None).")

                # Error case handled by st.error within the function
            else:
                st.warning("❕ Please enter some text to encode.")

elif option == '🔓 Decode Idli Code':
    with st.container(border=True):
        st.subheader("🔓 Decode Idli Code to Text")
        st.markdown("Enter the sequence of `Idli`, `Dosa`, `Sambar`, `Chutney` below.")

        code_input = st.text_area(
            "Idli Code Sequence:",
            height=200,
            key="decode_input",
            label_visibility="collapsed",
            placeholder="Paste your Idli Dosa Sambar Chutney sequence here...",
            help="Words should be separated by spaces. Case doesn't matter. Extra spaces/newlines are ignored."
        )

        # Button centered using columns
        col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
        with col_btn2:
            decode_pressed = st.button("Convert to Text ➡️", key="decode_button", type="primary", use_container_width=True)

        if decode_pressed:
            cleaned_input = code_input.strip()
            if cleaned_input:
                with st.spinner("🍲 Translating the code back to text..."):
                    decoded_text, errors = idli_code_to_text(cleaned_input)

                if errors:
                    # Error Handling - Make messages clear
                    is_structure_error = any("Invalid Idli Code structure" in str(e) for e in errors)
                    is_decoding_error = any("Problem decoding binary data" in str(e) for e in errors)
                    # ... other specific error checks if needed ...

                    if is_structure_error or is_decoding_error:
                         st.error(f"**Decoding Error:** {errors[0]}", icon="💔")
                    else:
                         # Assume list of invalid words
                         st.error(f"**Invalid Input:** Found non-code words: `{', '.join(errors)}`", icon="🤷‍♀️")
                         st.caption("Please use only: Idli, Dosa, Sambar, Chutney")

                elif decoded_text is not None:
                    st.markdown("---") # Divider before output
                    st.markdown("##### ✨ Decoded Text:")
                    # Use text_area for easy copying of potentially longer text
                    st.text_area("Decoded Text Output", value=decoded_text, height=150, key="decoded_output", disabled=True, label_visibility="collapsed")

                    st.download_button(
                        label="📄 Download Text (.txt)",
                        data=decoded_text,
                        file_name="decoded_text.txt",
                        mime="text/plain",
                        key="download_decoded",
                        use_container_width=True # Make download button fill width
                    )

                    # --- Verification Expander ---
                    with st.expander("🔍 Verify Accuracy (Optional)"):
                        st.caption("_The decoded text was re-encoded to check if it matches the valid parts of your original input._")
                        re_encoded_code = text_to_idli_code(decoded_text)
                        original_valid_words = [word.strip().title() for word in re.split(r'\s+', cleaned_input) if word.strip().title() in VALID_WORDS]
                        standardized_original_code = ' '.join(original_valid_words)

                        if "Error" in re_encoded_code:
                            st.error(f"**Verification Error:** Could not re-encode the result. Details: `{re_encoded_code}`")
                        else:
                            st.markdown("**Re-encoded Code (from result):**")
                            formatted_reencoded = format_idli_code_output(re_encoded_code)
                            st.code(formatted_reencoded, language=None)

                            if standardized_original_code == re_encoded_code:
                                st.success("✅ **Success!** Input code (valid parts) matches re-encoded text.")
                            else:
                                st.error("❌ **Mismatch!** Input code differs from re-encoded text.")
                                st.caption("This can happen if your input had invalid words/formatting.")
                                # Use columns for side-by-side comparison
                                v_col1, v_col2 = st.columns(2)
                                with v_col1:
                                    st.text("Valid Input Code:")
                                    st.code(standardized_original_code, language=None)
                                with v_col2:
                                    st.text("Re-encoded Result:")
                                    st.code(re_encoded_code, language=None) # Unformatted for direct diff
                elif decoded_text is None and not errors:
                     st.warning("❕ Input seemed empty or had no valid Idli Code words.")

            else:
                st.warning("❕ Please enter some Idli Code to decode.")

# --- Footer ---
st.markdown("---")
st.caption("Made with 🍲 and Streamlit. Ensure your GitHub repo is updated and check deployment status!")