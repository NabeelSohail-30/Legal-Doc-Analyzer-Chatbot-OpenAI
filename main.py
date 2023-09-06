import streamlit as st
import openai
import json

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

# Streamlit app layout
st.title("Legal Document Analyzer")

# File upload section
uploaded_file = st.file_uploader("Upload a legal document", type=["pdf", "docx", "txt"])

if uploaded_file:
    document_text = uploaded_file.read()
    st.subheader("Uploaded Document Preview")
    st.text(document_text)

    prompt = f"""
        You are an expert legal advisor with an experience of more than a decade. \
        Analyze the following Legal Document delimited by triple backticks \
        provide a JSON Object response \
        mentioning the following: \

        1. Risky Clauses \
        2. Partial Risky Clauses \
        3. Safe Clauses \

        Legal Document:
        ```
        {document_text}
        ```
    """

    # Analyze the document using the OpenAI API
    st.subheader("Analysis Results")

    # Generate analysis using OpenAI GPT model
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    analysis = response.choices[0].text.strip()

    # Parse the JSON response from the model into a Python dictionary
    try:
        analysis_dict = json.loads(analysis)
    except json.JSONDecodeError:
        st.error("Error parsing JSON response.")
        analysis_dict = {}

    # Extract and display Risky, Partial Risky, and Safe clauses
    risky_clauses = analysis_dict.get("Risky Clauses", [])
    partial_risky_clauses = analysis_dict.get("Partial Risky Clauses", [])
    safe_clauses = analysis_dict.get("Safe Clauses", [])

    st.subheader("Risky Clauses")
    for clause in risky_clauses:
        st.markdown(f"- {clause}")

    st.subheader("Partial Risky Clauses")
    for clause in partial_risky_clauses:
        st.markdown(f"- {clause}")

    st.subheader("Safe Clauses")
    for clause in safe_clauses:
        st.markdown(f"- {clause}")

