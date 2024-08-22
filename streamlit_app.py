import streamlit as st
import openai
import pandas as pd

# Show title and description.
st.title("💬 File-Integrated Chatbot")
st.write(
    "This chatbot leverages OpenAI's GPT-3.5 model and scans your uploaded CSV or Excel file to provide answers. "
    "To get started, enter your OpenAI API key, upload your file, and ask a question!"
)

# Step 1: User inputs their OpenAI API key.
openai_api_key = st.text_input("OpenAI API Key", type="password", help="Get your API key from https://platform.openai.com/account/api-keys")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set the OpenAI API key
    openai.api_key = openai_api_key

    # Step 2: User uploads a CSV or Excel file.
    uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"], help="Upload a CSV or Excel file")
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                # Attempt to read CSV with utf-8 encoding. If it fails, try with 'ISO-8859-1'.
                try:
                    df = pd.read_csv(uploaded_file)
                except UnicodeDecodeError:
                    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            else:
                df = pd.read_excel(uploaded_file)

            st.success("File uploaded successfully!")

            # Step 3: User can ask a question.
            user_question = st.text_input("Ask a question about the data")

            if user_question:
                # Display the user's question.
                st.write(f"**Question:** {user_question}")

                # Step 4: Scan the uploaded file for the answer.
                data_str = df.to_string()

                # Create a prompt for the OpenAI API.
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Here's the data:\n{data_str}\n\nAnswer this question: {user_question}"}
                ]

                # Generate a response using the OpenAI API.
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=150
                )

                # Step 5: Provide the answer.
                st.write("**Answer:**")
                st.write(response.choices[0].message["content"])

        except Exception as e:
            st.error(f"An error occurred: {e}")
