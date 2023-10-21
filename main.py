from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel,Field
from typing import Optional, List

#estas son las importaciones para los tokens
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = 'Mi primera aplicación con FastAPI'
app.version = '0.0.1'

class JWTBearer(HTTPBearer):
    async def __call__(self, request:Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail='No tienes permiso')

class User(BaseModel):
    email:str=Field(...)
    password: str
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    genre: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'title': 'Pelicula de prueba',
                'overview': 'Esta es una descripcion de prueba',
                'year': 2023,
                'rating': 8.9,
                'genre': 'Accion'
            }
        }

movies = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        'overview': 'En un exuberante planeta llamado pandora viven los Na vi',
        "year": 1994,
        'rating': 7.8,
        'genre': ['Drama']
    },

    {
        "id": 2,
        "title": "The Shawshank Redemption",
        'overview': 'En un exuberante planeta llamado pandora viven los Na vi',
        "year": 1994,
        'rating': 7.8,
        'genre': ['Drama']
    }

]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')

@app.post('/login', tags=['auth'])
def login(user:User):
    if user.email == 'admin@gmail.com' and user.password=='admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies():
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item['id'] == id :
            return item
    return 'La pelicula no se encuentra'

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [item for item in movies if item['categoty'] == category]

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
        
    movies.append(movie)

    return movies


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie:Movie):
    for item in movies:
        if item['id'] == id :
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['genre'] = movie.genre
    
    return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id :
            movies.remove(item)
            return movies



        