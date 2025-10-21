import pickle

requests = []

def SaveDatabase():
    global requests
    with open("requests.pkl", "wb") as f:
        pickle.dump(requests, f)

def LoadDatabase():
    global requests
    with open("requests.pkl", "rb") as f:
        requests = pickle.load(f)

def AddRequest(username1: str, username2: str):
    global requests
    requests.append({"username1": username1, "username2": username2})

def DeleteRequest(username1: str, username2: str):
    global requests
    for request in requests[:]:
        if request["username1"] == username1 and request["username2"] == username2:
            requests.remove(request)

def GetRequests():
    return requests

def GetRequest(username1: str, username2: str):
    global requests
    for request in requests:
        if request["username1"] == username1 and request["username2"] == username2:
            return request
    return None