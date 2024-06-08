EVAL_PROMPT = """
Objective:
Evaluate the candidate's response to the given technical question based on key criteria to determine their understanding, problem-solving ability, and communication skills.

Key Evaluation Criteria:
1. Accuracy:

1.1 Correctness: Is the solution technically correct?
1.2 Completeness: Does it address all parts of the question?

2. Depth of Understanding:

2.1 Conceptual Clarity: Is there a clear understanding of underlying concepts?
2.2 Detail Orientation: Does the answer go beyond surface-level understanding?

3. Problem-Solving Approach:

3.1 Methodology: What approach is taken to solve the problem?
3.2 Logical Reasoning: Is the argument well-reasoned and justified?

4. Practical Application:

4.1 Real-World Relevance: Is there awareness of real-world applications?
4.2 Examples and Scenarios: Are relevant examples provided?

5. Efficiency and Optimization:

5.1 Performance Considerations: Are performance implications considered?
5.2 Scalability and Maintainability: Is there awareness of scalability and maintainability?

6. Communication:

6.1 Clarity and Precision: Is the explanation clear and easy to follow?
6.2 Terminology and Language: Is technical terminology used correctly?

Final Output:
Rate the answer in the range of 1-10 for Problem-Solving Approach, Practical Application, Efficiency and Optimization, Communication, Overall Rating. There might be case where rating is not applicable. Give -1 in that case.

Input Question Answer Pair Format:
id: # question id
Question: # question string
Answer: # answer string

Output Format:

{id: {
"accuracy": #rating int,
"problem_solving": #rating int,
"practical_application": #rating int:,
"efficiency_and_optimization": #rating int:,
"communication": #rating int,
"overall_rating": #rating int},
id: { #similar structure},
}

Instruction:
Just give output in JSON format without any explanation or template text.
"""

GEN_PROMPT="""
You are AI interviewer who need to generate questions given job description provided by recruiter and candidate's skill extracted from the resume.

Instruction to generate questions:
1. Questions should cover all the primary skills, some of the secondary skills and candidate's skills
2. Generate 10 questions
3. Questions should be around fundamentals involved in the skills mentioned

# Ouptut Format:

### JSON
```
{"questions": #List(string)}
```

Instruction:
Just give output in above JSON format without any explanation or template text.
"""

PARSE_PROMPT="""
You are provided with Resume of the candidate and Job description.
Job description has keys: Designation, Experience, Primary Skills, Secondary Skills

Extract following keywords from the resume which are matching with the Job Description:
1. Years of Experience
2. Key Skills

It would be ideal if we have one skill from resume that is relevant to a different skill in job description.

Output Format:
### JSON
```
{"experience": # years of experience if provided fresher if mentioned or Unknown of not mentioned, "key_skills": # list of skills that are matching with job description, order by most relevant skills along with skills mentioned in job description}
```

Instruction:
Just give output in json format without any explanation or template text.
"""