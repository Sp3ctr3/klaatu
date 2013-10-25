import sys
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import praw as p

class RedditBot(irc.IRCClient):
 def __init__(self,channel):
  self.nickname="klaatu"
  self.chan=channel

 def signedOn(self):
  self.join(self.chan)

 def privmsg(self,user,channel,msg):
  if msg.startswith(self.nickname+ ":") and len(msg.split(":"))==3:
   subr=str(msg.split(":")[1])
   hot_no=int(msg.split(":")[2])
   try:
    top=r.get_subreddit(subr).get_hot(limit=hot_no)
    for i in top:
     self.msg(channel,i.title.encode('utf-8')+" "+i.url.encode('utf-8'))
   except:
    self.msg(channel,"Couldn't process your request")
  else:
   self.msg(channel,"Incorrect format")

class RedditBotFactory(protocol.ClientFactory):
 def __init__(self,channel):
  self.channel=channel

 def buildProtocol(self,addr):
  p=RedditBot(self.channel)
  p.factory=self
  return p

 def clientConnectionLost(self, connector, reason):
  connector.connect()

 def clientConnectionFailed(self, connector, reason):
  reactor.stop()

if __name__ == '__main__':
 if len(sys.argv)==3:
  r=p.Reddit(user_agent="klaatu")
  f = RedditBotFactory("#"+sys.argv[2])
  reactor.connectTCP(sys.argv[1], 6667, f)
  reactor.run()
 else:
  print "Incorrect syntax" 
  sys.exit()
