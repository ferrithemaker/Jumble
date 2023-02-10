import pandas as pd
import pymongo
import credentials
import json

# load credentials for mongodb database
user = credentials.login['user']
password = credentials.login['password']
url = credentials.login['url']

# db connection
client = pymongo.MongoClient("mongodb+srv://"+user+":"+password+"@"+url+"/?retryWrites=true&w=majority")

db = client.movie_db
collection = db.movies

# read tsv files as dataFrames
# get files from https://datasets.imdbws.com/
df_basics = pd.read_csv("basics.tsv", sep="\t")
df_ratings = pd.read_csv("ratings.tsv", sep="\t")

# data filtering
movies_basics = df_basics[df_basics["titleType"] == "movie"][["tconst","primaryTitle","startYear","genres","runtimeMinutes"]]
ratings_basics = df_ratings[["tconst","averageRating"]]

# merging data
merged_movies = pd.merge(movies_basics, ratings_basics, on="tconst")

# clean ALL previous data
collection.delete_many({})

# convert dataframe to json and upload to mongodb
collection.insert_many(json.loads(merged_movies.to_json(orient = "records")))


