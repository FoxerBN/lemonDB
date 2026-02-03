from app import LemonDB

schema = {
    "username": "string",
    "email": "string",
    "age": "integer",
    "premium": "boolean"}

db = LemonDB(name="users", engine="csv", schema=schema)

user1 = ["Andrea Blinova","adka95652@gmail.com", 23, True]
user2 = ["Andrea Blinova","adka95652@gmail.com", 23, True]
user3 = ["Andrea Blinova","adka95652@gmail.com", 23, True]
db.save(user1)