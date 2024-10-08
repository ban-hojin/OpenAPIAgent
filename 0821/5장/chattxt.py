import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import openai

# OpenAI API 키 설정
OPENAI_API_KEY = ''
openai.api_key = OPENAI_API_KEY

# 텍스트 파일을 로드하는 함수
def load_text(uploaded_file):
    text = uploaded_file.read().decode('utf-8')
    return text

# Streamlit UI 설정
st.title("내부 문서 Q&A 시스템")

# 텍스트 파일 업로드 UI
uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type=["txt"])

if uploaded_file is not None:
    # 텍스트 파일 로드
    document = load_text(uploaded_file)
    # 문서를 리스트로 구성
    documents = [{"text": document}]    
    # 문서에서 임베딩(벡터화) 생성
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)    
    # FAISS 벡터 스토어 생성
    vector_store = FAISS.from_texts([doc["text"] for doc in documents], embeddings) 

    # 질문에 답변하는 체인 설정
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_store.as_retriever(), chain_type="stuff")  
    
    # 질문 입력 UI 및 답변 처리
    question = st.text_input("질문을 입력하세요:", 
        on_change=lambda: st.session_state.update({"answer": qa_chain({"query": st.session_state["question"]}) 
        if st.session_state["question"] else None}), key="question")
    
    # 답변 출력
    if "answer" in st.session_state and st.session_state["answer"] is not None:
        st.write("답변:", st.session_state["answer"]['result'])