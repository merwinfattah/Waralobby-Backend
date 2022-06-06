from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import database
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

@



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)