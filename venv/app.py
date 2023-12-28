from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import chatbot_logic

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/yourdb"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    existing_user = users.find_one({'name': request.json['name']})

    if existing_user is None:
        hashpass = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        users.insert({'name': request.json['name'], 'password': hashpass})
        return jsonify({"message": "User created successfully"}), 201

    return jsonify({"message": "User already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.json['name']})

    if login_user:
        if bcrypt.check_password_hash(login_user['password'], request.json['password']):
            return jsonify({"message": "Logged in successfully"}), 200

    return jsonify({"message": "Invalid username/password combination"}), 401


@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user = request.json.get('user')
    response = chatbot_logic.get_response(user_input, user)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
