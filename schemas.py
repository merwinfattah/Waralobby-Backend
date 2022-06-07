from pydantic import BaseModel

class RequestSchema(BaseModel):
    id_user: int
    id_franchisor: int
    jumlah_invest: int
    lokasi_tempat: str
    luas_tempat: float
    status: str

class User(BaseModel):
    username:str
    password:str
    nama:str
    email:str

class Review(BaseModel):
    id_franchisor:int
    review:str
    sentimen:str

class AuthDetails(BaseModel):
    username: str
    password: str