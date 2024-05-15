from flask import Flask, request, jsonify
import pymongo
import datetime
import pandas as pd
from bson import ObjectId

app = Flask(__name__)

MONGO_URI = "mongodb+srv://aksh9881:newAkshay1234@cluster0.syakz2i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client['database_name']

users_collection = db['users']
movies_collection = db['movies']

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return jsonify({"message": "Login successful", "token": generate_token(user["_id"])})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data['token']
    user_id = verify_token(token)
    if user_id:
        return jsonify({"message": "Logout successful"})
    else:
        return jsonify({"error": "Invalid or expired token"}), 401

def generate_token(user_id):
    return str(user_id)

def verify_token(token):
    try:
        user_id = ObjectId(token)
    except:
        return None

    user_data = users_collection.find_one({"_id": user_id})
    if user_data:
        last_login = user_data['last_login']
        current_time = datetime.datetime.now().timestamp()
        if (current_time - last_login) < 3600:
            return user_id
    return None

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    existing_user = users_collection.find_one({"username": username})
    if not existing_user:
        new_user = {
            "username": username,
            "password": password,
            "last_login": datetime.datetime.now().timestamp(),
            "wishlist": []
        }
        result = users_collection.insert_one(new_user)
        user_id = result.inserted_id
        return jsonify({"message": "Signup successful", "token": generate_token(user_id)})
    else:
        return jsonify({"error": "User already exists"}), 400

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    token = data['token']
    movie_id = data['movieId']

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    user_data = users_collection.find_one({"_id": user_id})
    if movie_id in user_data['wishlist']:
        return jsonify({"error": "Movie already in wishlist"}), 400

    users_collection.update_one({"_id": user_id}, {"$push": {"wishlist": movie_id}})
    return jsonify({"message": "Movie added to wishlist"}), 200

@app.route('/delete_from_wishlist', methods=['POST'])
def delete_from_wishlist():
    data = request.get_json()
    token = data['token']
    movie_id = data['movieId']

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    users_collection.update_one({"_id": user_id}, {"$pull": {"wishlist": movie_id}})
    return jsonify({"message": "Movie removed from wishlist"}), 200

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    movies_result_list = []
    for movie in movies_collection.find({"title": {"$regex": query, "$options": "i"}}):
        movies_result_list.append({
            "id": str(movie["_id"]),
            "title": movie["title"],
            "genre": movie.get("genre", "N/A"),
            "rating": movie.get("rating", "N/A"),
            "year": movie.get("year", "N/A")
        })

    return jsonify(movies_result_list)



if __name__ == '__main__':
    app.run(debug=True)
