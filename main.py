#Python, librerias nativas
from typing import Optional
from enum import Enum
#pydantic
from pydantic import BaseModel
from pydantic import Field
# fastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path  
app = FastAPI()

#Models

class HairColor (Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location (BaseModel):
    city: str = Field (
        ..., 
        min_length=1,
        max_length=50,
        example="Cartago"
        )
    state: str = Field (
        ..., 
        min_length=1,
        max_length=50,
        example="valle"
        )
    country: str = Field (
        ..., 
        min_length=1,
        max_length=50,
        example="Colombia"
        )

class Person (BaseModel):
    first_name: str = Field (
        ..., 
        min_length=1,
        max_length=50,
        )
    last_name: str= Field (
        ..., 
        min_length=1,
        max_length=50,
        )
    age: int = Field  (
        ...,
        gt=0,
        le=115,
    )
    hair_color: Optional [HairColor] = Field (default=None)
    is_married: Optional [bool] = Field (default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Juan",
                "last_name": "Ganan",
                "age": 28,
                "hair_color": "black",
                "is_married": True
            }
        }

@app.get("/")
def home():
    return {"Hello": "World"}


#request and response BODY

@app.post("/person/new")
def create_person (person: Person = Body (...)):
    return person

#Validaciones: Query parameters

@app.get ("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )
): 
    return {name: age}

#validaciones: path Parameters

@app.get ("/person/detail/{person_id}")
def show_person (
    person_id: int = Path (..., gt=0)
    ):
    return {person_id: "It exists!"}

#validations: Request Body

@app.put ("/person/{person_id}")
def update_person (
    person_id: int = Path (
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body (...),
    Location: Location = (...)
):
    results = person.dict()
    results.update(Location.dict())

    return results
