from flask import Flask, request, jsonify
import game
from tree import SearchTree
from flask_cors import CORS
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
CORS(app)
@app.route("/start-game", methods=['POST'])
def start_game():
	print('start game app.py')
	gameId = request.json['id']
	game.new_game(gameId)
	return jsonify({'status': 'success'})

@app.route("/make-move", methods=['POST'])
def respond_to_move():
	print('make move app.py')
	content = request.json
	gameId = content['id']
	userMoveStart = content['start square']
	userMoveEnd = content['end square']

	args = (gameId,userMoveStart,userMoveEnd)
	try:
		computerMove = game.handle_move_and_respond(*args)
		startSquare,endSquare = computerMove
		return jsonify({
			'status': 'success',
			'start square':startSquare,
			'end square':endSquare
		})
	except game.GameDeletedException:
		return jsonify({'status': 'failure'})


if __name__ == '__main__':
    # Debug/Development
    # app.run(host="0.0.0.0", port="8080")
    # Production
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()