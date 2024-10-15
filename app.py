from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/users/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/users/register/batch', methods=['POST'])
def register_batch_users():
    data = request.json
    count = data.get('count')

    if not count or count <= 0:
        return jsonify({"error": "Count must be a positive integer"}), 400

    start_time = time.time()

    for i in range(count):
        username = f'user_{i}'
        email = f'user_{i}@example.com'
        new_user = User(username=username, email=email)
        db.session.add(new_user)

    db.session.commit()
    elapsed_time = time.time() - start_time

    return jsonify({"message": f"{count} users registered successfully!", "elapsed_time": elapsed_time}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_li

    st = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_list), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
