"""
Name: angry-walter.py 
Purpose: This is a 'Mad-Bomber' kind of Game
Copyright: 2016
Creator: Chris Hubbard
Note that this is a rewrite of the bomber.py that willie used to use
"""


from sopel.module import commands, OP, HALFOP
from random import choice, randint
from re import search
import sched
import time

colors = ['Red', 'Yellow', 'Blue', 'White', 'Black']
sch = sched.scheduler(time.time, time.sleep)
fuse = 120.0  # seconds
bombs = dict()

@commands('angry-walter')
def start(bot, trigger):
  """
  Put a bomb in the specified users pants.  They will be kicked if they
  don't guess the right wire fast enough.. VEG
  You have to specify the channel that you are doing this in.
  EXAMPLE: angry-walter #testing chubbard
  Note that Sopel must have ops to kick the user from the given channel.
  """
  # trigger.goup(2) is user supplied args
  if not trigger.group(2):
    return bot.msg(trigger.nick, 'Look at the help system.  This requires two arguments to work correctly')

  # format is #channel userid
  isChannelGiven = trigger.group(2)
  if not isChannelGiven.startswith('#'):
    return bot.msg(trigger.nick, "The #channel that the user is in is a manditory parameter")

  # split the channel from the user now
  channel=trigger.group(2).split()[0]
  target = trigger.group(2).split(' ')[1]

  # confirm that Sopel has ops to kick.
  #bot.msg(trigger.nick, "DEBUG: trigger sender " + trigger.sender +" bot nick "+ bot.nick +" channel "+ channel +" trigger nick "+ trigger.nick)
  if bot.privileges[channel][bot.nick] < HALFOP:
    return bot.reply("I'm not a channel operator for " + channel)

  global bombs
  global sch

  #  if target in bot.config.other_bots or target == bot.nick:
  if target == bot.nick:
    return bot.reply("As if I am dumb enough to blow myself up!")

  # One bomb at a time for a user
  if target in bombs:
    return bot.reply("I can't fit another bomb in " + target + "'s pants!")

  message = 'Hey, ' + target + '! Don\'t look but, I think there\'s a bomb in your pants. ' + str(fuse) + ' second timer and you see 5 wires: Red, Yellow, Blue, White and Black. Which wire should I cut? Don\'t worry, I know what I\'m doing! (respond with !cutwire color)'
  bot.say(message)
  color = choice(colors)

  # Inform the Client what color is the one to cut.
  bot.msg(trigger.nick,
     "Hey, don\'t tell %s, but the %s wire? Yeah, that\'s the one.  "
      "But shh! Don\'t say anything!" % (target, color))
  code = sch.enter(fuse, 1, explode, (bot, trigger))
  bombs[target.lower()] = (color, code)
  sch.run()

@commands('cutwire')
def cutwire(bot, trigger):
  """
  Tells the bot to cut a certain wire when you've been bombed.
  """
  # bot.msg('DEBUG: at cutwire breakpoint')
  global bombs, colors

  target = trigger.nick

  # If someone cuts a wire and we do not have a bomb on them  
  if target.lower() != bot.nick.lower() and target.lower() not in bombs:
    return bot.reply("You are lucky.  You are not currently one of my targets!  I will get you next time")

  # This somehow removes a target after they blow up, or cut the wire..  
  # Unsure of the logic, this was a holdover from bomb.py ( it works well, and I am lazy )  
  color, code = bombs.pop(target.lower()) 

  wirecut = trigger.group(2).rstrip(' ')
  if wirecut.capitalize() not in colors:
    # Add the target back onto the bomb list
    # Let the target know we could not parse the response to a specific color.
    bot.say('I can\'t seem to find that wire, ' + target + '! You sure you\'re picking the right one? It\'s not here!')
    bombs[target.lower()] = (color, code)
  elif wirecut.capitalize() == color:
    # Defuse the bomb
    bot.say('You did it, ' + target + '! I\'ll be honest, I thought you were dead. But nope, you did it. You picked the right one. Well done.')
    sch.cancel(code) 
  else:
    sch.cancel(code)  
    # defuse timer, execute premature detonation
    # trigger.sender should be the #channel
    kmsg = 'KICK ' + trigger.sender + ' ' + target + ' : No! No, that\'s the wrong one. Aww, you\'ve gone and killed yourself. Oh, that\'s... that\'s not good. No good at all, really. Wow. Sorry. (You should\'ve picked the ' + color + ' wire.)'
    bot.write([kmsg])

# This is a catchall if nothing is chosen and the timer expires.
def explode(bot, trigger):
  target = trigger.group(2).split(' ')[1]
  channel = trigger.group(2).split(' ')[0]
  bot.write(['KICK', channel, target, ' Oh, come on! ' + target + "! You could have at least TRIED to pick one!  Now you are DEAD!  Guts all over the place.  You see that?  There are guts all over your pants!  You should have picked the " + bombs[target.lower()][0] + " wire dumbass!!"])
  bombs.pop(target.lower())
