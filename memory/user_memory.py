from pymongo import MongoClient

def user_memory(user: str):
    try:
        collection = MongoClient("localhost", 27017)["memory"]["users"]
        user_memory = collection.find_one({"_id": user})
        if user_memory is None:
            user_memory = {}
        return user_memory
    except:
        return {}
    
def get_db():
    return MongoClient("localhost", 27017)["memory"]["users"]