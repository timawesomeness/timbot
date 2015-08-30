import socket, ssl, random, datetime, options, botcommands

server = options.server
port = options.port
channels = options.channels
botnick = options.botnick
password = options.serverpass

def parsetxt(txt):
    return bytes(txt, 'UTF-8')

def send(thing):
    ircsock.send(parsetxt(thing))

def auth(passwd):
    send("PASS " + passwd + "\n")

def ping():
    send("PONG :Pong\n")

def joinchans(chans):
    for chan in chans:
        send("JOIN " + chan + "\n")

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
    ircmsg = ircsock.recv(2048).decode('UTF-8')
    ircmsg = ircmsg.strip('\n\r')
    print(datetime.datetime.now().strftime("[%#I:%M:%S %p] ") + str(parsetxt(ircmsg)).strip('b\'').strip('\''))

    if ircmsg.find(' PRIVMSG ') != -1:
      nick = ircmsg.split('!')[0][1:]
      channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
      botcommands.findcommand(nick, channel, ircmsg)

    if ircmsg.find("PING :") != -1:
        ping()
