from chat_engine import ChatEngine

engine = ChatEngine()

def start_screen():
    return engine.invoke_initial()

def next_question(prev_question, user_ans):
    return engine.invoke(llm_response=prev_question, user_input=user_ans)

def final_submit(prev_question, user_ans):
    return engine.invoke(llm_response=prev_question, user_input=user_ans)