import options

botnick = options.botnick

def findcommand(nick, channel, message):
    import timbot
    msg = decodemsg(message, channel)
    if  msg == ".duck":
        sendmsg(channel, pickduck())
    elif (msg == ".bang") and (channel == "#penguinpower" or channel == "#timawesomeness"):
        sendmsg(channel, nick + " you missed the duck completely.")
    elif msg == ".bamg" or msg == ".banf":
        sendmsg(channel, "Learn to type, " + nick)
    elif message.find(" :.murder ") != -1:
        murderee = message.split('.murder ')[1].strip(' ')
        if murderee == botnick:
            murderee = nick
            nick = botnick
        sendmsg(channel, murder(nick, murderee))
    elif msg == ".rolecall":
        sendmsg(channel, pickduck() + " here")
    elif (message.find(" :.join ") != -1) and ((nick == "timawesomeness") or (nick == "?timawesomeness")):
        joinchan(message.split('.join ')[1].strip(' '))
    elif (message.find(" :.part ") != -1) and ((nick == "timawesomeness") or (nick == "?timawesomeness")):
        partchan(message.split('.part ')[1].strip(' '))
    elif msg == ".timsource":
        sendmsg(channel, "https://github.com/timawesomeness/timbot")
    elif msg == ".nsa/win":
        sendmsg(channel, "I’d just like to interject for a moment. What you’re refering to as Windows, is in fact, NSA/Windows, or as I’ve recently taken to calling it, NSA plus Windows. Windows is not an operating system unto itself, but rather another locked down component of a fully functioning NSA system made useful by the NSA corelibs, shell utilities and vital system components comprising a full OS as defined by the government.")
    elif (message.split(channel + ' :')[1].find(botnick) != -1):
        sendmsg("~#local", botnick + " mentioned by " + nick + " in " + channel)
        sendmsg("~#local", "\"" + msg + "\"")
    elif (message.split(channel + ' :')[1].find("timawesomeness") != -1):
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

def decodemsg(message, channel):
    return message.split(channel + ' :')[1]

def sendmsg(chan, msg):
    import timbot
    print("Sending \"" + msg + "\" to " + chan)
    timbot.send("PRIVMSG " + chan + " :" + msg + "\n")

def joinchan(chan):
    import timbot
    print("Joining " + chan)
    timbot.send("JOIN " + chan + "\n")

def partchan(chan):
    import timbot
    print("Leaving " + chan)
    timbot.send("PART " + chan + "\n")
