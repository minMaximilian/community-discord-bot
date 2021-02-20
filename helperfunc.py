from databaseClient import usersDB

def generateProfile(userID):
        usersDB.insert_one({'id': userID, 'context': {'currency': 100, 'moderation': {'bans': 0, 'kicked': 0, 'warnings': {}}}})

def enoughCurrency(userID, amount):
    result = usersDB.find_one({'id': userID})
    if result:
        if result['context']['currency'] - amount >= 0:
            return True
        else:
            return False
    else:
        generateProfile(userID)
        if 100 - amount >= 0:
            return True
        else:
            return False