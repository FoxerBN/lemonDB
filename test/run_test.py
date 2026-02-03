from app import LemonDB

schema = {
    "username": "string",
    "email": "string",
    "age": "integer",
    "premium": "boolean",
    "signup_date": "date"}

db = LemonDB(name="users", engine="csv", schema=schema)

user1 = ["Andrea Blinova","adka95652@gmail.com", 23, True, "2023-08-15"]

db.save(user1)