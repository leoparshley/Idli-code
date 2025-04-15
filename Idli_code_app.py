import streamlit as st

# Mappings
word_to_quat = {'Idli': '0', 'Dosa': '1', 'Sambar': '2', 'Chutney': '3'}
quat_to_word = {v: k for k, v in word_to_quat.items()}
quat_to_bin = {'0': '00', '1': '01', '2': '10', '3': '11'}
bin_to_quat = {v: k for k, v in quat_to_bin.items()}

def encrypt(text):
    # Convert text to binary
    binary = ''.join(format(ord(c), '08b') for c in text)
    # Convert binary to quaternary
    quaternary = [bin_to_quat[binary[i:i+2]] for i in range(0, len(binary), 2)]
    # Return as space-separated code
    return ' '.join(quat_to_word[q] for q in quaternary)

def decrypt(code):
    # Clean the input by removing extra spaces, line breaks, and empty characters
    code = ' '.join(code.split())  # This removes all unnecessary spaces and newlines
    
    try:
        # Convert the idli code back to quaternary
        words = code.split()
        quaternary = [word_to_quat[word] for word in words]
        # Convert quaternary to binary
        binary = ''.join(quat_to_bin[q] for q in quaternary)
        # Convert binary to text
        text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return text
    except Exception as e:
        return "Invalid Idli Code! Please ensure the input is correct."

# Streamlit settings
st.set_page_config(page_title="Idli Code Encryptor", layout="centered")
st.title("Idli Code Encryptor & Decryptor")

option = st.radio("Choose an option", ["Encrypt", "Decrypt"])

def wrap_encrypted_text(text, line_length=100):
    """ Function to wrap the encrypted text for better readability while keeping it reversible """
    words = text.split()  # Split the encrypted text into words
    wrapped_text = []
    
    # Group the words into lines of a specified length
    for i in range(0, len(words), line_length):
        wrapped_text.append(' '.join(words[i:i + line_length]))
    
    # Join the wrapped lines with line breaks
    return '\n'.join(wrapped_text)

if option == "Encrypt":
    text = st.text_area("Enter text to encrypt", height=200)
    if st.button("Encrypt"):
        encrypted_text = encrypt(text)
        
        # Wrap the encrypted text to improve readability, 100 words per line
        wrapped_encrypted_text = wrap_encrypted_text(encrypted_text, line_length=100)

        # Display the formatted output as code
        st.code(wrapped_encrypted_text)

        # Add "Copy to Clipboard" button for encrypted text using JavaScript
        st.markdown(f"""
            <button onclick="navigator.clipboard.writeText('{wrapped_encrypted_text}')">
            Copy Encrypted Text to Clipboard
            </button>
            <script>
                document.querySelector('button').style.padding = '10px';
                document.querySelector('button').style.fontSize = '14px';
                document.querySelector('button').style.cursor = 'pointer';
            </script>
            """, unsafe_allow_html=True)

        # Add "Download" button for encrypted text
        st.download_button(
            label="Download Encrypted Text",
            data=wrapped_encrypted_text,
            file_name="encrypted_text.txt",
            mime="text/plain"
        )

else:
    code = st.text_area("Enter Idli code to decrypt", height=200)
    if st.button("Decrypt"):
        decrypted_text = decrypt(code)
        # Display the decrypted text as code
        st.code(decrypted_text)

        # Add "Copy to Clipboard" button for decrypted text using JavaScript
        st.markdown(f"""
            <button onclick="navigator.clipboard.writeText('{decrypted_text}')">
            Copy Decrypted Text to Clipboard
            </button>
            <script>
                document.querySelector('button').style.padding = '10px';
                document.querySelector('button').style.fontSize = '14px';
                document.querySelector('button').style.cursor = 'pointer';
            </script>
            """, unsafe_allow_html=True)

        # Add "Download" button for decrypted text
        st.download_button(
            label="Download Decrypted Text",
            data=decrypted_text,
            file_name="decrypted_text.txt",
            mime="text/plain"
        )