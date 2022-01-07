import json
from src.database.schema import *

with open("./src/json_migration/localStorage.json", "r") as f:
    data = json.loads(f.read())['VoterHistory']

for user in data:
    username = user['username']
    yes = user['yes']
    no = user['no']
    print(f"{username} | yes: {str(yes)} | no: {str(no)}\n")
    new_user = User()
    new_user.username = username
    new_user.votes = [no,yes]
    new_user.save()