#Python, librerias nativas
from typing import Optional
#pydantic
from pydantic import BaseModel
# fastApi
from fastapi import FastAPI
from fastapi import Body    
app = FastAPI()

#Models
class Person (BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional [str] = None
    is_married: Optional [bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}


#request and response BODY

@app.post("/person/new")
def create_person (person: Person = Body (...)):
    return person
