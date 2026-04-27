from flask import Flask, render_template, request, session, jsonify
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for production

class NumberGame:
    def __init__(self):
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 10
        self.game_over = False
        self.message = ""
        self.min_range = 1
        self.max_range = 100
        
    def start_new_game(self):
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_over = False
        self.message = f"Guess a number between {self.min_range} and {self.max_range}! You have {self.max_attempts} attempts."
        return self.message
    
    def make_guess(self, guess):
        if self.game_over:
            return "Game is over! Start a new game."
        
        if self.attempts >= self.max_attempts:
            self.game_over = True
            return f"Game Over! You've used all {self.max_attempts} attempts. The number was {self.secret_number}."
        
        self.attempts += 1
        
        try:
            guess_num = int(guess)
        except ValueError:
            return f"Invalid input! Please enter a number between {self.min_range} and {self.max_range}."
        
        if guess_num < self.min_range or guess_num > self.max_range:
            return f"Please guess a number between {self.min_range} and {self.max_range}!"
        
        if guess_num < self.secret_number:
            remaining = self.max_attempts - self.attempts
            return f"Too low! Attempts used: {self.attempts}/{self.max_attempts}. {remaining} attempts remaining."
        elif guess_num > self.secret_number:
            remaining = self.max_attempts - self.attempts
            return f"Too high! Attempts used: {self.attempts}/{self.max_attempts}. {remaining} attempts remaining."
        else:
            self.game_over = True
            return f"Congratulations! You guessed the number {self.secret_number} in {self.attempts} attempts! 🎉"
    
    def get_game_state(self):
        return {
            'game_over': self.game_over,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'message': self.message,
            'min_range': self.min_range,
            'max_range': self.max_range
        }

# Store game instances per session
games = {}

def get_game(session_id):
    if session_id not in games:
        games[session_id] = NumberGame()
        games[session_id].start_new_game()
    return games[session_id]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    session_id = request.headers.get('X-Session-ID', 'default')
    if session_id in games:
        games[session_id].start_new_game()
    else:
        games[session_id] = NumberGame()
        games[session_id].start_new_game()
    return jsonify(games[session_id].get_game_state())

@app.route('/guess', methods=['POST'])
def guess():
    session_id = request.headers.get('X-Session-ID', 'default')
    game = get_game(session_id)
    data = request.get_json()
    guess_value = data.get('guess', '')
    
    result_message = game.make_guess(guess_value)
    game.message = result_message
    
    return jsonify({
        'message': result_message,
        'game_state': game.get_game_state()
    })

@app.route('/game_state', methods=['GET'])
def game_state():
    session_id = request.headers.get('X-Session-ID', 'default')
    game = get_game(session_id)
    return jsonify(game.get_game_state())

if __name__ == '__main__':
    # Production-ready configuration
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
