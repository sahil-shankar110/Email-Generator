from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
class Email_Generator:
    def __init__(self):
        self.llm = ChatGroq(
            api_key= groq_api_key,
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.4,
            max_tokens=None,
            max_retries=2)

    def extract_jobs(self, url):
        prompt_extract = PromptTemplate.from_template(
            """
            I will give you scraped text from the job posting. 
            Your job is to extract the job details & requirements in a JSON format containing the following keys: 'role', 'experience', 'skills', and 'description'. 
            Only return valid JSON. No preamble, please.
            Here is the scraped text: {page_data}
            
            """)    

        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={ "page_data": url})

        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)

        except OutputParserException:
            raise OutputParserException("Unable to parse the model's response as JSON. Please check the response content for details.")
        return response if isinstance(response, list) else [response]
    
    def Write_email(self, job_description, portfolio_urls,name,gmail):
        prompt_email = PromptTemplate.from_template(
"""
You are a professional email writer. Write a clean, direct job application email.

    Candidate Name: {name}
    Candidate Contact: {gmail}
    Job Description: {job_description}
    Portfolio Projects: {portfolio_urls}

    Instructions:
    1. Subject line: "[Job Title] - [2-3 most relevant specific skills]"
    2. Opening: "I'm {name}, applying for [full job title]."
       - If company name is clearly available in job description, add "at [company name]"
       - If company name is NOT available, just write the job title only
    3. Skills paragraph: "My technical background includes [list 4-5 relevant skills from job description]."
    4. Projects:
       - Format: "I built/developed [project name] using [tech1, tech2, tech3] to [what it does]."
       - NO made up statistics, percentages, or numbers (if not needed)
       - URL on next line
    5. Closing: "I'd welcome the opportunity to discuss how I can contribute to your team."

    Rules:
    - 130-160 words
    - Be direct and factual
    - NO words: excited, thrilled, proud, passionate, strong, confident
    - NO phrases: "aligns well", "showcases", "demonstrates my ability"
    - NO made up numbers or accuracy percentages(unless clearly stated in project description)
    - NO bullet points
    - Professional but conversational

    End with:
    Best regards,
    {name}
    Contact: {gmail}

    Write ONLY the email:
    """
)
        chain_email = prompt_email | self.llm
        response = chain_email.invoke(input={ "name": name, "job_description": job_description, "portfolio_urls": portfolio_urls, "gmail": gmail})
        return response.content

        
    
        

