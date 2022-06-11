from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, HTTPException, Depends
import database
from schemas import RequestSchema, User, Review, AuthDetails
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from auth import AuthHandler 


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
        franchisorList = []
        for franchisor in result:
            franchisorList.append(
                {
                    "id_franchisor": franchisor[0],
                    "nama_usaha": franchisor[1],
                    "tags": franchisor[2],
                    "logo": franchisor[3],
                    "tanggal_berdiri": franchisor[4],
                    "email": franchisor[5],
                    "kontak": franchisor[6],
                    "deskripsi_usaha": franchisor[7],
                    "investment_cost": franchisor[8],
                    "lokasi": franchisor[9]
                }
            )

        return franchisorList
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
        franchisor = {
                        "id_franchisor": result[0][0],
                        "nama_usaha": result[0][1],
                        "tags": result[0][2],
                        "logo": result[0][3],
                        "tanggal_berdiri": result[0][4],
                        "email": result[0][5],
                        "kontak": result[0][6],
                        "deskripsi_usaha": result[0][7],
                        "investment_cost": result[0][8],
                        "lokasi": result[0][9]
                    }
                        
        return franchisor
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

        requestList = []
        for request in result:
            requestList.append(
                {
                    "id_request": request[0],
                    "id_user": request[1],
                    "id_franchisor": request[2],
                    "jumlah_invest": request[3],
                    "lokasi_tempat": request[4],
                    "luas_tempat": request[5],
                    "status": request[6]
                }
            )

        return requestList
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
            return {
                    "id_user": request.id_user,
                    "id_franchisor": request.id_franchisor,
                    "jumlah_invest": request.jumlah_invest,
                    "lokasi_tempat": request.lokasi_tempat,
                    "luas_tempat": request.luas_tempat,
                    "status": request.status
                    }         
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
        return {
            "id_review": result[0][0],
            "id_franchisor": result[0][1],
            "review": result[0][2],
            "sentimen": result[0][3]
        }
    except Exception as e:
        print(e)

@app.get("/getPerformanceIndex/{id}")
def get_PerformanceIndex(id: int):
    try:
        conn = database.open_connection()
        with conn.cursor() as cursor:
            query = "SELECT COUNT(*) FROM review WHERE sentimen = 'negative';"
            cursor.execute(query)
            result1 = jsonable_encoder(cursor.fetchall())
            sql = "SELECT COUNT(*) FROM review WHERE sentimen = 'positive';"
            cursor.execute(sql)
            result2 = jsonable_encoder(cursor.fetchall())
            index = result2 / (result1 + result2)
        conn.close()
        return {
            "performance_index": index
        }
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
        return "review added"
     
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
        return "account registered successfully"
    except Exception as e:
        print(e)

@app.post('/login')
def user_signIn(auth_details: AuthDetails):
    try: 
        conn = database.open_connection()
        with conn.cursor() as cursor:
            user = None
            username = "'"+auth_details.username+"'"
            password = "'"+auth_details.password+"'"
            jumlah_user = jsonable_encoder(cursor.execute("SELECT COUNT(*) FROM user WHERE username="+username+";").fetchall())
            
            if (jumlah_user[0][0] > 0):
                user = jsonable_encoder(cursor.execute("SELECT * FROM user WHERE username="+username+";").fetchall())
                token = auth_handler.encode_token(user[0][1])
            if (user is None) or (not auth_handler.verify_password(auth_details.password, user[0][2])):
                raise HTTPException(status_code=401, detail='Invalid username and/or password')
        
        return { "token": token }
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

        return {
            "id_user": result[0][0],
            "username": result[0][1],
            "password": result[0][2],
            "email": result[0][3],
            "nama": result[0][4]
        }
    except Exception as e:
        print(e)       


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)