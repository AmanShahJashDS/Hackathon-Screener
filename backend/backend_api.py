from fastapi import FastAPI,Query, Depends, File, UploadFile
from datetime import datetime 
from sqlalchemy.orm import  Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from engine import GenEngine, ParseEngine, EvalEngine
import json
from http.client import HTTPException
from typing import List, Dict, Any
import logging

log = logging.getLogger("backend-apis")

UPLOAD_DIRECTORY = "/home/ec2-user/resumes"  

DB_HOST = 'screeners.c3iyi0cuiwty.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'jashds48'

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("db connected")
    except Exception as e:
        raise
    finally:
        db.close()
        
def shutdown_db_client():
    SessionLocal.close_all()


@app.post("/signup")
async def signup(
    user_role_id: str = Query(...),
    org_name:str = Query(...),
    org_desc:str = Query(...),
    user: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db)
):

    try:
        existing_user_query = text("SELECT * FROM screener.users WHERE username=:user")
        existing_user = db.execute(existing_user_query, {"user": user}).fetchall()

        if existing_user:
            return {"status_code": 409, "detail": "User already exists"}

        insert_org_query = text("INSERT INTO screener.organizations (name, org_desc) VALUES (:org_name, :org_desc)")
        db.execute(insert_org_query, {"org_name": org_name, "org_desc": org_desc})
        org_id_query = text("SELECT org_id FROM screener.organizations WHERE name=:org_name")
        org_id=db.execute(org_id_query, {"org_name": org_name}).fetchone()
        print(org_id)


        insert_user_query = text("INSERT INTO screener.users (username, password , user_role) VALUES (:user, :hashed_password, :user_role)")
        db.execute(insert_user_query, {"user": user, "hashed_password":password, "user_role": user_role_id.lower()})
        db.commit()

        return {
            "Success": True, 
            "message": "User signed up successfully"
        }
    except Exception as e:
        error_message = str(e)
        print("Error:", error_message)
        error_response = {
            "Success": False,
            "Timestamp": datetime.now(),
            "Error": error_message
        }
        return {"status_code": 400, "detail": error_response}

@app.get("/login")
async def login(
    user: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db)
):
    if not user or not password:
        return {"status_code": 409, "detail": "Incorrect email or password"}

    try:
        print(f"user : {user}")
        password_query = text("SELECT password FROM screener.users WHERE username='{}'".format(user))
        print(password_query)
        stored_password = db.execute(password_query,{"user": user}).fetchone()[0]
        
        print(f"password : {stored_password}")

        
        user_role_query=text("SELECT user_role FROM screener.users WHERE username ='{}'".format(user))
        user_role = db.execute(user_role_query,{"user": user}).fetchone()[0]
        print(f"user_role : {user_role}")

        if not stored_password:
            return {"status_code": 400, "detail": "Incorrect email or password"}
        else:
            print("password matched")
        
        if user_role=='candidate':
            organizations_query=text("SELECT name,org_id,org_desc FROM screener.organizations")
            organizations = db.execute(organizations_query).fetchall()
            print(organizations)
            organizations_data = [
                    {
                        "org_name": result.name,
                        "org_id": result.org_id,
                        "org_desc": result.org_desc
                    }
                    for result in organizations
                    if result.name != ""
                ]

            
            response_data = {
                "organizations_data":organizations_data,
                "username":user,
                "user_role":user_role,
                "Success": True,
                "timestamp": str(datetime.now()),
            }
            
            # elif user_role=='recruiter':
            
            return response_data
        else:
            return {"status_code": 400, "detail": "Incorrect email or password"}

    except Exception as e:
        error_message = str(e)
        print("Error:", error_message)
        error_response = {
            "Success": False,
            "Timestamp": str(datetime.now()),
            "Error": error_message
        }
        return {"status_code": f"exception raised : {e}"}


@app.get("/job_list")
async def list_jobs(
    org_id: str = Query(...),
    db: Session = Depends(get_db)
):  
    print(f" -- List Jobs API called with args : org_id : {org_id} --")
    try :
        jobs_query=text("SELECT job_role,job_id,job_status FROM screener.job_details WHERE org_id ='{}'".format(org_id))
        jobs = db.execute(jobs_query, {'org_id': org_id}).fetchall()
        print(f"jobs : {jobs}")
        jobs_data = []
        for result in jobs:
            print(f"result : {result}")
            try :
                job_req_query=text("SELECT primary_skills,secondary_skills,required_exp FROM screener.job_requirements where job_id='{}'".format(result.job_id))
                req_query = db.execute(job_req_query, {'job_id': result.job_id}).fetchone()

                print(f"req_query : {req_query}")

                job_data = {
                    "job_role": result.job_role,
                    "job_id": result.job_id,
                    "job_status": result.job_status,
                    "job_primary_skills": ','.join(req_query.primary_skills),
                    "job_secondary_skills": ','.join(req_query.secondary_skills),
                    "required_exp": req_query.required_exp
                }
                jobs_data.append(job_data)
            except Exception as e:
                print(f"error : {e}")
    
        response_data = {
                    "jobs_data":jobs_data,
                    "Success": True,
                    "timestamp": str(datetime.now()),
                }
        return response_data
    
    except Exception as e:

        error_message = str(e)
        print("Error:", error_message)
        error_response = {
            "Success": False,
            "Timestamp": str(datetime.now()),
            "Error": error_message
        }
        return {"status_code": f"exception raised : {e}"}

@app.post("/analysis")
async def upload_pdf(pdf_file: UploadFile = File(...),
                     job_id: str = Query(...),
                     org_id: str = Query(...),
                     user_name: str = Query(...),
                     db: Session = Depends(get_db)):

    print(f"-- Analysis API called with args : job_id : {job_id}, org_id : {org_id}, user_name : {user_name} --")

    # upload pdf file to server
    try:
        
        # extract filename from file
        start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"start_timestamp : {start_timestamp}")
        filename = start_timestamp+pdf_file.filename

        # check if file is pdf
        if not filename.endswith('.pdf'):
            return {"status_code": 400, "detail": "Invalid file type"}
        
        # upload file to server
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await pdf_file.read())

    except Exception as e:
        print(f"Exception occured while uploading file : {e}")
        return {"status_code": 400, "detail": "Error while uploading pdf file"}

    # get user_id from db
    try:
        user_id_query = text("SELECT user_id FROM screener.users WHERE username='{}'".format(user_name))
        user_id = db.execute(user_id_query, {'user_name': user_name}).fetchone()[0]
        print(f"user_id : {user_id}")

    except Exception as e:
        print(f"Exception occured while reading user_id from DB : {e}")
        return {"status_code": 400, "detail": "Error while reading user_id from DB for creating sessions"}
    
    # insert session details in db
    try:
        insert_session_query = text("insert into screener.sessions (job_id, user_id, session_start_date) values ({},{},'{}')".format(job_id, user_id,start_timestamp))

        db.execute(insert_session_query)
        db.commit()
        print("----->Session details inserted successfully into DB")

    except Exception as e:
        log.error(f"Exception occured while inserting data into DB : {e}")
        return {"status_code": 400, "detail": "Error while inserting session details into DB"}

    # get job requirements from db
    try:
        job_req_query=text("SELECT primary_skills,secondary_skills,required_exp FROM screener.job_requirements where job_id='{}'".format(job_id))
        job_requirements = db.execute(job_req_query, {'job_id': job_id}).fetchone()
        print(f"job_requirements : {job_requirements}")
        print(f"job requirements fetched successfully")
        
    except Exception as e:
        print(f"Exception occured while reading from Job Requirements table : {e}")
        return {"status_code": 400, "detail": "Error while reading from Job Requirements table"}

    # invoke parser engine
    try:
        resume_parser = ParseEngine()
        resume_response = resume_parser.invoke(file_path, job_requirements)
        resume_data = json.loads(resume_response.content.replace("\n", "").strip())
        print(f"resume_data parsed successfully")

    except Exception as e:
        print(f"exception occurred while parsing resume : {e}")
        return {"status_code": 400, "detail": "Error while Parsing Resume"}

    # invoke chat engine
    try:
        chat_engine = GenEngine()
        questions_response = chat_engine.invoke(resume_data["key_skills"], job_requirements)
        print(f"questions_response : {questions_response}")
        questions = json.loads(questions_response.content.replace("\n", "").strip())
        print(f"questions generated successfully")
    except Exception as e:
        print(f"exception occurred while generating questions : {e}")
        return {"status_code": 400, "detail": "Error while Generating questions"}
    try:
        response_data = {
                    "jobs_data":questions["questions"],
                    "Success": True,
                    "timestamp": str(datetime.now()),
                }
        print("----->returning response data")
        return response_data
    except Exception as e:
        print(str(e))
        return {"status_code": 400, "detail": "Error while Generating questions"}

@app.post("/submit")
async def submit(qa_pairs: List[Dict[str, str]], 
                user_name: str = Query(...),
                db: Session = Depends(get_db)):

    print(f"-----> Submit API called with args : qa_pairs : {qa_pairs}, user_name : {user_name} <-----")

    success = "false"
    
    end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # get user_id from db
    try:
        user_id_query = text("SELECT user_id FROM screener.users WHERE username='{}'".format(user_name))
        user_id = db.execute(user_id_query, {'user_name': user_name}).fetchone()[0]
        print(f"user_id : {user_id}")
    except Exception as e:
        print(f"Exception occurred while fetching user_id from DB : {e}")
        return {"status_code": 400, "detail": "Error while fetching user_id from DB"}

    # insert end_timestamp into db
    try:
        insert_end_timestamp_query = text("update screener.sessions set session_end_date = '{}' where user_id = {};".format(end_timestamp, user_id))
        db.execute(insert_end_timestamp_query)
        db.commit()
        print("----->session_end_date inserted successfully into DB")

    except Exception as e:
        print(f"Exception occurred while inserting session_end_date into DB : {e}")
        return {"status_code": 400, "detail": "Error while inserting session_end_date into DB"}

    # print("deleting data from table")

    # try :
    #     del_query = text("truncate table screener.session_qa CASCADE;")
    #     db.execute(del_query)
    #     db.commit()
    # except Exception as e:
    #     print(f"Exception occurred while deleting data from table : {e}")
    #     return {"status_code": 400, "detail": "Error while deleting data from table"}

    # fetch session_id from db
    try:
        session_id_query = text("SELECT session_id FROM screener.sessions WHERE user_id = {} ORDER BY session_id DESC LIMIT 1;".format(user_id))
        session_id = db.execute(session_id_query).fetchone()[0]
        print(f"----->Session_id : {session_id}")

    except Exception as e:
        print(f"Exception occurred while fetching session_id from DB : {e}")
        return {"status_code": 400, "detail": "Error while fetching session_id from DB"}

    print("Proceeding to parse and evaluate the answers...")
    try:
        for qa in qa_pairs:
            print(f"qa : {qa}")
            question = qa["question"]
            answer = qa["ans"]

            insert_qa_query = text("insert into screener.session_qa (session_id, question, answer) values ({},'{}','{}')".format(session_id,question, answer));
            print(f"insert_qa_query : {insert_qa_query}")
            db.execute(insert_qa_query)
            db.commit()
            print("Data inserted successfully into DB for session_qa")
        
        print("All QA Data inserted successfully into DB - session_qa table")

    except Exception as e:
        print(f"Exception occurred while inserting data into DB : {e}")
        return {"status_code": 400, "detail": "Error while inserting data into DB for session_qa"}   
    

    # Evaluate the qa_pairs

    # get qa_id, question and answer from db
    qa_query = text("SELECT qa_id, question, answer FROM screener.session_qa where session_id = {};".format(session_id));
    qa_data = db.execute(qa_query).fetchall()
    print(f"qa_data : {qa_data}")

    qa = ""
    # create a list of questions and answers
    count_qa = 0;
    for id,q,a in qa_data:
        qa += f"QA_ID : {id}\nQuestion : {q}\nAnswer : {a} \n\n"
        count_qa += 1
        if count_qa == 10:
            break
    
    print(f"numbers of questios to be evaluated : {count_qa}")

    # invoke eval engine
    try:
        eval_engine = EvalEngine()
        eval_response = eval_engine.invoke(qa)
        print(f"eval_response : {eval_response}")
        print(f"eval_response content :", eval_response.content.replace('\n', '').strip())
        evaluations = json.loads(eval_response.content.replace("\n", "").strip())
        print(f"evaluations generated successfully")
    except Exception as e:
        print(f"exception occurred while evaluating answers : {e}")
        return {"status_code": 400, "detail": "Error while Evaluating answers"}

    # insert evaluations into db
    try:
        
        print("Inserting evaluations into DB")
        for key, value in evaluations.items():
            print(f"key : {key}")
            print(f"value : {value}")
            accuracy = value["accuracy"]
            problem_solving = value["problem_solving"]
            practical_application = value["practical_application"]
            efficiency_and_optimization = value["efficiency_and_optimization"]
            communication = value["communication"]
            overall_rating = value["overall_rating"]

            insert_eval_query = text("insert into screener.rating (session_id, qa_id, accuracy, problem_solving, practical_application, efficiency_and_optimization, communication, overall_rating) values ({},{},{},{},{},{},{},{})".format(session_id,key, accuracy, problem_solving, practical_application, efficiency_and_optimization, communication, overall_rating));
            db.execute(insert_eval_query)
            db.commit()

            success = "true"
        print("----->Evaluations inserted successfully into DB")

    except Exception as e:
        print(f"Exception occurred while inserting data into DB : {e}")
        return {"status_code": 400, "detail": "Error while inserting data into DB"}


    # fetch details report

    try:
        metric_query = text("""SELECT
                                AVG(CASE WHEN accuracy = -1 THEN NULL ELSE accuracy END) as "accuracy",
                                AVG(CASE WHEN problem_solving = -1 THEN NULL ELSE problem_solving END) as "problem_solving",
                                AVG(CASE WHEN practical_application = -1 THEN NULL ELSE practical_application END) as "practical_application",
                                AVG(CASE WHEN efficiency_and_optimization = -1 THEN NULL ELSE efficiency_and_optimization END) as "efficiency_and_optimization",
                                AVG(CASE WHEN communication = -1 THEN NULL ELSE communication END) as "communication",
                                AVG(CASE WHEN overall_rating = -1 THEN NULL ELSE overall_rating END) as "overall_rating"
                            FROM
                                screener.rating
                            where session_id = {};""".format(session_id))
        metrics = db.execute(metric_query).fetchall()
        
        metric_dict = {
            "accuracy": metrics[0][0] if metrics[0][0] else 0,
            "problem_solving": metrics[0][1] if metrics[0][1] else 0,
            "practical_application": metrics[0][2] if metrics[0][2] else 0,
            "efficiency_and_optimization": metrics[0][3] if metrics[0][3] else 0,
            "communication": metrics[0][4] if metrics[0][4] else 0,
            "overall_rating": metrics[0][5] if metrics[0][5] else 0
        }

        print(f"metrics : {metrics}")
        print(f"metric_dict : {metric_dict}")

        job_id_query = text("SELECT job_id FROM screener.sessions WHERE session_id = {}".format(session_id))
        job_id = db.execute(job_id_query).fetchone()[0]
        print(f"job_id : {job_id}")

        job_role_query = text("SELECT job_role FROM screener.job_details WHERE job_id = {}".format(job_id))
        job_role = db.execute(job_role_query).fetchone()[0]
        print(f"job_role : {job_role}")

        print("-----$$$$$$$$$$$$$$$$$$$$$$$$$$> Metrics fetched successfully from DB")

    except Exception as e:
        print(f"Exception occurred while fetching data from DB : {e}")
        return {"status_code": 400, "detail": "Error while fetching data from DB"}

    
    if success == "true":
        return {
            "Success": True,
            "user_id": user_id,
            "user_name": user_name,
            "session_id": session_id,
            "message": "Answers evaluated successfully",
            "metrics_dict": metric_dict
        }
    else :
        return {
            "Success": False,
            "message": "Error Occurred while evaluating answers"
        }
    
