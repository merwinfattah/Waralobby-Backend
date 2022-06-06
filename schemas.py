from pydantic import BaseModel

class RequestSchema(BaseModel):
    id_user: int
    id_franchisor: int
    jumlah_invest: int
    lokasi_tempat: str
    luas_tempat: float
    status: str