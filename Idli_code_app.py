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