from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import database
from schemas import RequestSchema
from fastapi.encoders import jsonable_encoder



app = FastAPI()

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


@app.get("/franchisors/")
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

@app.get("/getRequest/")
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



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)