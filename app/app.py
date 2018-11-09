from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/seasons')
def seasons():
    return jsonify({
        2017: list(range(1, 13)),
        2018: list(range(1, 13)),
    })


@app.route('/ratings/<season>/<week>')
def ratings(season: int, week: int):
    return jsonify([
        dict(
            team="Nebraska Cornhuskers",
            rating=2000,
            variance=1,
            wins=12,
            losses=0,
            ties=0,
            previousRanking=1,
            gameResults=[
                dict(
                    opponent="Ohio State Buckeyes",
                    score=100,
                    opponentScore=1,
                )
            ]
        )
    ])


if __name__ == '__main__':
    app.run()
