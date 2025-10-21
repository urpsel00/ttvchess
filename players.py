import pickle

players = []

def SaveDatabase():
    global players
    with open("players.pkl", "wb") as f:
        pickle.dump(players, f)

def LoadDatabase():
    global players
    with open("players.pkl", "rb") as f:
        players = pickle.load(f)

def GetPlayer(username: str):
    global players
    for player in players:
        if player["username"] == username:
            return player
    return None

def CheckPlayer(username: str):
    global players
    for player in players:
        if player["username"] == username:
            return True
    return False

def AddPlayer(username: str, elo: int, layout: tuple[int, int]):
    global players
    if not CheckPlayer(username):
        players.append({"username": username, "elo": elo, "layout": layout})

def GetPlayers():
    global players
    return players

def SetLayout(username: str, layout: tuple[int, int]):
    global players
    for player in players:
        if player["username"] == username:
            player["layout"] = layout