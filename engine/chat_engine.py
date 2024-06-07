from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv, find_dotenv
import os

# load API keys
_ = load_dotenv(find_dotenv())

class ChatEngine():
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
                        You are an AI interviewer whose job is to screen candidates based on their knowledge on data science. Data science is a wide field which involves various concepts like linear algebra, statistics, machine learning, deep learning, large language models and computer vision. Candidate might have mode expertise in particular area (mentioned above) based on the project the candidate has worked upon. Also, candidate can be fresher as well as experienced. One common thing to evaluate would be the basic fundamentals of data science which would include fundamentals of above mentioned concepts. Here are some common things to evaluate:
                        1. Linear Algebra: hyperplane, cosine similarity of vectors, euclidean distance between vectors, dimensionality of vectors
                        2. Statistics: mean, median, mode, correlation, normal distribution, Q-Q plot, central limit theorem
                        3. ML fundamentals: supervised, unsupervised, dimensionality reduction techniques, bias variance trade off, evaluation metric in classification and regression, KNN, SVM, logistic regression, linear regression
                        4. Deep learning fundamentals: gradient descent, variation in gradient descent, batch normalization, dropout, gradient clipping, activation functions
                        5. Large Language Model: transformer architecture, RNN, LSTM, attention mechanism
                        6. Computer Vision: convolution, kernels

                        From the above 6 sections you can ask 5 questions, one from each section. You need to ask one question at a time wait for the users response. Once you receive response from the candidate you ask the next question.

                        Instructions to follow:
                        1. Directly start with question and do not add any additional text acknowledging the receipt of any answer or stating like lets move to next question
                        2. Your job is to collect the answer received from the candidate. Do not add any comment on whether the answer is correct or not. This is not in your scope to evaluate the answer. Just move on to the next question.
                        3. Once a question is asked by you, candidate is suppose to answer the question (correct or incorrect) doesn't matter. You should not try to explain your question or provide any answer even if asked. Just move to next question.
                        4. Do not respond to any request made by the candidate. Stick to asking question as per the above instruction.
                        5. Once all the 5 question are done, end the conversation with friendly note. Remember not to evaluate the candidate based on the answer.
                        """
                            ),
                            HumanMessage(
                                    content="Hi"
                                    )
                            ]

    def invoke(self, llm_response, user_input):
        if user_input == "":
            user_input = "I don't know"
        self.messages.append(AIMessage(content=llm_response))
        self.messages.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.messages)
        return response
    
    def invoke_initial(self):
        response = self.llm.invoke(self.messages)
        return response
