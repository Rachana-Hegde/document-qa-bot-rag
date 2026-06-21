import streamlit as st
from query import ask_question

st.set_page_config(
    page_title="Document Q&A Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("📚 Document Q&A Bot (RAG)")
st.write("Ask questions about the uploaded documents.")

question = st.text_input("Enter your question")

if st.button("Ask") and question:

    answer, citations, context = ask_question(question)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")
    for citation in citations:
        st.write(f"• {citation}")

    with st.expander("Retrieved Context"):
        st.write(context)