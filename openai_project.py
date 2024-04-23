import streamlit as st
import PyPDF2
import openai
from io import BytesIO

# OpenAI API Key
openai.api_key = 'sk-proj-GBGDDHiiuUjRK0wD6pZdT3BlbkFJw7Ye6fKj0XbdDOmX7zAZ'

def extract_text_from_pdf(file):
    with BytesIO(file.getvalue()) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def query_openai(text, question):
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose different models
        prompt=f"{text}\n\nQuestion: {question}\nAnswer:",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    st.title('PDF Chatbot')
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted Text", value=text, height=300)
        
        question = st.text_input("Ask a question based on the PDF:")
        if st.button("Get Answer"):
            if question:
                answer = query_openai(text, question)
                st.write("Answer:", answer)
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()