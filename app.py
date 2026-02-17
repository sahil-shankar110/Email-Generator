import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from EmailGenerator import Email_Generator
from Portfolio import Portfolio
from utils import clean_text

def streamlit_app(llm, Portfolio, clean_text):
    st.title("📧 Email Generator")
    st.write("Generate Professional and personalized job application emails based on job postings and URLs")
    
    # Input fields
    name = st.text_input("Enter your name")
    gmail = st.text_input("Enter your email address")
    url_input = st.text_input("Enter job posting URL")
    
    if st.button("Generate Email"):
        # Basic validation
        if not name or not gmail or not url_input:
            st.error("Please enter name, email address, and URL")
            return
        
        try:
            # Show loading
            with st.spinner("Generating email..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                Portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                if not jobs:
                    st.error("Could not extract job information from URL")
                    return
                
                # Generate emails
                for job in jobs:
                    skills = job.get("skills", {})
                    Portfolio_urls = Portfolio.query_links(skills)
                    email = llm.Write_email(job, Portfolio_urls, name, gmail)
                    
                    st.success("Email generated!")
                    st.code(email, language="markdown")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    Email_Generator = Email_Generator()
    Portfolio = Portfolio(file_path="./Sample_links.csv")
    st.set_page_config(page_title="Email Generator", page_icon="📧")
    streamlit_app(Email_Generator, Portfolio, clean_text)