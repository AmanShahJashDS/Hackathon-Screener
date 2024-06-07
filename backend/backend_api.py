from fastapi import FastAPI,Query, Depends, File, UploadFile
from datetime import datetime 
from sqlalchemy.orm import  Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from engine import GenEngine, ParseEngine
import json
from http.client import HTTPException

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


        insert_user_query = text("INSERT INTO screener.users (username, password , user_role ,org_id) VALUES (:user, :hashed_password, :user_role, :org_id)")
        db.execute(insert_user_query, {"user": user, "hashed_password":password, "user_role": user_role_id.lower() ,"org_id":org_id[0]})
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
                     db: Session = Depends(get_db)):
    try:
        
        # extract filename from file
        timestamp = str(datetime.now())
        filename = timestamp+pdf_file.filename

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

    try:

        job_req_query=text("SELECT primary_skills,secondary_skills,required_exp FROM screener.job_requirements where job_id='{}'".format(job_id))
        job_requirements = db.execute(job_req_query, {'job_id': job_id}).fetchone()
        
    except Exception as e:
        print(f"Exception occured while reading from Job Requirements table : {e}")
        return {"status_code": 400, "detail": "Error while reading from Job Requirements table"}

    # invoke parser engine
    try:
        resume_parser = ParseEngine()
        resume_response = resume_parser.invoke(file_path, job_requirements)
        resume_data = json.loads(resume_response.content.replace("\n", "").strip())

    except Exception as e:
        print(f"exception occured while parsing resume : {e}")
        return {"status_code": 400, "detail": "Error while Parsing Resume"}

    # invoke chat engine
    try:
        chat_engine = GenEngine()
        questions_response = chat_engine.invoke(resume_data["key_skills"], job_requirements)
        print(f"questions_response : {questions_response}")
        questions = json.loads(questions_response.content.replace("\n", "").strip())
    except Exception as e:
        print(f"exception occured while generating questions : {e}")
        return {"status_code": 400, "detail": "Error while Generating questions"}
    try:
        response_data = {
                    "jobs_data":questions["questions"],
                    "Success": True,
                    "timestamp": str(datetime.now()),
                }
        return response_data
    except Exception as e:
        print(str(e))
        return {"status_code": 400, "detail": "Error while Generating questions"}


        
    
