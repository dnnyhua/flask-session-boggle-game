from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def create_gameboard():
  """Home page where the game board will be created"""
  
  game_board = boggle_game.make_board()
  session['game_board'] = game_board
  highscore = session.get('highscore', 0)
  num_of_plays = session.get('num_of_plays',0)

  return render_template(
    'index.html', game_board=game_board, highscore=highscore, num_of_plays=num_of_plays)


@app.route('/check-submitted-word')
def check_word():
  """ Check if word is a valid answer """
  
  inputWord = request.args['inputWord']
  game_board = session['game_board']
  response = boggle_game.check_valid_word(game_board, inputWord)

  return jsonify({'result' : response})


@app.route('/post-score', methods=['POST'])
def post_score():
  """ update scores """

  score = request.json["score"]
  highscore = session.get('highscore',0)
  num_of_plays = session.get('num_of_plays',0)
  
  # update the num of plays in flask session so that when you start another game it will update to the correct value
  session['num_of_plays'] = num_of_plays + 1
  session['highscore'] = max(score, highscore) #max will return the value that is greater and assign it to 'highscore' in flask session

  # want to return a boolean so that we can decide how to update post game message on the DOM
  return jsonify(brokeRecord = score > highscore)
 