import players
import sessions
import requests
import board

import irc.bot

class Chatbot(irc.bot.SingleServerIRCBot):
    prefix = '#'

    def __init__(self, token):
        super().__init__([("irc.chat.twitch.tv", 6667, f'oauth:{token}')], "dummy", "dummy")

    def on_welcome(self, connection, event):
        print("on_welcome()")

        # load database

        players.LoadDatabase()
        requests.LoadDatabase()
        sessions.LoadDatabase()

        # join channels

        for player in players.GetPlayers():
            self.connection.join(f'#{player["username"]}')

    def on_pubmsg(self, connection, event):
        if players.CheckPlayer(event.source.nick):
            words = event.arguments[0].strip().split()
            if words and words[0].startswith(self.prefix):
                if f'#{event.source.nick}' == event.target:

                    # emoteset 

                    if words[0] == f'{self.prefix}emoteset':
                        if len(words) == 1:
                            self.connection.privmsg(event.target, "https://7tv.app/emote-sets/01K81670KVVWM8JG25JH9015P5")
                        else:
                            self.connection.privmsg(event.target, "emoteset accepts 0 arguments. (usage: #emoteset)") 


                    # layout

                    elif words[0] == f'{self.prefix}layout':
                        if len(words) == 1:
                            self.connection.privmsg(event.target, "T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T  . use #linebreaks to set the line breaks that match your current chat layout.")
                        else:
                            self.connection.privmsg(event.target, "layout accepts 0 arguments. (usage: #layout)") 

                    # linebreak

                    elif words[0] == f'{self.prefix}linebreaks':
                        if len(words) == 3 and words[1].isdigit() and words[2].isdigit():

                            if 0 < int(words[1]) and 8 <= int(words[2]):
                                players.SetLayout(event.source.nick, (int(words[1]), int(words[2])))
                                players.SaveDatabase()
                                self.connection.privmsg(event.target, "sucessfully set new linebreaks.") 
                            else:
                                self.connection.privmsg(event.target, "invalid linebreaks. second break must at least be 8 for the field to work.") 
                        else:
                            self.connection.privmsg(event.target, "linebreaks accepts 2 arguments. (usage: #linebreaks <first_break> <second_break>)") 

                    # testboard

                    elif words[0] == f'{self.prefix}testboard':
                        board.Board()
                        if len(words) == 1:
                            tb = board.Board()
                            self.connection.privmsg(event.target, tb.string(True, players.GetPlayer(event.source.nick)["layout"]))
                        else:
                            self.connection.privmsg(event.target, "testboard accepts 0 arguments. (usage: #testboard)") 

                    # request 

                    elif words[0] == f'{self.prefix}request':
                        if len(words) == 2:
                            if players.CheckPlayer(words[1]):
                                if requests.GetRequest(event.source.nick, words[1]) is None:
                                    if sessions.GetSession(event.source.nick, words[1]) is None:
                                        requests.AddRequest(event.source.nick, words[1])
                                        requests.SaveDatabase()
                                        self.connection.privmsg(f'#{words[1]}', f'{event.source.nick} challenged you to a match of chess. do you accept?')
                                    else:
                                        self.connection.privmsg(event.target, "invalid request. already in a session with you.")
                                else:
                                    self.connection.privmsg(event.target, "invalid request. player already has a pending request from you.")
                            else:
                                self.connection.privmsg(event.target, "invalid request. requested username is not subscribed.") 
                        else:
                            self.connection.privmsg(event.target, "request accepts 1 arguments. (usage: #request <username>)") 

                    # accept

                    elif words[0] == f'{self.prefix}accept':
                        if len(words) == 2:
                            if players.CheckPlayer(words[1]):
                                if requests.GetRequest(words[1], event.source.nick):
                                    if sessions.GetSession(event.source.nick, words[1]) is None:
                                        requests.DeleteRequest(words[1], event.source.nick)
                                        requests.SaveDatabase()

                                        sessions.AddSession(event.source.nick, words[1])
                                        sessions.SaveDatabase()

                                        self.connection.privmsg(f'#{event.source.nick}', f'accepted {words[1]}\'s request')
                                        self.connection.privmsg(f'#{words[1]}', f'{event.source.nick} accepted your request.')

                                        self.connection.privmsg(f'#{event.source.nick}', sessions.GetSession(event.source.nick, words[1])["board"].string(
                                            sessions.GetSession(event.source.nick, words[1])["white"] == event.source.nick,
                                            players.GetPlayer(event.source.nick)["layout"]
                                        ))
                                        self.connection.privmsg(f'#{words[1]}', sessions.GetSession(words[1], event.source.nick)["board"].string(
                                            sessions.GetSession(words[1], event.source.nick)["white"] == words[1],
                                            players.GetPlayer(words[1])["layout"]
                                        ))
                                    else:
                                        self.connection.privmsg(event.target, "invalid accept. session already exists.")
                                else:
                                    self.connection.privmsg(event.target, "invalid accept. no pending request from this user.")
                            else:
                                self.connection.privmsg(event.target, "invalid accept. accepted username is not subscribed.") 
                        else:
                            self.connection.privmsg(event.target, "request accepts 1 arguments. (usage: #request <username>)") 

                    # show 

                    elif words[0] == f'{self.prefix}show':
                        if len(words) == 2:
                            if players.CheckPlayer(words[1]):
                                if sessions.GetSession(event.source.nick, words[1]):
                                    self.connection.privmsg(f'#{event.source.nick}', sessions.GetSession(event.source.nick, words[1])["board"].string(
                                        sessions.GetSession(event.source.nick, words[1])["white"] == event.source.nick,
                                        players.GetPlayer(event.source.nick)["layout"]
                                    ))
                                else:
                                    self.connection.privmsg(event.target, "invalid show. no active session with this user.")
                            else:
                                self.connection.privmsg(event.target, "invalid show. accepted username is not subscribed.") 
                        else:
                            self.connection.privmsg(event.target, "show accepts 1 arguments. (usage: #show <username>)")

                    # move

                    elif words[0] == f'{self.prefix}move':
                        if len(words) == 3:
                            if players.CheckPlayer(words[1]):
                                if sessions.GetSession(event.source.nick, words[1]):
                                    if sessions.GetSession(event.source.nick, words[1])["turn"] == event.source.nick:
                                        status = sessions.GetSession(event.source.nick, words[1])["board"].move(words[2])
                                        
                                        if status == board.Status.Moved:
                                            self.connection.privmsg(f'#{event.source.nick}', sessions.GetSession(event.source.nick, words[1])["board"].string(
                                                sessions.GetSession(event.source.nick, words[1])["white"] == event.source.nick,
                                                players.GetPlayer(event.source.nick)["layout"]
                                            ))

                                            self.connection.privmsg(f'#{words[1]}', f'{event.source.nick} moved {words[2]}.')
                                            self.connection.privmsg(f'#{words[1]}', sessions.GetSession(words[1], event.source.nick)["board"].string(
                                                sessions.GetSession(words[1], event.source.nick)["white"] == words[1],
                                                players.GetPlayer(words[1])["layout"]
                                            ))

                                            sessions.GetSession(event.source.nick, words[1])["turn"] = words[1]
                                        elif status == board.Status.Illegal:
                                            self.connection.privmsg(event.target, "invalid move. illegal move.")
                                        else:
                                            self.connection.privmsg(event.target, "invalid move. internal error.")
                                    else:
                                        self.connection.privmsg(event.target, "invalid move. its not your turn.")
                                else:
                                    self.connection.privmsg(event.target, "invalid move. no active session with this user.")
                            else:
                                self.connection.privmsg(event.target, "invalid move. accepted username is not subscribed.") 
                        else:
                            self.connection.privmsg(event.target, "move accepts 2 arguments. (usage: #move <username> <notation>)") 

                    # unknown

                    else:
                        self.connection.privmsg(event.target, "unknown command.")
                else:
                    self.connection.privmsg(event.target, "you can only play from your own chat.")
        else:
            self.connection.privmsg(event.target, "the user is not subscribed.")