def create_user(db, username, password_hash):
    return db.users.insert_one({
        "username": username,
        "password": password_hash
    })

def find_user_by_username(db, username):
    return db.users.find_one({"username": username})
