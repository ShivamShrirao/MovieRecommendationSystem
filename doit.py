import sys
import json
from tqdm import tqdm
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.moviemeta


with open("datasets/moviemeta_export.json","r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    lines[i] = json.loads(lines[i])

for i in tqdm(range(int(sys.argv[1]), int(sys.argv[2]))):
    db.movies.update_one({"id":lines[i]["id"]}, {"$set": {"idx": i}})
