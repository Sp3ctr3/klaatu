import sys,wolframalpha
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import praw as p

class KBot(irc.IRCClient):
 def __init__(self,channel,wolf):
  self.nickname="klaatu"
  self.chan=channel
  self.wolf=wolf

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
  elif msg.startswith(self.nickname+ ":") and len(msg.split(":"))==2:
   query=str(msg.split(":")[1])
   try:
    result=next(self.wolf.query(query).results).text.encode('utf-8')
    self.msg(channel,result)
   except:
    self.msg(channel,"I'm sorry I can't answer that")

class KBotFactory(protocol.ClientFactory):
 def __init__(self,channel,wolf):
  self.channel=channel
  self.wolf=wolf

 def buildProtocol(self,addr):
  p=KBot(self.channel,self.wolf)
  p.factory=self
  return p

 def clientConnectionLost(self, connector, reason):
  connector.connect()

 def clientConnectionFailed(self, connector, reason):
  reactor.stop()

if __name__ == '__main__':
 if len(sys.argv)==3:
  r=p.Reddit(user_agent="klaatu")
  client=wolframalpha.Client("Wolfram Key")
  f = KBotFactory("#"+sys.argv[2],client)
  reactor.connectTCP(sys.argv[1], 6667, f)
  reactor.run()
 else:
  print "Incorrect syntax" 
  sys.exit()
