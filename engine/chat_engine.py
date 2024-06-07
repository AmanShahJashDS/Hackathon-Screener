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
                        ###### JD ######
                        Designation: # designation name
                        Experience: # Experience in Years

                        Primary Skills:

                        1. Machine Learning Algorithms
                        2. Statistical Methods
                        3. Python, R
                        4. Flask
                        5. Neural Network

                        Secondary Skills:
                        1. Pandas.
                        2. NoSQL.
                        3. Data Analytics


                        ###### Resume ######
                        Candidate's Skill:
                        1. Machine learning
                        2. Deep learning
                        3. Computer Vision

                        ###### PROMPT ######
                        You are AI interviewer who need to generate questions given job description provided by recruiter 
                        and candidate's skill extracted from the resume.

                        Instruction to generate questions:
                        1. Questions should cover all the primary skills, some of the secondary skills and candidate's skills
                        2. Total 10 questions should be generated
                        3. Questions should be around fundamentals involved in the skills mentioned
                        4. Along with questions provide the skills on you are evaluating. Note: skills should be from the given context only.
                        """
                            ),
                            HumanMessage(
                                    content="Provide Question"
                                    )
                            ]

    def invoke(self):
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
                        You are a recruiter reviewing a candidates job profile.
                        """
                    ),
                    ]

    def invoke(self, pdf_path, cursor):
        resume_text = self.parse_resume(pdf_path)
        job_text = cursor.execute("query")
        self.messages.append(HumanMessage(
                                    content=f"""
                                    This is a  resume : {resume_text} 
                                    Extract the following information from the given resume 
                                    in a json. [The first key should be 'Years of Experience' if it doesn't show any experience 
                                    or if the candidate is a recent graduate give 0 give me answer as one number and nothing else, 
                                    The second key is 'Current Position' if any else return Student here,  and the third key is a 
                                    'Key Skills' this is a comma seprated list of five most relevant keyskills from this person's resume 
                                    to this job description {job_text}. I only want skills that are present in the resume and 
                                    relevant to the skills in {job_text} and it would be ideal if we have one skill from resume that is 
                                    relevant to a different skill in {job_text}. All skills should be present in the resume]
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
