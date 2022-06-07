from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, HTTPException, Depends
import database
from schemas import RequestSchema, User, Review
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from auth import AuthHandler
from schemas import AuthDetails


app = FastAPI()

auth_handler = AuthHandler()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#db = database.Database()
#engine = db.get_db_connection()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/franchisors")
def get_AllFranchisor():
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM franchisor;')
            result = jsonable_encoder(cursor.fetchall())
        conn.close()

        return result
    except Exception as e:
        print(e)

@app.get("/franchisors/{id}")
def get_FranchisorById(id: int):
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            query = "SELECT * FROM franchisor WHERE id_franchisor="+str(id)+";"
            cursor.execute(query)
            result = jsonable_encoder(cursor.fetchall())
        conn.close()

        return result
    except Exception as e:
        print(e)

@app.get("/getRequest")
def get_AllRequest():
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM request;')
            result = jsonable_encoder(cursor.fetchall())
        conn.close()

        return result
    except Exception as e:
        print(e)

@app.post("/addRequest")
def add_request(request: RequestSchema):
    try:
            conn = database.open_connection()
            with conn.cursor() as cursor:
                    tempat = "'"+request.lokasi_tempat+"'"
                    status = "'"+request.status+"'"
                    query = "INSERT INTO request (id_user, id_franchisor, jumlah_invest, lokasi_tempat, luas_tempat, status) VALUES ("+str(request.id_user)+", "+str(request.id_franchisor)+", "+str(request.jumlah_invest)+", "+tempat+", "+str(request.luas_tempat)+", "+status+");"
                    cursor.execute(query)
            conn.commit()
            conn.close()
            return 
    except Exception as e:
            print(e)

@app.get("/getReview/{id}")
def get_AllReview(id: int):
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            query = "SELECT * FROM review WHERE id_franchisor="+str(id)+";"
            cursor.execute(query)
            result = jsonable_encoder(cursor.fetchall())
        conn.close()
        return result
    except Exception as e:
        print(e)

@app.post("/addReview")
def add_review(request: Review):
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            review_user = "'"+request.review+"'"
            sentimen = "'"+request.sentimen+"'"
            query = "INSERT INTO review (id_franchisor, review, sentimen) VALUES ("+str(request.id_franchisor)+", "+review_user+", "+sentimen+");"
            cursor.execute(query)
        conn.commit()
        conn.close()
        return
    except Exception as e:
        print(e)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post("/register")
def user_signUp(request: User):
    try: 
        conn = database.open_connection()
        with conn.cursor() as cursor:
            username = "'"+request.username+"'"
            nama = "'"+request.nama+"'"
            email = "'"+request.email+"'"
            password = "'"+request.password+"'"
            hashedPassword = "'"+pwd_context.hash(password)+"'"
            query = "INSERT INTO user (username, password, email, nama) VALUES ("+username+", "+hashedPassword+", "+email+", "+nama+");"
            cursor.execute(query)
        conn.commit()
        conn.close()
        return
    except Exception as e:
        print(e)

@app.post('/login')
def user_signIn(auth_details: AuthDetails):
    try: 
        conn = database.open_connection()
        with conn.cursor() as cursor:
            username = "'"+auth_details.username+"'"
            password = "'"+auth_details.password+"'"
            query = "SELECT * FROM user WHERE username="+username+";"
            cursor.execute(query)
            result = jsonable_encoder(cursor.fetchall())
            verifiedPassword = "'"+auth_handler.verify_password(auth_details.password, result[0][2])+"'"
            
            query2 = "SELECT * FROM user WHERE username="+username+" AND password="+verifiedPassword+" ;"
            cursor.execute(query2)
            result2 = jsonable_encoder(cursor.fetchall())
            if not result2:
                raise HTTPException(status_code=401, detail='Invalid username and/or password')
            
            else:
                token = auth_handler.encode_token('username')
                return { 'token': token }
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
   

@app.get("/user/{id}")
def get_Profil_User(id: int):
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            query = "SELECT * FROM user WHERE id_user="+str(id)+";"
            cursor.execute(query)
            result = jsonable_encoder(cursor.fetchall())
        conn.close()

        return result
    except Exception as e:
        print(e)       


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)