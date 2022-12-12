#Python, librerias nativas
from typing import Optional
from enum import Enum
#pydantic
from pydantic import BaseModel
from pydantic import Field
# fastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path  
from fastapi import status


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

#inheritance to class person and personOut 
class PersonBase (BaseModel):
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
    le=115
  
    )
    hair_color: Optional [HairColor] = Field (default=None)
    is_married: Optional [bool] = Field (default=None)


class Person (PersonBase):

    password: str = Field (
        ..., 
        min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Juan",
                "last_name": "Ganan",
                "age": 28,
                "hair_color": "black",
                "is_married": True,
                "password": "welcometoprogramming"
            }
        }

class PersonOut (PersonBase):
    pass

    
@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )

def home():
    return {"Hello": "World"}


#request and response BODY
#contraseña en response_model
@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person (person: Person = Body (...)):
    return person

#Validaciones: Query parameters

@app.get (
    path="/person/detail",
    status_code=status.HTTP_200_OK
)

def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Carlos"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=18
        )
): 
    return {name: age}

#validaciones: path Parameters

@app.get (
    path="/person/detail/{person_id}",
    status_code = status.HTTP_200_OK)
    
def show_person (
    person_id: int = Path (
     ...,
     gt=0,
     example=108
     )
    ):
    return {person_id: "It exists!"}

#validations: Request Body

@app.put (
    path="/person/{person_id}",
    status_code = status.HTTP_202_ACCEPTED )
def update_person (
    person_id: int = Path (
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=108
    ),
    person: Person = Body (...),
    Location: Location = (...)
):
    results = person.dict()
    results.update(Location.dict())

    return results
