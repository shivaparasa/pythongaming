from flask import Flask, render_template, request, session, jsonify
import random
import os
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

class NumberGame:
    def __init__(self):
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 10
        self.game_over = False
        self.message = ""
        self.min_range = 1
        self.max_range = 100
        self.score = 0
        self.hints_used = 0
        
    def start_new_game(self):
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_over = False
        self.score = 100
        self.hints_used = 0
        self.message = f"🎯 Guess a number between {self.min_range} and {self.max_range}! You have {self.max_attempts} attempts. Score: {self.score}"
        return self.message
    
    def get_hint(self):
        if self.game_over:
            return "Game is over! Start a new game."
        
        if self.hints_used >= 2:
            return "You've used both hints! Keep guessing!"
        
        self.hints_used += 1
        self.score -= 10
        
        if self.secret_number % 2 == 0:
            hint = f"The number is even. (Hint used: {self.hints_used}/2)"
        else:
            hint = f"The number is odd. (Hint used: {self.hints_used}/2)"
        
        return hint
    
    def make_guess(self, guess):
        if self.game_over:
            return "Game is over! Start a new game.", self.score
        
        if self.attempts >= self.max_attempts:
            self.game_over = True
            return f"❌ Game Over! You've used all {self.max_attempts} attempts. The number was {self.secret_number}. Your final score: {self.score}", self.score
        
        self.attempts += 1
        
        try:
            guess_num = int(guess)
        except ValueError:
            return f"❌ Invalid input! Please enter a number between {self.min_range} and {self.max_range}.", self.score
        
        if guess_num < self.min_range or guess_num > self.max_range:
            return f"❌ Please guess a number between {self.min_range} and {self.max_range}!", self.score
        
        if guess_num < self.secret_number:
            remaining = self.max_attempts - self.attempts
            return f"📈 Too low! Attempts: {self.attempts}/{self.max_attempts}. {remaining} attempts left. Score: {self.score}", self.score
        elif guess_num > self.secret_number:
            remaining = self.max_attempts - self.attempts
            return f"📉 Too high! Attempts: {self.attempts}/{self.max_attempts}. {remaining} attempts left. Score: {self.score}", self.score
        else:
            self.game_over = True
            points_earned = self.score + (self.max_attempts - self.attempts + 1) * 10
            self.score = points_earned
            return f"🎉 CONGRATULATIONS! You guessed {self.secret_number} in {self.attempts} attempts! Score: {self.score} points! 🎉", self.score
    
    def get_game_state(self):
        return {
            'type': 'number',
            'game_over': self.game_over,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'message': self.message,
            'min_range': self.min_range,
            'max_range': self.max_range,
            'score': self.score,
            'hints_used': self.hints_used
        }

class WordFindingGame:
    def __init__(self):
        self.words_db = {
            'python': 'A popular programming language 🐍',
            'flask': 'A lightweight web framework 🚀',
            'django': 'A high-level web framework 🎯',
            'javascript': 'Language of the web 🌐',
            'html': 'Structure of web pages 📄',
            'css': 'Styling language for web 🎨',
            'database': 'Stores organized data 💾',
            'algorithm': 'Step-by-step procedure 📊',
            'function': 'Reusable block of code 🔧',
            'variable': 'Stores data values 📦',
            'loop': 'Repeats code blocks 🔄',
            'array': 'List of items 📋'
        }
        self.current_word = None
        self.current_hint = None
        self.scrambled_word = None
        self.attempts = 0
        self.max_attempts = 6
        self.game_over = False
        self.message = ""
        self.score = 100
        self.hints_used = 0
        
    def start_new_game(self):
        self.current_word, self.current_hint = random.choice(list(self.words_db.items()))
        self.scrambled_word = self.scramble_word(self.current_word)
        self.attempts = 0
        self.game_over = False
        self.score = 100
        self.hints_used = 0
        self.message = f"🔤 Unscramble the word: '{self.scrambled_word}'\n📝 Hint: {self.current_hint}\nScore: {self.score}"
        return self.message
    
    def scramble_word(self, word):
        word_list = list(word)
        scrambled = word_list[:]
        while scrambled == word_list and len(word) > 1:
            random.shuffle(scrambled)
        return ''.join(scrambled)
    
    def get_hint(self):
        if self.game_over:
            return "Game is over! Start a new game."
        
        if self.hints_used >= 2:
            return "You've used both hints! Keep trying!"
        
        self.hints_used += 1
        self.score -= 10
        
        # Reveal first letter as hint
        hint = f"💡 The word starts with '{self.current_word[0]}' and has {len(self.current_word)} letters. (Hints used: {self.hints_used}/2)"
        return hint
    
    def make_guess(self, guess):
        if self.game_over:
            return "Game is over! Start a new game.", self.score
        
        if self.attempts >= self.max_attempts:
            self.game_over = True
            return f"❌ Game Over! The word was '{self.current_word}'. Your final score: {self.score}", self.score
        
        self.attempts += 1
        
        if guess.lower() == self.current_word:
            self.game_over = True
            points_earned = self.score + (self.max_attempts - self.attempts + 1) * 15
            self.score = points_earned
            return f"🎉 EXCELLENT! '{self.current_word}' is correct! Score: {self.score} points! 🎉", self.score
        else:
            remaining = self.max_attempts - self.attempts
            return f"❌ '{guess}' is incorrect! Attempts: {self.attempts}/{self.max_attempts}. {remaining} attempts left. Score: {self.score}", self.score
    
    def get_game_state(self):
        return {
            'type': 'word',
            'game_over': self.game_over,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'message': self.message,
            'scrambled_word': self.scrambled_word,
            'hint': self.current_hint,
            'score': self.score,
            'hints_used': self.hints_used,
            'word_length': len(self.current_word) if self.current_word else 0
        }

# Store game instances per session
games = {}

def get_game(session_id):
    if session_id not in games:
        games[session_id] = {'active_game': None, 'game_type': None}
    return games[session_id]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_game', methods=['POST'])
def select_game():
    session_id = request.headers.get('X-Session-ID', 'default')
    data = request.get_json()
    game_type = data.get('game_type')
    
    session_data = get_game(session_id)
    
    if game_type == 'number':
        session_data['active_game'] = NumberGame()
        session_data['game_type'] = 'number'
    elif game_type == 'word':
        session_data['active_game'] = WordFindingGame()
        session_data['game_type'] = 'word'
    else:
        return jsonify({'error': 'Invalid game type'}), 400
    
    session_data['active_game'].start_new_game()
    return jsonify(session_data['active_game'].get_game_state())

@app.route('/new_game', methods=['POST'])
def new_game():
    session_id = request.headers.get('X-Session-ID', 'default')
    session_data = get_game(session_id)
    
    if session_data['active_game']:
        session_data['active_game'].start_new_game()
        return jsonify(session_data['active_game'].get_game_state())
    else:
        return jsonify({'error': 'No game selected'}), 400

@app.route('/guess', methods=['POST'])
def guess():
    session_id = request.headers.get('X-Session-ID', 'default')
    session_data = get_game(session_id)
    
    if not session_data['active_game']:
        return jsonify({'error': 'No game selected'}), 400
    
    data = request.get_json()
    guess_value = data.get('guess', '')
    
    result_message, score = session_data['active_game'].make_guess(guess_value)
    session_data['active_game'].message = result_message
    
    return jsonify({
        'message': result_message,
        'game_state': session_data['active_game'].get_game_state()
    })

@app.route('/hint', methods=['POST'])
def hint():
    session_id = request.headers.get('X-Session-ID', 'default')
    session_data = get_game(session_id)
    
    if not session_data['active_game']:
        return jsonify({'error': 'No game selected'}), 400
    
    hint_message = session_data['active_game'].get_hint()
    
    return jsonify({
        'message': hint_message,
        'game_state': session_data['active_game'].get_game_state()
    })

@app.route('/game_state', methods=['GET'])
def game_state():
    session_id = request.headers.get('X-Session-ID', 'default')
    session_data = get_game(session_id)
    
    if not session_data['active_game']:
        return jsonify({'error': 'No game selected', 'game_selected': False})
    
    return jsonify(session_data['active_game'].get_game_state())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
