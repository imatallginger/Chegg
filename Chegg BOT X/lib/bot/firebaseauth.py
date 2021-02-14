from firebase import firebase

firebase = firebase.FirebaseApplication('YOUR_LINK', None)


# Post
def addUser(userid, mail):
    data = {'mail': f'{mail}','question':''}
    result = firebase.put(f"users/", userid, data)
    return result


def getUser(userid):
    result = firebase.get('/users/', userid)
    return result
    # returns {'mail': 'random@protonmail.com'}


def getUserMail(userid):
    result = firebase.get("/users/", userid)
    return result["mail"]
    # Returns the "user@mail.com"


def updateMail(userid, mail):
    data = {'mail': f'{mail}','question':''}
    result = firebase.put(f"users/", userid, data)
    return result


def deleteUser(userid):
    result = firebase.delete("/users/", userid)
    return result

def addQuestion(userid, questionid):
    if getUser(userid) != None:
        result = firebase.put("users/", f"{userid}/question", questionid)
        return result
    else:
        return "Such user does not exist!"

def addAll(userid):
    firebase.put("users/", f"{userid}/question", "")

def updateQuestion(userid, questionid):
    if getUser(userid) != None:
        result = firebase.put("users/", f"{userid}/question", questionid)
        return result
    else:
        return "Such user does not exist!"

def getQuestion(userid):
    if getUser(userid) != None:
        result = firebase.get("/users/", userid)
        return result["question"]
    else:
        return "Such user does not exist!"

def deleteQuestion(userid):
    if getUser(userid) != None:
        result = firebase.put("users/", f"{userid}/question", "")
        return result

def fetchAllUsers():
    result = firebase.get('/users', None)
    return result