from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Initialize PyMongo without app
mongo = PyMongo()

class Question:
    @staticmethod
    # phương thức trả về tất cả câu hỏi từ bộ sưu tập question
    def get_all():
        return list(mongo.db.questions.find())
    
    @staticmethod
#  get_by_level(level): Phương thức này tìm câu hỏi theo cấp độ (level).
# if isinstance(level, str) and level.isdigit(): Kiểm tra nếu level là chuỗi và có thể chuyển đổi thành số nguyên. Nếu đúng, nó chuyển chuỗi thành số nguyên.
# mongo.db.questions.find_one({"level": level}): Truy vấn MongoDB để tìm một câu hỏi có trường level bằng với giá trị đã cho.
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
# use_lifeline(game_id, lifeline): Phương thức này đánh dấu một "lifeline" (trợ giúp) là đã sử dụng (ví dụ: fifty_fifty).
# f"lifelines.{lifeline}": Đây là cách sử dụng cú pháp động để cập nhật một trường trong tài liệu, với trường hợp này là trường lifelines cho các lifeline cụ thể (ví dụ: lifelines.fifty_fifty).
# {f"lifelines.{lifeline}": False}: Đánh dấu lifeline là đã sử dụng bằng cách gán giá trị False.
    def use_lifeline(game_id, lifeline):
        if isinstance(game_id, str):
            game_id = ObjectId(game_id)
        mongo.db.games.update_one(
            {"_id": game_id},
            {"$set": {f"lifelines.{lifeline}": False}}
        )