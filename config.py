import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-millionaire-game'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/millionaire_vietnam'
    
    # Game settings
    QUESTION_TIME_LIMIT = 60  
    LIFELINES = {
        'fifty_fifty': True,
        
    }
    
    
    PRIZE_MONEY = [
        200000,      
        400000,     
        600000,      
        1000000,     
        2000000,     
        3000000,     
        6000000,     
        10000000,    
        14000000,    
        22000000,    
        30000000,    
        40000000,    
        60000000,    
        85000000,    
        150000000    
    ]