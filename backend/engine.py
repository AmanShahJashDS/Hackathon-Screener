from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv, find_dotenv
import os
import PyPDF2
from prompts import GEN_PROMPT, EVAL_PROMPT, PARSE_PROMPT 
# load API keys
_ = load_dotenv(find_dotenv())

class GenEngine():
    def __init__(self):
        MODEL_NAME = "claude-3-opus-20240229"
        self.llm = ChatAnthropic(
                    model=MODEL_NAME,
                    temperature=0,
                    max_tokens=1024,
                    timeout=None,
                    max_retries=2,
                    # other params...
                )
        self.messages = [
                            SystemMessage(
                                content=GEN_PROMPT
                            )
                            ]

    def invoke(self, skills, cursor, job_id):
        job_text = cursor.execute("query")
        self.messages.append(HumanMessage(
                                    content=f"""
                                    ### Job Description:
                                    {job_text}

                                    ### Candidate's Skill:
                                    {skills}
                                    """
                                    ))
        return self.llm.invoke(self.messages)
    
class ParseEngine():
    def __init__(self):
        MODEL_NAME = "claude-3-opus-20240229"
        self.llm = ChatAnthropic(
                    model=MODEL_NAME,
                    temperature=0,
                    max_tokens=1024,
                    timeout=None,
                    max_retries=2,
                    # other params...
                )

        self.messages = [
                    SystemMessage(
                                content=PARSE_PROMPT
                    ),
                    ]

    def invoke(self, pdf_path, cursor, job_id):
        resume_text = self.parse_resume(pdf_path)
        job_text = cursor.execute("query")
        self.messages.append(HumanMessage(
                                    content=f"""
                                    ### Resume:
                                    {resume_text}

                                    ### Job Description:
                                    {job_text}
                                    """
                                    ))
        return self.llm.invoke(self.messages)

    def parse_resume(self, pdf_path):
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Get the number of pages in the PDF
            num_pages = len(pdf_reader.pages)

            # Initialize a variable to store the extracted text
            text = ""

            # Loop through each page and extract text
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        return text


class EvalEngine():
    def __init__(self):
        MODEL_NAME = "claude-3-opus-20240229"
        self.llm = ChatAnthropic(
                    model=MODEL_NAME,
                    temperature=0,
                    max_tokens=1024,
                    timeout=None,
                    max_retries=2,
                    # other params...
                )

        self.messages = [
                    SystemMessage(
                                content=EVAL_PROMPT
                    ),
                    ]

    def invoke(self, qa_pairs):
        self.messages.append(HumanMessage(
                                    content=f"""
                                    {qa_pairs}
                                    """
                                    ))
        return self.llm.invoke(self.messages)
