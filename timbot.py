#!/usr/bin/python3
#############################################################################
# Copyright 2015 timawesomeness                                             #
#                                                                           #
# Licensed under the Apache License, Version 2.0 (the "License");           #
# you may not use this file except in compliance with the License.          #
# You may obtain a copy of the License at                                   #
#                                                                           #
#  http://www.apache.org/licenses/LICENSE-2.0                               #
#                                                                           #
# Unless required by applicable law or agreed to in writing, software       #
# distributed under the License is distributed on an "AS IS" BASIS,         #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
# See the License for the specific language governing permissions and       #
# limitations under the License.                                            #
#############################################################################
import socket, ssl, datetime, options, botcommands, sys, time, signal, json, os.path
from random import randint

server = options.server
port = options.port
channels = options.channels
botnick = options.botnick
password = options.serverpass

if not os.path.exists('duckcount'):
    with open('duckcount', 'a') as newdcf:
        newdcf.write("{}")
        newdcf.close()

duckcountfile = open('duckcount', 'r+')
# duckcount = int(duckcountfile.read())
duckcount = json.loads(duckcountfile.read())

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
    send("PRIVMSG " + "~#sent" + " :" + "Sending \"" + str(parsetxt(msg)).strip('b\'').strip('\'') + "\" to " + str(parsetxt(chan)).strip('b\'').strip('\'') + "\n")
    send("PRIVMSG " + chan + " :" + msg + "\n")

def safeexit():
    duckcountfile.truncate(0)
    duckcountfile.seek(0)
    duckcountfile.write(json.dumps(duckcount))
    duckcountfile.close()
    sys.exit(0)

def sighandle(signal, frame):
    safeexit()

signal.signal(signal.SIGINT, sighandle)
# Connect, set nick, and join channels
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
ircsock = ssl.wrap_socket(s)
if (options.serverpass != ""): auth(password);
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
        elif command == "DCKCNT":
            if output in duckcount:
                duckcount[output]["count"] += 1
            else:
                duckcount[output] = {"count":1}
        elif command == "DCKFLS":
            if nick in duckcount:
                sendmsg(chan, "(" + nick + ") You have " + str(duckcount[nick]["count"]) + " duck fails.")
            else:
                sendmsg(chan, "(" + nick + ") You have 0 duck fails.")
        elif command == "TDCKFLS":
            num = 0
            for i in duckcount:
                num += duckcount[i]["count"]
            sendmsg(chan, "There have been " + str(num) + " duck fails.")
        elif command == "QUIT":
            safeexit()
        else:
            command, chan, output = "", "", ""

    if ircmsg.find("PING :") != -1:
        ping()

    if randint(0, 25) == 0:
        duckcountfile.truncate(0)
        duckcountfile.seek(0)
        duckcountfile.write(json.dumps(duckcount))
