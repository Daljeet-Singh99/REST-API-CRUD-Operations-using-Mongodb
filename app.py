from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
collection = db['users']


@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(collection.find())
    # Convert ObjectId to string for serialization
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        'id': data['id'],
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    try:
        collection.insert_one(user)
        return jsonify({'message': 'User created successfully'}), 201
    except:
        return jsonify({'message': 'User with that ID already exists'}), 409


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = collection.find_one({'id': id})
    if user:
        # Convert ObjectId to string for serialization
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = {
        'id': id,
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = collection.replace_one({'id': id}, user)
    if result.modified_count:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'id': id})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    if 'user_db' not in client.list_database_names():
        db = client['user_db']
        collection = db['users']
        # Create the unique index on email field
        collection.create_index('id', unique=True)
    
    app.run()

