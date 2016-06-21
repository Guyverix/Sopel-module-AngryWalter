# Sopel-module-AngryWalter
## Configuration:
None.  This module has no options.

## Installation:
Add the angry-walter.py file to the modules directory for Sopel, and re-start services.  It MAY be found on a reload, but I suspect it is unlikely.


## Operation:
Sopel MUST be an operator for this to work, otherwise she cannot kick whoever is being bombed.  She will complain about not having ops just like anyone else when she is asked to do this and she does not have the power. :)


### In channel:
.angry-walter #channel TARGET

This is what will show up in the channel:

(10:43:24 AM) Sopel: Hey, TARGET! Don't look but, I think there's a bomb in your pants. 
120.0 second timer and you see 5 wires: Red, Yellow, Blue, White and Black. 
Which wire should I cut? Don't worry, I know what I'm doing! (respond with !cutwire color)

### In private to the userid who started all this:

(10:44:37 AM) Sopel: Hey, don't tell TARGET, but the White wire? Yeah, that's the one.  But shh! Don't say anything!


### In private to Sopel:
.angry-walter #channel TARGET

This is not currently recommended.  There are odd behaviors being seen currently expecially if there are few users
or you are testing this on your local userid.


## Notes:
I have attempted to add debug logic into the script if people
have trouble and need to find the source of the problem. 


Simply uncomment the stuff that says DEBUG in it, and make sure
to watch your indents so that Sopel / Python does not complain.
Then comment them out again when you are done.


I am still learning Python, if you see oddball stuff it is likely due 
to me not knowing better, not me attempting to be tricky.


## Creator Etc section:
* Created by: Chris Hubbard
* Contact: guyverix@yahoo.com
* Created on: 03-01-2016
* Version: 0.1.0

This is a re-write of the "Bomber" module that used to be in place.  There 

were many problems with getting it to work, so a re-write was done instead.

