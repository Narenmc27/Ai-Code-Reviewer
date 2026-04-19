import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
llm = ChatGroq(api_key=st.secrets["GROQ_API_KEY"], model="llama-3.3-70b-versatile")

# Code Reviewer function
def review_code(code):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert Python code reviewer. Provide: 1. Bugs 2. Improvements 3. Best practices. Keep it concise."},
            {"role": "user", "content": f"Review this Python code:\n{code}"}
        ]
    )
    return response.choices[0].message.content

# Flashcard Generator function
def generate_flashcards(topic):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate exactly 5 flashcards. Format: Q: question\nA: answer\n---"),
        ("human", "Generate flashcards for: {topic}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"topic": topic})

# UI
st.title("🤖 AI Learning Tools")

tab1, tab2 = st.tabs(["Code Reviewer", "Flashcard Generator"])

with tab1:
    st.header("🔍 Code Reviewer")
    code = st.text_area("Paste your Python code here", height=300)
    if st.button("Review My Code"):
        if code:
            with st.spinner("Reviewing..."):
                review = review_code(code)
            st.markdown("## 📝 Review:")
            st.markdown(review)
        else:
            st.warning("Please paste some code first!")

with tab2:
    st.header("📚 Flashcard Generator")
    topic = st.text_input("Enter a topic (e.g. Python lists, Machine Learning)")
    if st.button("Generate Flashcards"):
        if topic:
            with st.spinner("Generating..."):
                cards = generate_flashcards(topic)
            st.markdown("## 🃏 Flashcards:")
            st.markdown(cards)
        else:
            st.warning("Please enter a topic first!")
