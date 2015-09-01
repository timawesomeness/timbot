import socket, ssl, datetime, options, botcommands

server = options.server
port = options.port
channels = options.channels
botnick = options.botnick
password = options.serverpass

def parsetxt(txt):
    return bytes(txt, 'UTF-8')

def send(thing):
    ircsock.send(bytes(thing, 'UTF-8'))

def auth(passwd):
    send("PASS " + passwd + "\n")

def ping():
    send("PONG :Pong\n")

def joinchans(chans):
    for chan in chans:
        send("JOIN " + chan + "\n")

def joinchan(chan):
    print("Joining " + str(parsetxt(chan)).strip('b\'').strip('\''))
    send("JOIN " + chan + "\n")

def partchan(chan):
    print("Leaving " + str(parsetxt(chan)).strip('b\'').strip('\''))
    send("PART " + chan + "\n")

def sendmsg(chan, msg):
    print("Sending \"" + str(parsetxt(msg)).strip('b\'').strip('\'') + "\" to " + str(parsetxt(chan)).strip('b\'').strip('\''))
    send("PRIVMSG " + chan + " :" + msg + "\n")

# Connect, set nick, and join channels
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
ircsock = ssl.wrap_socket(s)
auth(password)
send("USER " + botnick + " " + botnick + " " + botnick + " :This bot is " + botnick + ", controlled by timawesomeness\n")
send("NICK " + botnick + "\n")
joinchans(channels)

#Main loop
while 1:
    ircmsg = ircsock.recv(2048).decode('UTF-8')
    ircmsg = ircmsg.strip('\n\r')
    print(datetime.datetime.now().strftime("[%#I:%M:%S %p] ") + str(parsetxt(ircmsg)).strip('b\'').strip('\''))

    if ircmsg.find(' PRIVMSG ') != -1:
        nick = ircmsg.split('!')[0][1:]
        channel = ircmsg.split(' PRIVMSG ', 1)[-1].split(' :', 1)[0]
        command, chan, output = botcommands.findcommand(nick, channel, ircmsg)
        if command == "SEND":
            sendmsg(chan, output)
        elif command == "SENDMULTI":
            for i in output:
                sendmsg(chan, i)
        elif command == "JOIN":
            joinchan(output)
        elif command == "PART":
            partchan(output)
        else:
            command, chan, output = "", "", ""

    if ircmsg.find("PING :") != -1:
        ping()
