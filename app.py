
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import mongo, Question, Game
from config import Config
import random
import time

app = Flask(__name__)
app.config.from_object(Config)


mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    player_name = request.form.get('player_name', 'Anonymous')
    game_id = Game.create_game(player_name)
    session['game_id'] = str(game_id)
    session['start_time'] = time.time()
    return redirect(url_for('game'))

@app.route('/game')
def game():
    if 'game_id' not in session:
        return redirect(url_for('index'))
    
    game_id = session['game_id']
    game_data = Game.get_game(game_id)
    
    if not game_data:
        return redirect(url_for('index'))
    
    if game_data['completed']:
        return redirect(url_for('result'))
    
    current_level = game_data['current_level']
    question = Question.get_by_level(current_level)
    
  
  
    if not question:
        print("WARNING: No question found for level", current_level)
        question = {
            'question': f'Câu hỏi mẫu cho cấp độ {current_level}',
            'options': ['A. Lựa chọn 1', 'B. Lựa chọn 2', 'C. Lựa chọn 3', 'D. Lựa chọn 4'],
            'correct_answer': 'A. Lựa chọn 1'
        }
    
    # Calculate remaining time
    elapsed_time = int(time.time() - session.get('start_time', time.time()))
    remaining_time = max(0, Config.QUESTION_TIME_LIMIT - elapsed_time)
    
    return render_template(
        'game.html',
        game=game_data,
        question=question,
        current_prize=Config.PRIZE_MONEY[current_level-1],
        next_prize=Config.PRIZE_MONEY[current_level] if current_level < 15 else None,
        remaining_time=remaining_time,
        prize_money=Config.PRIZE_MONEY
    )
@app.route('/test_questions')
def test_questions():
    questions = []
    for i in range(1, 16):
        q = Question.get_by_level(i)
        if q:
            questions.append({
                'level': i,
                'question': q.get('question', 'Missing question'),
                'options': q.get('options', []),
                'correct_answer': q.get('correct_answer', '')
            })
        else:
            questions.append({
                'level': i,
                'question': 'Question not found',
                'options': [],
                'correct_answer': ''
            })
    
    return jsonify(questions)
@app.route('/answer', methods=['POST'])
def answer():
    if 'game_id' not in session:
        return redirect(url_for('index'))
    
    game_id = session['game_id']
    game_data = Game.get_game(game_id)
    
    if not game_data or game_data['completed']:
        return redirect(url_for('index'))
    
    selected_answer = request.form.get('answer')
    current_level = game_data['current_level']
    question = Question.get_by_level(current_level)
    
    
    elapsed_time = int(time.time() - session.get('start_time', time.time()))
    if elapsed_time > Config.QUESTION_TIME_LIMIT:
        
        update_data = {
            'completed': True,
            'won_amount': get_safe_haven_amount(current_level - 1)
        }
        Game.update_game(game_id, update_data)
        return redirect(url_for('result'))
    
    
    session['start_time'] = time.time()
    
    if selected_answer == question['correct_answer']:
  
        if current_level == 15:
           
            update_data = {
                'current_level': current_level + 1,
                'completed': True,
                'won_amount': Config.PRIZE_MONEY[14]  
            }
        else:
        
            update_data = {
                'current_level': current_level + 1,
                'won_amount': Config.PRIZE_MONEY[current_level - 1]
            }
        Game.update_game(game_id, update_data)
        return redirect(url_for('game'))
    else:
       
        update_data = {
            'completed': True,
            'won_amount': get_safe_haven_amount(current_level)
        }
        Game.update_game(game_id, update_data)
        return redirect(url_for('result'))

@app.route('/use_lifeline', methods=['POST'])
def use_lifeline():
    if 'game_id' not in session:
        return jsonify({'success': False, 'message': 'No active game'})
    
    game_id = session['game_id']
    game_data = Game.get_game(game_id)
    
    if not game_data or game_data['completed']:
        return jsonify({'success': False, 'message': 'Game already completed'})
    
    lifeline = request.form.get('lifeline')
    if not lifeline or not game_data['lifelines'].get(lifeline, False):
        return jsonify({'success': False, 'message': 'Lifeline not available'})
    
    current_level = game_data['current_level']
    question = Question.get_by_level(current_level)
    
    result = {}
    
    if lifeline == 'fifty_fifty':
        incorrect_options = [opt for opt in question['options'] if opt != question['correct_answer']]
        to_remove = random.sample(incorrect_options, 2)
        result = {'removed_options': to_remove}
    
    elif lifeline == 'phone_a_friend':
        if random.random() < 0.75:
            friend_answer = question['correct_answer']
        else:
            incorrect_options = [opt for opt in question['options'] if opt != question['correct_answer']]
            friend_answer = random.choice(incorrect_options)
        
        result = {'friend_answer': friend_answer}
    elif lifeline == 'ask_the_audience':
        
        audience_votes = {}
       
        correct_percentage = random.randint(40, 70)
        remaining_percentage = 100 - correct_percentage
        
   
        incorrect_options = [opt for opt in question['options'] if opt != question['correct_answer']]
       
        if len(incorrect_options) != 3:
           
            
            audience_votes[question['correct_answer']] = 60
            for i, option in enumerate(question['options']):
                if option != question['correct_answer']:
                    audience_votes[option] = 40 // (len(question['options']) - 1)
        else:
            
            random_percentages = [random.randint(1, remaining_percentage-2) for _ in range(2)]
            random_percentages.append(remaining_percentage - sum(random_percentages))
            
            audience_votes[question['correct_answer']] = correct_percentage
            for i, option in enumerate(incorrect_options):
                audience_votes[option] = random_percentages[i]
        
        result = {'audience_votes': audience_votes}
    
  
    Game.use_lifeline(game_id, lifeline)
    
    return jsonify({'success': True, 'result': result})

@app.route('/walk_away', methods=['POST'])
def walk_away():
    if 'game_id' not in session:
        return redirect(url_for('index'))
    
    game_id = session['game_id']
    game_data = Game.get_game(game_id)
    
    if not game_data or game_data['completed']:
        return redirect(url_for('index'))
    
    current_level = game_data['current_level']
    
    update_data = {
        'completed': True,
        'won_amount': Config.PRIZE_MONEY[current_level - 2] if current_level > 1 else 0
    }
    Game.update_game(game_id, update_data)
    
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'game_id' not in session:
        return redirect(url_for('index'))
    
    game_id = session['game_id']
    game_data = Game.get_game(game_id)
    
    if not game_data:
        return redirect(url_for('index'))
    
    return render_template('result.html', game=game_data)

def get_safe_haven_amount(current_level):
    """
    Returns the safe haven amount based on the current level.
    Safe havens are at levels 5 and 10.
    """
    if current_level >= 10:
        return Config.PRIZE_MONEY[9]  
    elif current_level >= 5:
        return Config.PRIZE_MONEY[4]  
    return 0

if __name__ == '__main__':
    app.run(debug=True)

