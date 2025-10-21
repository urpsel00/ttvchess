import players
import chatbot
import requests
import sessions

import sys

def start(token: str):
    try:
        bot = chatbot.Chatbot(token)
        bot.start()
    except KeyboardInterrupt:
        bot.disconnect()
        print("interrupted.")

def invite(username: str):
    players.LoadDatabase()
    players.AddPlayer(username, 100, (5, 10))
    players.SaveDatabase()

def playerbase():
    players.LoadDatabase()
    print(players.GetPlayers())

def requestbase():
    requests.LoadDatabase()
    print(requests.GetRequests())

def sessionbase():
    sessions.LoadDatabase()
    print(sessions.GetSessions())

def setup():
    players.SaveDatabase()
    requests.SaveDatabase()
    sessions.SaveDatabase()

def main():
    if len(sys.argv) == 3 and sys.argv[1] == "start":
        start(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "invite":
        invite(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "playerbase":
        playerbase()
    elif len(sys.argv) == 2 and sys.argv[1] == "requestbase":
        requestbase()
    elif len(sys.argv) == 2 and sys.argv[1] == "sessionbase":
        sessionbase()
    elif len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
    else:
        print("abort: invalid number of arguments. (usage: python3 main.py <token>)")
        sys.exit(1)

if __name__ == "__main__":
    main()
