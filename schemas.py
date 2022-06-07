from pydantic import BaseModel
from typing import Optional

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

class Login(BaseModel):
    username:str
    password:str

class Review(BaseModel):
    id_franchisor:int
    review:str
    sentimen:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None