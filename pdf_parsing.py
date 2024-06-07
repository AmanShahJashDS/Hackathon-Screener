import PyPDF2
import getpass
import os
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    # other params...
)


def extract_text_from_pdf(pdf_path):
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

def get_keywords_from_anthropic(resume_text):
    os.environ["anthropic_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")
    messages = [
    (
        "system",
        f"You are a recruiter reviewing a candidates job profile.",
    ),
    ("human", f"This is a  resume : {resume_text}. Extract the following information from the given resume in a list. [Years of Experience, Current Position if any else return student here, Give me another list of keyskills from this person's resume, Give me a list of skills used in this person's projects if he has any projects"),
    ]
    keywords = llm.invoke(messages)
    return keywords




# Example usage
pdf_path = 'dummy_resume.pdf'
extracted_text = extract_text_from_pdf(pdf_path)
# print(extracted_text)
Jobs = { "job_skills": "",
        }
keyword_from_resume = get_keywords_from_anthropic(extracted_text)
print(keyword_from_resume)