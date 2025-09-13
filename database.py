from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")  


db = client["assessment_db"]  


employees_collection = db["employees"]  
