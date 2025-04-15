def decrypt(encrypted_text):
    words = encrypted_text.replace('\n', ' ').split()
    cleaned_words = [word.strip().capitalize() for word in words if word.strip()]

    invalid = [w for w in cleaned_words if w not in quat_to_char]
    if invalid:
        return f"Invalid code: contains unknown word(s): {', '.join(invalid)}"

    try:
        quats = [quat_to_char[word] for word in cleaned_words]
        bins = [quat_to_bin[q] for q in quats]
        binary_string = ''.join(bins)
        chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
        return ''.join(chars)
    except:
        return "Decryption failed. Check for possible corruption or unsupported characters."