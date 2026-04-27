import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import PyPDF2
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
llm = ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="llama-3.3-70b-versatile")

def review_code(code):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert Python code reviewer. Provide: 1. Bugs 2. Improvements 3. Best practices. Keep it concise."},
            {"role": "user", "content": f"Review this Python code:\n{code}"}
        ]
    )
    return response.choices[0].message.content

def generate_flashcards(topic):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate exactly 5 flashcards. Format: Q: question\nA: answer\n---"),
        ("human", "Generate flashcards for: {topic}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"topic": topic})

def ask_document(question, document):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Answer ONLY from this document. If not found say Not found in document. DOCUMENT: {document}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

st.title("AI Learning Tools")

tab1, tab2, tab3 = st.tabs(["Code Reviewer", "Flashcard Generator", "Document Q&A"])

with tab1:
    st.header("Code Reviewer")
    code = st.text_area("Paste your Python code here", height=300)
    if st.button("Review My Code"):
        if code:
            with st.spinner("Reviewing..."):
                review = review_code(code)
            st.markdown("## Review:")
            st.markdown(review)
        else:
            st.warning("Please paste some code first!")

with tab2:
    st.header("Flashcard Generator")
    topic = st.text_input("Enter a topic")
    if st.button("Generate Flashcards"):
        if topic:
            with st.spinner("Generating..."):
                cards = generate_flashcards(topic)
            st.markdown("## Flashcards:")
            for card in cards.split("---"):
                if card.strip():
                    st.info(card.strip())
        else:
            st.warning("Please enter a topic first!")

with tab3:
    st.header("Document Q&A")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file:              # only read if file uploaded!
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        st.success("PDF loaded!")
        
        question = st.text_input("Ask a question about the document")
        if st.button("Ask"):
            if question:
                with st.spinner("Searching..."):
                    answer = ask_document(question, text)  # use text!
                st.markdown("### Answer:")
                st.info(answer)
            else:
                st.warning("Please ask a question!")
