import socket, ssl, random, datetime, options

server = options.server
port = options.port
channels = options.channels
botnick = options.botnick
password = options.serverpass

def commands(nick, channel, message):
    msg = decodemsg(message, channel)
    if  msg == ".duck":
        sendmsg(channel, pickduck())
    elif (msg == ".bang") and (channel == "#penguinpower" or channel == "#timawesomeness"):
        sendmsg(channel, nick + " you missed the duck completely.")
    elif msg == ".bamg":
        sendmsg(channel, "Learn to type, " + nick)
    elif message.find(parsetxt(" :.murder ")) != -1:
        murderee = message.split(parsetxt('.murder '))[1].strip(parsetxt(' ')).decode('UTF-8')
        if murderee == botnick:
            murderee = nick
            nick = botnick
        sendmsg(channel, murder(nick, murderee))
    elif msg == ".rolecall":
        sendmsg(channel, pickduck() + " here")
    elif (message.find(parsetxt(" :.join ")) != -1) and ((nick == "timawesomeness") or (nick == "?timawesomeness")):
        joinchan(message.split(parsetxt('.join '))[1].strip(parsetxt(' ')).decode('UTF-8'))
    elif (message.find(parsetxt(" :.part ")) != -1) and ((nick == "timawesomeness") or (nick == "?timawesomeness")):
        partchan(message.split(parsetxt('.part '))[1].strip(parsetxt(' ')).decode('UTF-8'))
    elif msg == ".timsource":
        sendmsg(channel, "https://github.com/timawesomeness/timbot")
    elif msg == ".nsa/win":
        sendmsg(channel, "I’d just like to interject for a moment. What you’re refering to as Windows, is in fact, NSA/Windows, or as I’ve recently taken to calling it, NSA plus Windows. Windows is not an operating system unto itself, but rather another locked down component of a fully functioning NSA system made useful by the NSA corelibs, shell utilities and vital system components comprising a full OS as defined by the government.")
    elif (message.split(parsetxt(channel + ' :'))[1].find(parsetxt(botnick)) != -1):
        sendmsg("~#local", botnick + " mentioned by " + nick + " in " + channel)
        sendmsg("~#local", "\"" + msg + "\"")
    elif (message.split(parsetxt(channel + ' :'))[1].find(parsetxt("timawesomeness")) != -1):
        sendmsg("~#local", "timawesomeness mentioned by " + nick + " in " + channel)
        sendmsg("~#local", "\"" + msg + "\"")
    elif (msg == ".killbutt") and ((nick == "timawesomeness") or (nick == "?timawesomeness")):
        print("\nKilled by " + nick)
        quit()

def murder(nick, murderee):
    num = random.randint(0,8)
    murders = {
        0: nick + " brutally murders " + murderee + " with a rusty axe.",
        1: nick + " brutally murders " + murderee + " with a chainsaw.",
        2: nick + " brutally murders " + murderee + " with a bloody scalpel.",
        3: nick + " brutally murders " + murderee + " with Winter_Fox.",
        4: nick + " brutally murders " + murderee + " with a large cleaver.",
        5: nick + " burns " + murderee + " to death with a napalm flamethrower.",
        6: nick + " brutally murders " + murderee + " with a nail gun.",
        7: nick + " brutally murders " + murderee + " using an electric chair.",
        8: nick + " brutally murders " + murderee + " with a .50 caliber pistol."
    }
    return murders[num]

def decodemsg(message, channel):
    return message.split(parsetxt(channel + ' :'))[1].decode('UTF-8')

def pickduck():
    num = random.randint(0,5)
    ducks = {
        0: "・゜゜・。。・゜ ​ ゜\_O​< QUA​CK!",
        1: "・゜゜・。。 ​ ・゜゜\_o<​ qu​ack!",
        2: "・゜゜・。。・゜ ​ ゜\_​ö< quac​k!",
        3: "・゜゜・。。・ ​ ゜゜\_o​< F​LAP FLAP!",
        4: "・゜゜ ​ ・。。・゜゜\_ó<​ qu​ack!",
        5: "・゜゜・。 ​ 。・゜゜\​_0< QUACK​!"
    }
    return ducks[num]

def parsetxt(txt):
    return bytes(txt, 'UTF-8')

def send(thing):
    ircsock.send(parsetxt(thing))

def auth(passwd):
    send("PASS " + passwd + "\n")

def ping():
    send("PONG :Pong\n")

def sendmsg(chan, msg):
    print(parsetxt("Sending \"" + msg + "\" to " + chan))
    send("PRIVMSG " + chan + " :" + msg + "\n")

def joinchans(chans):
    for chan in chans:
        send("JOIN " + chan + "\n")

def joinchan(chan):
    send("JOIN " + chan + "\n")

def partchan(chan):
    send("PART " + chan + "\n")

def hello():
    send("PRIVMSG " + channel + " :・゜゜・。。・゜ ​ ゜\_O​< QUA​CK!\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
ircsock = ssl.wrap_socket(s)
auth(password)
send("USER " + botnick + " " + botnick + " " + botnick + " :This bot is " + botnick + ", controlled by timawesomeness\n")
send("NICK " + botnick + "\n")

joinchans(channels)

while 1:
    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip(parsetxt('\n\r'))
    print(parsetxt(datetime.datetime.now().strftime("[%#I:%M:%S %p] ")) + ircmsg)

    if ircmsg.find(parsetxt(' PRIVMSG ')) != -1:
      nick = ircmsg.split(parsetxt('!'))[0][1:].decode('UTF-8')
      channel = ircmsg.split(parsetxt(' PRIVMSG '))[-1].split(parsetxt(' :'))[0].decode('UTF-8')
      commands(nick, channel, ircmsg)

    if ircmsg.find(parsetxt("PING :")) != -1:
        ping()
