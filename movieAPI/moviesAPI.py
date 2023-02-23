from pydantic import BaseModel,Field

from flask import jsonify,request
from flask_openapi3 import OpenAPI,Tag
from flask_openapi3 import Info
from flask_openapi3.models.security import HTTPBearer

import pymongo
import credentials

# load credentials form mongodb database
user = credentials.login['user']
password = credentials.login['password']
url = credentials.login['url']

# db connection
client = pymongo.MongoClient("mongodb+srv://"+user+":"+password+"@"+url+"/?retryWrites=true&w=majority")
db = client.movie_db
collection = db.movies

# start of flask app
info = Info(title="IMDB movies API", version="0.0.1")
jwt = HTTPBearer(bearerFormat="JWT")

security_schemes = {"jwt": jwt}


class NotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Resource not found!", description="Exception Information")


app = OpenAPI(__name__,info = info,security_schemes=security_schemes, responses={"404": NotFoundResponse})

class MoviesQuery(BaseModel):
    genre: str = Field(description="Genre of the movie (Action, Horror, Comedy, Documentary, ...). Blank for all genres")
    rating_threshold: float = Field(description="Rating threshold from 0.0 to 10.0. Default 0.0")
    rating_direction: str =  Field(description="Defines the threshold rating filter direction (lower / higher). Default: higher")
    page: int = Field(description="Initial page of results. Default 1")
    per_page: int = Field(description="Number of results per page. Default 10")
    sort_key: str = Field(description="Sort key [primaryTitle,startYear,genres,runtimeMinutes,averageRating]")
    sort_method: str = Field(description="Sorting direction (asc / desc). Default asc")

class MovieQuery(BaseModel):
    idmovie: str = Field(description="ID (tconst) of the movie")

@app.route('/movies/<id>')
def movieid(id):
    movie = collection.find_one({"tconst": id})
    if (movie):
        output_json = {
            "title": movie["primaryTitle"],
            "release_date": movie["startYear"],
            "genres": movie["genres"],
            "length": movie["runtimeMinutes"],
            "rating": movie["averageRating"],
            "link": "https://www.imdb.com/title/" + movie["tconst"] + "/"
        }
        return jsonify({"result": output_json})
    else:
        return jsonify({"result": "id not found"})

@app.get('/movies',tags=[Tag(name="movies API", description="Get movies data from IMDB")])
def get_movies(query:MoviesQuery):
    """get movies
    get movies from IMDB database
    """
    rating_threshold = float(request.args.get('rating_threshold',0.0))
    rating_direction = request.args.get('rating_direction', 'higher')
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    sort_key = request.args.get('sort_key', 'primaryTitle')
    sort_method = request.args.get('sort_method', 'asc')

    # validate query data
    if rating_direction == "higher":
        order = "$gt"
    elif rating_direction == "lower":
        order = "$lt"
    else:
        return jsonify({"error": "rating_direction value error"})

    if sort_method == "asc":
        sd = 1
    elif sort_method == "desc":
        sd = -1
    else:
        return jsonify({"error": "sort_method value error"})

    # define the query
    cursor = collection. \
        find({"$and": [
        {"genres": {'$regex': query.genre.capitalize()}},
        {"averageRating": {order: float(rating_threshold)}}]}). \
        sort(sort_key, sd). \
        skip(per_page * (page - 1)).limit(per_page)

    output_json = []
    for movie in cursor:
        output_json.append(
            {
                "title": movie["primaryTitle"],
                "release_date": movie["startYear"],
                "genres": movie["genres"],
                "length": movie["runtimeMinutes"],
                "rating": movie["averageRating"],
                "link": "https://www.imdb.com/title/"+movie["tconst"]+"/"
            }
        )
    print("output",output_json)
    return jsonify({"result": output_json})


@app.get('/movie',tags=[Tag(name="movie by ID (tconst)", description="Get movie data from IMDB by ID (tconst)")])
def get_movie(query:MovieQuery):
    """get movie
    get movie from IMDB database by id (tconst)
    """
    movie = collection.find_one({"tconst": query.idmovie})
    if movie:
        output_json =  {
                "title": movie["primaryTitle"],
                "release_date": movie["startYear"],
                "genres": movie["genres"],
                "length": movie["runtimeMinutes"],
                "rating": movie["averageRating"],
                "link": "https://www.imdb.com/title/" + movie["tconst"] + "/"
            }
        return jsonify({"result": output_json})
    else:
        return jsonify({"result": "id not found"})

@app.post('/movies',tags=[Tag(name="movies API [POST]", description="Get movies data from IMDB")])
def post_movie(query:MoviesQuery):
    """get movies from HTML form (using POST)
        get movies from IMDB database
    """

    rating_threshold = float(request.form.get('rating_threshold', 0.0))
    rating_direction = request.form.get('rating_direction', 'higher')
    page = int(request.form.get("page", 1))
    per_page = int(request.form.get("per_page", 10))
    sort_key = request.form.get('sort_key', 'primaryTitle')
    sort_method = request.form.get('sort_method', 'asc')

    # validate query data
    if rating_direction == "higher":
        order = "$gt"
    elif rating_direction == "lower":
        order = "$lt"
    else:
        return jsonify({"error": "rating_direction value error"})

    if sort_method == "asc":
        sd = 1
    elif sort_method == "desc":
        sd = -1
    else:
        return jsonify({"error": "sort_method value error"})

    # define the query
    cursor = collection. \
        find({"$and": [
        {"genres": {'$regex': query.genre.capitalize()}},
        {"averageRating": {order: float(rating_threshold)}}]}). \
        sort(sort_key, sd). \
        skip(per_page * (page - 1)).limit(per_page)

    output_json = []
    for movie in cursor:
        output_json.append(
            {
                "title": movie["primaryTitle"],
                "release_date": movie["startYear"],
                "genres": movie["genres"],
                "length": movie["runtimeMinutes"],
                "rating": movie["averageRating"],
                "link": "https://www.imdb.com/title/" + movie["tconst"] + "/"
            }
        )
    return jsonify({"result": output_json})


app.run()
