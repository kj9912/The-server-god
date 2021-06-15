import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from importer import get_quote

get_quote()


my_secret = os.environ['TOKEN']

client = discord.Client()


sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]


starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"

]

commands = [ 
"$inspire",
"$new",
"$del",
"$list",
"$police",
"$help"
]

if "responding" not in db.keys():
  db["responding"] = True

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
     encouragements = db["encouragements"]
     encouragements.append(encouraging_message)
     db["encouragements"] = encouragements 
  else:
    db["encouragements"] = [encouraging_message]

def delete_encoutagment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
      del encouragements[index]
      db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      # Her måtte jeg gå bort fra videoen
      options.extend(db["encouragements"])

        
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encoutagment(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)


  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)

  if msg.startswith("$police"):
    value = msg.split("$police ",1)[1]

    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("The sadnesspolice is active")
    elif value.lower() == "off":
      db["responding"] = False
      await message.channel.send("The sadnesspolice is taking a break")
    else:
      await message.channel.send("Invalid arguments. You can turn the police on or off. ")
  
  if msg.startswith("$help"):
    space = " "
    await message.channel.send("I listen for the following commands: " + space.join(commands))



 




keep_alive()
client.run(my_secret)
