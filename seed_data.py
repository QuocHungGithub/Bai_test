# Thư Viện Flask
from flask import Flask 

# models
from models import mongo, Question

# config
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

def seed_questions():
    mongo.db.questions.delete_many({})
    
    questions = [
        {
            "level": 1,
            "question": "Thủ đô của Việt Nam là gì?",
            "options": ["A. Hà Nội", "B. Hồ Chí Minh", "C. Đà Nẵng", "D. Huế"],
            "correct_answer": "A. Hà Nội"
        },
        {
            "level": 2,
            "question": "Sông nào dài nhất Việt Nam?",
            "options": ["A. Sông Hồng", "B. Sông Mekong", "C. Sông Đồng Nai", "D. Sông Đà"],
            "correct_answer": "B. Sông Mekong"
        },
        {
            "level": 3,
            "question": "Việt Nam có bao nhiêu tỉnh thành?",
            "options": ["A. 58", "B. 63", "C. 64", "D. 65"],
            "correct_answer": "B. 63"
        },
        {
            "level": 4,
            "question": "Đâu là món ăn nổi tiếng của Việt Nam?",
            "options": ["A. Sushi", "B. Kimchi", "C. Phở", "D. Pizza"],
            "correct_answer": "C. Phở"
        },
        {
            "level": 5,
            "question": "Ai là người đầu tiên bay vào vũ trụ?",
            "options": ["A. Neil Armstrong", "B. Yuri Gagarin", "C. Phạm Tuân", "D. Alan Shepard"],
            "correct_answer": "B. Yuri Gagarin"
        },
        {
            "level": 6,
            "question": "Đâu là ngọn núi cao nhất Việt Nam?",
            "options": ["A. Phan Xi Păng", "B. Bà Đen", "C. Núi Bà", "D. Ngọc Linh"],
            "correct_answer": "A. Phan Xi Păng"
        },
        {
            "level": 7,
            "question": "Năm bao nhiêu Việt Nam giành độc lập?",
            "options": ["A. 1945", "B. 1954", "C. 1975", "D. 1986"],
            "correct_answer": "A. 1945"
        },
        {
            "level": 8,
            "question": "Đâu là loại tiền tệ của Việt Nam?",
            "options": ["A. Đô la", "B. Euro", "C. Đồng", "D. Yên"],
            "correct_answer": "C. Đồng"
        },
        {
            "level": 9,
            "question": "Ai là tác giả của Truyện Kiều?",
            "options": ["A. Hồ Xuân Hương", "B. Nguyễn Du", "C. Nguyễn Trãi", "D. Nguyễn Đình Chiểu"],
            "correct_answer": "B. Nguyễn Du"
        },
        {
            "level": 10,
            "question": "Đâu là di sản thiên nhiên thế giới ở Việt Nam?",
            "options": ["A. Phố cổ Hội An", "B. Vịnh Hạ Long", "C. Cố đô Huế", "D. Phong Nha Kẻ Bàng"],
            "correct_answer": "B. Vịnh Hạ Long"
        },
        {
            "level": 11,
            "question": "Nguyên tố hóa học nào chiếm tỉ lệ cao nhất trong không khí?",
            "options": ["A. Oxy", "B. Nitơ", "C. Hydro", "D. Carbon dioxide"],
            "correct_answer": "B. Nitơ"
        },
        {
            "level": 12,
            "question": "Đâu là hành tinh lớn nhất trong hệ mặt trời?",
            "options": ["A. Trái Đất", "B. Sao Thổ", "C. Sao Mộc", "D. Sao Hỏa"],
            "correct_answer": "C. Sao Mộc"
        },
        {
            "level": 13,
            "question": "Ai là người phát minh ra điện thoại?",
            "options": ["A. Thomas Edison", "B. Alexander Graham Bell", "C. Nikola Tesla", "D. Albert Einstein"],
            "correct_answer": "B. Alexander Graham Bell"
        },
        {
            "level": 14,
            "question": "Đâu là quốc gia đông dân nhất thế giới?",
            "options": ["A. Ấn Độ", "B. Trung Quốc", "C. Mỹ", "D. Indonesia"],
            "correct_answer": "B. Trung Quốc"
        },
        {
            "level": 15,
            "question": "Bộ phim nào đạt doanh thu cao nhất mọi thời đại?",
            "options": ["A. Avatar", "B. Avengers: Endgame", "C. Titanic", "D. Star Wars: The Force Awakens"],
            "correct_answer": "B. Avengers: Endgame"
        }
    ]
    
    for question in questions:
        mongo.db.questions.insert_one(question)
    
   

if __name__ == "__main__":
    with app.app_context():
        seed_questions()
       