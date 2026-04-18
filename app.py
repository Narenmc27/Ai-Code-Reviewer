import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def review_code(code):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert Python code reviewer. 
                When given code, provide:
                1. Bugs (if any)
                2. Improvements
                3. Best practices
                Keep feedback concise and clear."""
            },
            {
                "role": "user",
                "content": f"Review this Python code:\n{code}"
            }
        ]
    )
    return response.choices[0].message.content

st.title("🤖 AI Code Reviewer")
st.write("Paste your Python code below and get instant AI feedback!")

code = st.text_area("Your Code Here", height=300)

if st.button("Review My Code"):
    if code:
        with st.spinner("Reviewing..."):
            review = review_code(code)
        st.markdown("## 📝 Review:")
        st.markdown(review)
    else:
        st.warning("Please paste some code first!")
