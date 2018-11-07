# RS-Econ
###### Runescape Economy Tracker
######~ *version: 1.04a [release]* ~

## What is it for?
* econ.py : Pulling economy information from both (OSRS & RS3) grand exchange.
* update_db.py : A 16+ hour long scan to update the item list. 

![demonstration](http://i.imgur.com/Jw8uzaq.png)

## Supports:
* item name searches
* Multiple item searches

## Future additions
* autoupdate + notifications on update
* flags and arguments

## Known Issues
* 32.9 second wait per item (This isn't actually a bug. Jagex throttles their API usage heavily.)

# Why is it cli-only?
It's temporary. If I come back to it, I'll make some type of gui. Although, this
would end up creating dependencies, something I'd rather not do.

## Requirements
* Python 2.7

