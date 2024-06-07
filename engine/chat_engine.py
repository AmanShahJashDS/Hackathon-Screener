from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv, find_dotenv
import os
import PyPDF2

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
                                content="""
                        You are AI interviewer who need to generate questions given job description provided by recruiter and candidate's skill extracted from the resume.

                        Instruction to generate questions:
                        1. Questions should cover all the primary skills, some of the secondary skills and candidate's skills
                        2. Generate 20 question
                        3. Questions should be around fundamentals involved in the skills mentioned
                        4. Along with questions provide the skills on which you are evaluating. Note: skills should be from the given context only.

                        # Ouptut Format:
                        {"questions": [q1, q2, ...]}
                        """
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
                                content="""
                        You are provided with Resume of the candidate and Job description.
                        Job description has keys: Designation, Experience, Primary Skills, Secondary Skills

                        Extract following keywords from the resume which are matching with the Job Description:
                        1. Years of Experience
                        2. Key Skills

                        It would be ideal if we have one skill from resume that is relevant to a different skill in job description.

                        Output Format:
                        ### JSON
                        ```
                        {
                        "experience": # years of experience if provided, fresher if mentioned or Unknown of not mentioned 
                        "key_skills": # list of skills that are matching with job description, order by most relevant skills along with skills mentioned in job description
                        }
                        ```
                        """
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
