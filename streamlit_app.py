import streamlit as st
from openai import OpenAI
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
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Step 2: User uploads a CSV or Excel file.
    uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"], help="Upload a CSV or Excel file")
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        # Step 3: User can ask a question.
        user_question = st.text_input("Ask a question about the data")

        if user_question:
            # Display the user's question.
            st.write(f"**Question:** {user_question}")

            # Step 4: Scan the uploaded file for the answer.
            # For simplicity, we'll just convert the entire DataFrame to a string.
            # In a real application, you would implement a more sophisticated search.
            data_str = df.to_string()

            # Create a prompt for the OpenAI API.
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Here's the data:\n{data_str}\n\nAnswer this question: {user_question}"}
            ]

            # Generate a response using the OpenAI API.
            response = client.Completion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )

            # Step 5: Provide the answer.
            st.write("**Answer:**")
            st.write(response.choices[0].message["content"])
