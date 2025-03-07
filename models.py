from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Initialize PyMongo without app
mongo = PyMongo()

class Question:
    @staticmethod
    def get_all():
        return list(mongo.db.questions.find())
    
    @staticmethod
    def get_by_level(level):
      
        if isinstance(level, str) and level.isdigit():
            level = int(level)
        return mongo.db.questions.find_one({"level": level})
    
    
        if isinstance(question_id, str):
            question_id = ObjectId(question_id)
        return mongo.db.questions.find_one({"_id": question_id})

class Game:
    @staticmethod
    def create_game(player_name):
        game = {
            "player_name": player_name,
            "current_level": 1,
            "lifelines": {
                "fifty_fifty": True,
               
            },
            "completed": False,
            "won_amount": 0
        }
        return mongo.db.games.insert_one(game).inserted_id
    
    @staticmethod
    def get_game(game_id):
        if isinstance(game_id, str):
            game_id = ObjectId(game_id)
        return mongo.db.games.find_one({"_id": game_id})
    
    @staticmethod
    def update_game(game_id, update_data):
        if isinstance(game_id, str):
            game_id = ObjectId(game_id)
        mongo.db.games.update_one(
            {"_id": game_id},
            {"$set": update_data}
        )
    
    @staticmethod
    def use_lifeline(game_id, lifeline):
        if isinstance(game_id, str):
            game_id = ObjectId(game_id)
        mongo.db.games.update_one(
            {"_id": game_id},
            {"$set": {f"lifelines.{lifeline}": False}}
        )