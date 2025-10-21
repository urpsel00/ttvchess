import board

import pickle

sessions = []

def SaveDatabase():
    global sessions
    with open("sessions.pkl", "wb") as f:
        pickle.dump(sessions, f)

def LoadDatabase():
    global sessions
    with open("sessions.pkl", "rb") as f:
        sessions = pickle.load(f)

def AddSession(username1: str, username2: str):
    global sessions
    sessions.append({"username1": username1, "username2": username2, "white": username1, "turn": username1, "board": board.Board()})

def GetSession(username1: str, username2: str):
    global sessions
    for session in sessions:
        if (username1 == session["username1"] and username2 == session["username2"]) or (username1 == session["username2"] and username2 == session["username1"]):
            return session

    return None

def GetSessions():
    global sessions
    return sessions