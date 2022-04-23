import discord, json, pyfiglet, time
from discord.ext import commands
from discord import Embed, DMChannel
import asyncio
from discord.ext import tasks
from datetime import datetime
from discord_slash import SlashCommand
from discord.errors import Forbidden
from typing import Optional
from random import choice as randchoice
from discord.ext import tasks
import randomstuff
from googletrans import Translator
import googletrans
from discord.ext.commands import has_any_role
import json, os, random
from discord.utils import get
from typing import Optional
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, DisabledCommand, RoleNotFound, MemberNotFound, MissingAnyRole, NotOwner


#INTENTS AND PREFIX
intents = discord.Intents.all()
prefix = "!"
bot = commands.Bot(command_prefix = prefix, intents = intents)
slash = SlashCommand(bot, sync_commands = True)
bot.remove_command("help")
os.chdir("D:\\Empty Bot")


#QUICK ACCESS DATA
embed_color = 0x080404
allowed = [914092837564481556] #For nuke channel command...
stuff = [':bouquet:',':ear_of_rice:',':potted_plant:',':tulip:',':rose:',':hibiscus:',':cherry_blossom:',':blossom:',':sunflower:',':shell:']
names = ['Jenny','Lauren','Humble','Dan','Matthew','Blacksmith','Clarke','Simon','Christian','Hector','Albert','Vader','Walker','Phillip']
randomitem = [':soccer:',':boomerang:',':yo_yo:',':badminton:',':lacrosse:',':roller_skate:',':musical_keyboard:',':video_game:',':dart:',':jigsaw:',':violin:',':microphone:',':trophy:',':video_camera:',':film_frames:',':fire_extinguisher:',':syringe:',':magic_wand:',':pill:',':sewing_needle:']
mainshop = [{"name":"Anda-Paratha","price":100,"description":"Economical"},
			{"name":"Kebab","price":200,"description":"Goes well with anything!"},
			{"name":"Shwarma","price":600,"description":"I don't know what to add here"},
			{"name":"Daal","price":250,"description":"Same here"},
			{"name":"Roti","price":150,"description":"And here"},
			{"name":"Chanay","price":750,"description":"And here"},
			{"name":"Hoes","price":6969,"description":"Bang bang"},
			{"name":"Astagfar","price":10,"description":"Be sure to get this after getting ze hoes"},
			{"name":"Alloo-Keema","price":1100,"description":"Zubair asked for this"}]
huntanimals = [':hamster:',':rabbit:',':fox:',':bear:',':chicken:',':baby_chick:',':hatching_chick:',0]
fishcate = [':fish:',':tropical_fish:',':blowfish:',0,':octopus:',':squid:',':dolphin:',':shark:']



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#FUNCTIONS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#TIME CONVERSION FUNCTION
def convert(time):
		pos = ["s","m","h","d"]

		time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

		unit = time[-1]

		if unit not in pos:
			return -1
		try:
			val = int(time[:-1])
		except:
			return -2

		return val * time_dict[unit]


#INITIATING USER DATABASE FUNCTION
async def open_account(user):
	users = await get_bank_data()
	
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["wallet"] = 0
		users[str(user.id)]["bank"] = 0

	with open("mainbank.json", "w") as f:
		json.dump(users,f)
	return True


#FETCHING USER DETAILS FUNCTION
async def get_bank_data():
	with open("mainbank.json", "r") as f:
		users = json.load(f)

	return users


#UPDATING USER DETAILS FUNCTION
async def update_bank(user, change = 0, mode = "wallet"):
	users = await get_bank_data()
	users [str(user.id)][mode] += change 

	with open("mainbank.json", "w") as f:
		json.dump(users,f)
	
	bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
	return bal


#BUYING FUNCTION
async def buy_this(user,item_name,amount):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			price = item["price"]
			break

	if name_ == None:
		return [False,1]

	cost = price*amount

	users = await get_bank_data()

	bal = await update_bank(user)

	if bal[0]<cost:
		return [False,2]

	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt + amount
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			index+=1 
		if t == None:
			obj = {"item":item_name , "amount" : amount}
			users[str(user.id)]["bag"].append(obj)
	except:
		obj = {"item":item_name , "amount" : amount}
		users[str(user.id)]["bag"] = [obj]        

	with open("mainbank.json","w") as f:
		json.dump(users,f)

	await update_bank(user,cost*-1,"wallet")

	return [True,"Worked"]


#SELLING FUNCTION
async def sell_this(user,item_name,amount,price = None):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			if price==None:
				price = 0.9* item["price"]
			break

	if name_ == None:
		return [False,1]

	cost = price*amount

	users = await get_bank_data()

	bal = await update_bank(user)


	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt - amount
				if new_amt < 0:
					return [False,2]
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			index+=1 
		if t == None:
			return [False,3]
	except:
		return [False,3]    

	with open("mainbank.json","w") as f:
		json.dump(users,f)

	await update_bank(user,cost,"wallet")

	return [True,"Worked"]


#HELP FUNCTIONS
def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("ctx"):
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

	params = " ".join(params)
	
	return f"```{cmd_and_aliases} {params}```"

async def format_page(menu, entries):
	fields = []

	for entry in entries:
		fields.append((entry.brief or "No description", syntax(entry)))

	return await write_page(menu, fields)

async def cmd_help(ctx, command):
	embed = Embed(title = f"Details for `{command}` command", color = embed_color)
	embed.add_field(name = "Command Syntax", value = syntax(command), inline = False)
	embed.add_field(name = "Command description", value = command.help, inline = False)
	await ctx.send(embed = embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#GENRAL COMMANDS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#GENERAL HELP COMMAND
@bot.command(name="help", help="Responds to the call of help.")
async def show_help(ctx, cmd: Optional[str]):
	if cmd is None:
		embed=Embed(title="Help", color= embed_color)
		embed.set_thumbnail(url = ctx.guild.me.avatar_url)
		embed.set_footer(text =f"Requested By {ctx.author.display_name}",icon_url=f"{ctx.author.avatar_url}")
		fields = [("Total Commands",f"I have a total of **{len(bot.commands)}** commands" , False),
					("Miscellaneous Commands","`ping`, `setnick`, `avatar`, `role`, `remindme`, `translate`", False),
					("Moderation Commands","`toggle`, `say`, `embed`, `kick`, `ban`, `nuke`" , False),
					("Functions","Ghost ping detector, modmail system, keyword reactions, word specific triggers and monitored dms.", False),
					("Economy","Use the command `!economy` to get a list of all economy functions and commands.", False),
					("Individual Commands Help", f"To view help for individual commands, use the following syntax \n```{ctx.prefix}help <command>```", False)]
		for name , value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await ctx.reply(embed=embed)
	
	else:
		if (command := get(bot.commands, name=cmd)):
			await cmd_help(ctx, command)

		else:
			await ctx.reply("That command does not exist!")


#ROLE COMMAND
@bot.command(name="role", help="Add or remove user roles.")
async def roles(ctx, target: discord.Member, role: discord.Role):
	try:	
		if role not in target.roles:
			await target.add_roles(role)
			embed = Embed(description=f"Added **{role.mention}** to **{target.mention}**", color=embed_color)
			await ctx.channel.send(embed=embed)

		else:
			await target.remove_roles(role)
			embed = Embed(description=f"Removed **{role.mention}** from **{target.mention}**",  color=embed_color)
			await ctx.channel.send(embed=embed)
	
	except Forbidden:
		embed = Embed(description=f"You cannot edit roles for {target.mention}", color=embed_color)
		await ctx.channel.send(embed=embed)


#TRANSLATE COMMAND
@bot.command(name="translate", aliases = ["t"], help= "Translate anything in any language.")
async def translate(ctx, lang, *sentence):
    lang = lang.lower()
    if lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:
        await ctx.reply("huh?")

    else:
	    text = ' '.join(sentence)
	    translator = Translator()
	    text_translated = translator.translate(text, dest= lang)
	    await ctx.reply(text_translated.text)


#SAY COMMAND
@bot.command(name="say", help = "Make the bot say anything.")
async def say(ctx, *, message):
	await ctx.channel.send(f"{message}")


#EMBED COMMAND
@bot.command(name="embed", help = "Make the bot send an embed.")
async def embed(ctx, *, message):
	embed = Embed(description = f"{message}", color = embed_color)
	await ctx.channel.send(embed=embed)


#TOGGLE COMMAND
@bot.command(name="toggle", help = "Enable or disable commands.")
@commands.is_owner()
async def toggle(ctx, *, command):
	command = bot.get_command(command)

	if command is None:
		await ctx.reply("That command does not exist!", delete_after=60)

	elif ctx.command == command:
		await ctx.reply("You cannot disable this command!",delete_after=60)

	else:
		command.enabled = not command.enabled
		ternary = "enabled" if command.enabled else "disabled"
		await ctx.reply(f"I have successfully **{ternary}** `{command.qualified_name}` command.")


#SETNICK COMMAND
@bot.command(name="setnick", help ="Change user nicknames")
async def set_nick(ctx, target: discord.Member, nickname):
	try:
		await target.edit(nick=nickname)
		embed = Embed(description=f"Changed **{target.name}#{target.discriminator}**'s name to **{nickname}**", color=embed_color)
		await ctx.channel.send(embed=embed)
	except Forbidden:
		await ctx.channel.send(f"I cant change **{target.name}#{target.discriminator}**'s name")


#NUKE COMAMND
@bot.command(name="nuke", help = "Delete channels without much effort.")
async def nuke(ctx, channel: discord.TextChannel = None):
	if ctx.author.id in allowed:	
		if channel == None:
			embed = Embed(description=f"**You did not mention a channel\n For example {ctx.channel.mention}**", color=0x000000)
			await ctx.reply(embed=embed)
			return

		nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

		if nuke_channel is not None:
			new_channel = await nuke_channel.clone(reason="Has been Nuked!")
			await nuke_channel.delete()
			nuke_channel_embed = Embed(description="**This channel has been nuked**",color=0x000000)
			nuke_channel_embed.set_image(url="https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif")
			await new_channel.send(embed=nuke_channel_embed)
			embed=Embed(description=f"**`{new_channel.name}` has been nuked sucessfully**", color=0x000000)
			await ctx.reply(embed=embed)

		else:
			emebd = Embed(description=f"**No channel named `{channel.name}` was found!**")
			await ctx.reply(embed=embed)

	else:
		embed = Embed(description="**Insufficient permissions to perform that task!**")
		await ctx.send(embed=embed) 


#REMIND-ME COMMAND
@bot.command(name="remindme", help = "Set a reminder for yourself.")
async def remindme(ctx, time, *, message):
	try:
		sleep_time = convert(time)

		try:
			await ctx.author.send(f"I will remind you after **{time}** with the message **{message}**")
			await ctx.channel.send("Check your dms...")
		
		except:
			await ctx.channel.send(f"I will remind you after **{time}** with the message **{message}** \n <:uhh:847601058904932362> Also enable your dms bruh")
		
		await asyncio.sleep(sleep_time)

		embed = Embed(title="Reminder",
			description=f"{message}",
			color=embed_color)
		try:
			await ctx.author.send(embed=embed)
		
		except:
			await ctx.channel.send(f"||{ctx.author.mention}||",embed=embed)

	except:
		return await ctx.channel.send("Please enter either `s`, `m`, `h` or `d` after the integer!")


#AVATAR COMMAND
@bot.command(name="avatar", help = "Displays user avatar.")
async def avatar(ctx, target: Optional[discord.Member]):
	target = target or ctx.author
	embed = Embed(title=f"{target.display_name}'s Avatar",url=f"{target.avatar_url}",color=embed_color)
	embed.set_image(url=f"{target.avatar_url}")
	await ctx.channel.send(embed = embed)


#PING COMMAND
@bot.command(name="ping", help = "Displays bot latency.")
async def ping(ctx):
	embed = Embed(description=f"Pong! Latency is **{round(bot.latency*1000)}** ms",color=embed_color)
	await ctx.channel.send(embed=embed)


#KICK COMMAND
@bot.command(name="kick", help = "Kick users from the server.")
async def kick(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.kick(reason = reason)
	embed = Embed(description=f"Successfully kicked **{target.name}#{target.discriminator}**", color=embed_color)
	await ctx.channel.send(embed=embed)


#BAN COMMAND
@bot.command(name="ban", help = "Ban users from the server.")
async def ban(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.ban(reason = reason)
	embed = Embed(description=f"Successfully banned **{target.name}#{target.discriminator}**", color=embed_color)
	await ctx.channel.send(embed=embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#SLASH COMMANDS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#HELP COMMAND [Slash]
@slash.slash(name="help", description = "Get a list of all available commands.")
async def show_help(ctx):
	guild = ctx.guild
	embed = Embed(title="Help",
		description=f"I have a total of **{len(bot.commands)}** commands \n My current prefix is **{prefix}**",
		color=embed_color)
	embed.add_field(name = "Miscellaneous Commands", value = " `ping`, `setnick`, `avatar`, `role`, `remindme`, `translate`", inline = False)
	embed.add_field(name = "Moderation Commands", value = "`kick`, `ban`", inline = False)
	embed.add_field(name = "Functions", value = "Ghost ping detector, Modmail system, Supports keyword reactions and word specific triggers", inline = False)
	embed.add_field(name = "Developer", value = "<@914092837564481556>", inline = False)
	embed.set_thumbnail(url = guild.me.avatar_url)
	await ctx.send(embed=embed)


#ROLE COMMAND [Slash]
@slash.slash(name="role", description="Add or remove user roles")
async def roles(ctx, target: discord.Member, role: discord.Role):
	try:	
		if role not in target.roles:
			await target.add_roles(role)
			embed = Embed(description=f"Added **{role.mention}** to **{target.mention}**", color=embed_color)
			await ctx.send(embed=embed)

		else:
			await target.remove_roles(role)
			embed = Embed(description=f"Removed **{role.mention}** from **{target.mention}**",  color=embed_color)
			await ctx.send(embed=embed)
	
	except Forbidden:
		embed = Embed(description=f"You cannot edit roles for {target.mention}", color=embed_color)
		await ctx.send(embed=embed)


#SET NICK COMMAND [Slash]
@slash.slash(name="setnick", description="Change User Nicknames")
async def set_nick(ctx, target: discord.Member, nickname):
	try:
		await target.edit(nick=nickname)
		embed = Embed(description=f"Changed **{target.name}#{target.discriminator}**'s name to **{nickname}**", color=embed_color)
		await ctx.send(embed=embed)
	except Forbidden:
		await ctx.send(f"I cant change **{target.name}#{target.discriminator}**'s name")


#REMINDER COMMAND [Slash]
@slash.slash(name="remindme", description="Set a reminder")
async def remindme(ctx, time, *, message):
	try:
		sleep_time = convert(time)

		try:
			await ctx.author.send(f"I will remind you after **{time}** with the message **{message}**")
			await ctx.channel.send("Check your dms...")
		
		except:
			await ctx.channel.send(f"I will remind you after **{time}** with the message **{message}** \n <:uhh:847601058904932362> Also enable your dms bruh")
		
		await asyncio.sleep(sleep_time)

		embed = Embed(title="Reminder",
			description=f"{message}",
			color=embed_color)
		try:
			await ctx.author.send(embed=embed)
		
		except:
			await ctx.channel.send(f"||{ctx.author.mention}||",embed=embed)

	except:
		return await ctx.send("Please enter either `s`, `m`, `h` or `d` after the integer!")


#AV COMMAND [Slash]
@slash.slash(name="avatar",description="User avatar")
async def avatar(ctx, target: Optional[discord.Member]):
	target = target or ctx.author
	embed = Embed(title=f"{target.display_name}'s Avatar",url=f"{target.avatar_url}",color=embed_color)
	embed.set_image(url=f"{target.avatar_url}")
	await ctx.send(embed = embed)


#PING COMMAND [Slash]
@slash.slash(name="ping", description="Bot Latency")
async def ping(ctx):
	embed = Embed(description=f"Pong! Latency is **{round(bot.latency*1000)}** ms",color=embed_color)
	await ctx.send(embed=embed)


#TRANSLATE COMMAND [Slash]
@slash.slash(name="trasnalte", description = "Translate any sentence in any language")
async def translate(ctx, lang, *sentence):
    lang = lang.lower()
    if lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:
        await ctx.send("huh?")

    else:
	    text = ' '.join(sentence)
	    translator = Translator()
	    text_translated = translator.translate(text, dest= lang)
	    await ctx.send(text_translated.text)


#KICK COMMAND [Slash]
@slash.slash(name="kick", description="Kick Users")
async def kick(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.kick(reason = reason)
	embed = Embed(description=f"Successfully kicked **{target.name}#{target.discriminator}**", color=embed_color)
	await ctx.send(embed=embed)


#BAN COMMAND [Slash]
@slash.slash(name="ban", description="Ban Users")
async def ban(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.ban(reason = reason)
	embed = Embed(description=f"Successfully banned **{target.name}#{target.discriminator}**", color=embed_color)
	await ctx.send(embed=embed)


#NUKE COMAMND [Slash]
@slash.slash(name="nuke", description="Nukes a mentioned channel")
async def nuke(ctx, channel: discord.TextChannel = None):
	allowed = [914092837564481556]
	if ctx.author.id in allowed:	
		if channel == None:
			embed = Embed(description=f"**You did not mention a channel\n For example {ctx.channel.mention}**", color=0x000000)
			await ctx.send(embed=embed)
			return

		nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

		if nuke_channel is not None:
			new_channel = await nuke_channel.clone(reason="Has been Nuked!")
			await nuke_channel.delete()
			nuke_channel_embed = Embed(description="**This channel has been nuked**",color=0x000000)
			nuke_channel_embed.set_image(url="https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif")
			await new_channel.send(embed=nuke_channel_embed)
			embed=Embed(description=f"**`{new_channel.name}` has been nuked sucessfully**", color=0x000000)
			await ctx.send(embed=embed)

		else:
			emebd = Embed(description=f"**No channel named `{channel.name}` was found!**")
			await ctx.send(embed=embed)

	else:
		embed = Embed(description="**Insufficient permissions to perform that task!**")
		await ctx.send(embed=embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#MESSAGE EVENTS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON MESSAGE EVENT
@bot.event
async def on_message(message):	


	#Deleting messages in #gateway
	if message.channel.id == 929474964619419708:
		await message.delete(delay=60)


	#Sending bot updates
	if message.channel.id == 929734021586501632:
		updates_channel = bot.get_guild(879392778533077102).get_channel(955751049908609024)
		embed = Embed(title = "New Update", description = f"{message.content}", color = embed_color)
		await updates_channel.send(embed = embed)


	#Handling suggestions
	if message.channel.id == 955750968245497867:
		if not message.author.bot:
			if message.content != None:
				if len(message.content) > 5:
					
					log_channel = bot.get_guild(929473357311795310).get_channel(949933663653613579)
					
					embed = Embed(description = f"{message.content}",
						color = embed_color)
					embed.set_author(name = f"{message.author.display_name}'s Suggestion", icon_url=f"{message.author.avatar_url}")
					
					reaction_message = await message.channel.send(embed = embed)
					await log_channel.send(embed = embed)
					await message.delete()
					
					await reaction_message.add_reaction("👍")
					await reaction_message.add_reaction("👎")
					await reaction_message.add_reaction("😓")

				else:
					await message.channel.send("Your message needs to be longer than 5 characters!", delete_after = 60)
					await message.delete(delay = 60)


	#Handling bug reports
	if message.channel.id == 949933748055588904:
		if not message.author.bot:
			if message.content != None:
				if len(message.content) > 5:

					log_channel = bot.get_guild(929473357311795310).get_channel(949933748055588904)

					embed = Embed(description = f"{message.content}",
					color = embed_color)
					embed.set_author(name = f"{message.author.display_name}'s Bug Report", icon_url=f"{message.author.avatar_url}")
					
					reaction_message = await message.channel.send(embed = embed)
					await log_channel.send(embed = embed)
					await message.delete()
					
					await reaction_message.add_reaction("👍")
					await reaction_message.add_reaction("👎")
					await reaction_message.add_reaction("😓")

				else:
					await message.channel.send("Your message needs to be longer than 5 characters!", delete_after = 60)
					await message.delete(delay = 60)


	#BOT MENTION EVENT
	if bot.user.mentioned_in(message) and message.content.startswith("<") and message.content.endswith(">"):
		if not message.author.bot:
			choice_69 = ["Try using slash commands aka `/`", "Slash commands || aka  `/` || exist for a reason. Consider using them???", "My prefix is `!` but slash commands || aka `/` || are better, no cap",
			"`/help` for help", "Need help? Just use slash help command || aka `/help` ||", "`!help` for help"]
			await message.reply(f"{randchoice(choice_69)}")

	
	#BOT DMS EVENT
	if isinstance(message.channel, DMChannel):
		if not message.author.bot:
			logs_channel = bot.get_guild(929473357311795310).get_channel(929473357311795310)
			embed = Embed(title="DM Received",
				description=f"**Message By:** \n {message.author.mention}丨{message.author.name}#{message.author.discriminator} \n\n **Message:** \n {message.content}",
				color=embed_color,
				timestamp=datetime.utcnow())
			embed.set_thumbnail(url = f"{message.author.avatar_url}")
			await logs_channel.send(embed=embed)
			await message.add_reaction("✅")


	#KEYWORD EVENTS
	if not message.author.bot:
		await bot.process_commands(message)
 


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#GUILD JOIN EVENTS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON MEMBER JOIN EVENT
@bot.event
async def on_member_join(member):
	insert_guild_id_here = 929473357311795310
	if member.guild.id == insert_guild_id_here:
		await member.send(f"{member.mention} welcome to Empty Remastered. \nA request has been sent to get you verified, please bear with me until then 😩 \n**Note:** This bot's dms are monitored, you can leave a message anytime...")
		logs_channel = bot.get_guild(insert_guild_id_here).get_channel(929702945111568435)
		empty_role = bot.get_guild(insert_guild_id_here).get_role(929475219784081479)
		
		embed = Embed(title=f"{member.name} Just joined {member.guild.name}!", 
							color =embed_color, timestap=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
		fields = [("Name", f"**{member.mention}丨{member.name}#{member.discriminator}**", False),
					("ID", f"{member.id}", False),				
					("Joined on", member.joined_at.strftime("%d/%m/%Y"), True),
					("Create on", member.created_at.strftime("%d/%m/%Y"), True),
					("Role Status", f"Do you want me to hand out **<@&{empty_role.id}>** role to **{member.mention}**? \n Please react accordingly within `12 hours` \n **Status:** Pending...", False)]	
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		this = await logs_channel.send("<@&929732908149788743>",embed=embed)
		await this.add_reaction("✅")

		def check(reaction, user):
			return user != user.bot and str(reaction.emoji) == '✅'

		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=43200, check=check)
	    
		except asyncio.TimeoutError:
			await this.clear_reaction("✅")
			embed = Embed(title=f"{member.name} Just joined {member.guild.name}!", 
							color =embed_color, timestap=datetime.utcnow())
			embed.set_thumbnail(url=member.avatar_url)
			fields = [("Name", f"**{member.mention}丨{member.name}#{member.discriminator}**", False),
						("ID", f"{member.id}", False),				
						("Joined on", member.joined_at.strftime("%d/%m/%Y"), True),
						("Create on", member.created_at.strftime("%d/%m/%Y"), True),
						("Status", f"Session Expired!", False)]	
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await this.edit(embed=embed)

		else:
			await this.clear_reaction("✅")
			for role in member.roles:
				if empty_role not in member.roles:

					await member.add_roles(empty_role)
					embed = Embed(title=f"{member.name} Just joined {member.guild.name}!", 
									color =embed_color, timestap=datetime.utcnow())
					embed.set_thumbnail(url=member.avatar_url)
					fields = [("Name", f"**{member.mention}丨{member.name}#{member.discriminator}**", False),
								("ID", f"{member.id}", False),				
								("Joined on", member.joined_at.strftime("%d/%m/%Y"), True),
								("Create on", member.created_at.strftime("%d/%m/%Y"), True),
								("Status", f"Roles Added Successfully!", False)]	
					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					return await this.edit(embed=embed)
				
				else:
					embed = Embed(title=f"{member.name} Just joined {member.guild.name}!", 
									color =embed_color, timestap=datetime.utcnow())
					embed.set_thumbnail(url=member.avatar_url)
					fields = [("Name", f"**{member.mention}丨{member.name}#{member.discriminator}**", False),
								("ID", f"{member.id}", False),				
								("Joined on", member.joined_at.strftime("%d/%m/%Y"), True),
								("Create on", member.created_at.strftime("%d/%m/%Y"), True),
								("Status", f"{member.mention} already has <@&{empty_role.id}> role!", False)]	
					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					return await this.edit(embed=embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#REACTION EVENTS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON RAW REACTION ADD EVENT
@bot.event
async def on_raw_reaction_add(payload):
	if not payload.member.bot:
		starboard_channel = bot.get_guild(929473357311795310).get_channel(929702972835913778)
		if payload.emoji == ("📌") or payload.emoji.name == "📌":
			message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
			if len(message.content) < 1020:
				if not len(message.attachments):
					embed = Embed(title= f"Pinned By {payload.member.name}",
						color= embed_color,
						timestamp = datetime.utcnow())
					embed.add_field(name = f"Message By", value = f"{message.author.name}#{message.author.discriminator}丨{message.author.id}", inline = False)					
					embed.add_field(name = f"Message", value = f"{message.content}", inline = False)
					embed.add_field(name = f"Link", value = f"[Jump to the original message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", inline = False)
					
					await starboard_channel.send(embed=embed)
					await message.reply(f"This message has been posted in <#{starboard_channel.id}>")

				else:
					embed = Embed(title= f"Pinned By {payload.member.name}",
						color= embed_color,
						timestamp = datetime.utcnow())
					embed.add_field(name = f"Message By", value = f"{message.author.name}#{message.author.discriminator}丨{message.author.id}", inline = False)					
					embed.add_field(name = f"Link", value = f"[Jump to the original message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", inline = False)
					embed.set_image(url=message.attachments[0].url)
				
					await starboard_channel.send(embed=embed)
					await message.reply(f"This message has been posted in <#{starboard_channel.id}>")

			else:
				await message.reply("This message is too long for me to actually pin...")



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#ERROR HANDLERS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ERROR HANDLING EVENT
@bot.event
async def on_command_error(ctx, exc):
	IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
	if isinstance(exc, NotOwner):
		await ctx.reply(":x: Insufficient permissions to perform that task", delete_after=60)
		await ctx.message.delete(delay=60)
	
	elif isinstance(exc, MissingAnyRole):			
		await ctx.reply(":x: Insufficient permissions to perform that task", delete_after=60)
		await ctx.message.delete(delay=60)

	elif isinstance(exc, DisabledCommand):
		await ctx.reply("That command is disabled for now, try again later", delete_after=60)
		await ctx.message.delete(delay=60)
	
	elif isinstance(exc, RoleNotFound):
		await ctx.reply("That role does not exist", delete_after=60)
		await ctx.message.delete(delay=60)
	
	elif any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
		pass
	
	elif isinstance(exc, MissingRequiredArgument):
		await ctx.reply("One or more required arguments are missing!", delete_after=60)
		await ctx.message.delete(delay=60)
	
	elif isinstance(exc, CommandOnCooldown):
		cd = round(exc.retry_after)
		minutes = str(cd // 60)
		seconds = str(cd % 60)
		await ctx.reply(f"That command is on cooldown!... \nTry again in **{minutes}** minutes and **{seconds}** seconds.", delete_after=60)
		await ctx.message.delete(delay=60)
	
	elif hasattr(exc, "original"):
		raise exc.original

	else:
		raise exc



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#GHOST PING DETECTOR
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON MESSAGE DELETE EVENT
@bot.event
async def on_message_delete(message):
	guild = bot.get_guild(929473357311795310)
	logs_channel = bot.get_guild(929473357311795310).get_channel(929703044919230494)
	
	if message.mentions:
		if not message.author == guild.me:
			for s in message.mentions:
				channel_embed=Embed(title="Ghost Ping",
					description=f"**{s.mention} was ghost pinged by {message.author.mention}**",
					color=embed_color, 
					timestamp=datetime.utcnow())
				fields = [("Message", f"{message.content}", False)]
				for name, value, inline in fields:
					channel_embed.add_field(name=name, value=value, inline=inline)
				await message.channel.send(embed=channel_embed)
				
				log_embed=Embed(title="Ghost Ping",color=embed_color, timestamp=datetime.utcnow())
				log_embed.set_thumbnail(url=f"{message.author.avatar_url}")
				fields = [("Ping By", f"{message.author.name}#{message.author.discriminator}", True),
						("Ping To", f"{s.name}#{s.discriminator}", False),
						("Channel", message.channel.mention , True),
						("Message", message.content , False)]
				for name, value, inline in fields:
					log_embed.add_field(name=name, value=value, inline=inline)
				return await logs_channel.send(embed=log_embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#ECONOMY SYSTEM
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ECONOMY HELP COMMAND
@bot.command(name = "economy", help = "Get a list of all available economy commands.")
async def economy_help(ctx):
	embed = Embed(title = "Economy Help", color = embed_color)
	embed.add_field(name = "Database Commands", value = "`profile`, `lb`, `withdraw`, `deposit`", inline = False)
	embed.add_field(name = "Gambling Commands", value = "`beg`, `rob`, `slots`", inline = False)
	embed.add_field(name = "Inventory Commands", value = "`shop`, `buy`, `sell`, `send`", inline = False)
	embed.add_field(name = "Individual Commands Help", value =  f"To view help for individual commands, use the following syntax \n```{ctx.prefix}help <command>```", inline =  False)
	await ctx.send(embed = embed)


#PROFILE COMMAND
@bot.command(name = "profile", help = "Displays user profile with info such as your bank balance and wallet balance etc.")
async def balance(ctx, user: Optional[discord.Member]):
	user = user or ctx.author
	
	await open_account(user)

	users = await get_bank_data()
	wallet_amount = users[str(user.id)]["wallet"]
	bank_amount = users[str(user.id)]["bank"]

	final_wallet_amount = round(wallet_amount)
	final_bank_amount = round(bank_amount)
	
	if wallet_amount == 0:
		final_wallet_amount = "Your wallet is empty!"
	if bank_amount == 0:
		final_bank_amount = "Your bank account is empty!"

	try:
		bag = users[str(user.id)]["bag"]
	
	except:
		bag = []

	members = await get_bank_data()
	leader_board = {}
	total = []
	for member in members:
		name = int(member)
		total_amount = members[member]["wallet"] + members[member]["bank"]
		leader_board[total_amount] = name
		total.append(total_amount)

	total = sorted(total,reverse=True)

	index = 1
	for amt in total:
		id_ = leader_board[amt]
		if id_ == user.id:
			member = bot.get_user(id_)
			if member.name == user.name:
				break
		else:
			index += 1

	final_index = index 
	if bank_amount == 0 and wallet_amount == 0:
		final_index = "None"
	
	embed = Embed(title = f"{user.name}'s Profile", description = f"Rank = {final_index}",
	color = embed_color)
	embed.set_thumbnail(url = user.avatar_url)
	embed.add_field(name = "Wallet balance", value = final_wallet_amount, inline = False)
	embed.add_field(name = "Bank balance", value = final_bank_amount, inline = False)

	users = await get_bank_data()

	try:
		bag = users[str(user.id)]["bag"]

		net = []
		for item in bag:
			name = item["item"]
			amount = item["amount"]

			net.append(f"{name.capitalize()} - `{amount}` \n")
		embed.add_field(name = "Inventory", value = "".join(net), inline = False)
		await ctx.reply(embed = embed)

	except:
		embed.add_field(name = "Inventory", value = "Your inventory is empty!", inline = False)
		await ctx.reply(embed = embed)
	

#BEG COMMAND
@bot.command(name = "beg", help = "An easy way to earn coins every 30 minutes.")
@commands.cooldown(1, 1800 , type = commands.BucketType.user)
async def beg(ctx):
	await open_account(ctx.author)

	money = [0,random.randint(10,2000),random.randint(30,500),random.randint(100,200),random.randint(1,2500),random.randint(2,300)]
	amount = random.choice(money)
	person = random.choice(names)
	
	await update_bank(ctx.author, amount)
	
	if amount == 0:
	    await ctx.send("Ahh, you got nothing! :(")
	
	elif amount>1000:
	    await ctx.send(embed = Embed(title = "Woow!!",
	    description = f"Seems like {person.title()} donated you **{amount}** coins :star_struck:",
	    color = embed_color))
	
	elif amount <500 and amount >100:
	    await ctx.send(embed = Embed(title = "Nice!!",
	    description = f"You got a mediocre amount of **{amount}** coins from {person.title()} :)",
	    color = embed_color))
	
	elif amount <100:
	    await ctx.send(embed = Embed(title = "Ahhh!",
	    description = f"{person.title()} donated you a small portion of **{amount}** coins :expressionless:",
	    color = embed_color))


#WITHDRAW COMMAND
@bot.command(name = "withdraw", help = "Withdraw money from your bank balance.")
@commands.cooldown(1, 1800 , type = commands.BucketType.user)
async def withdraw(ctx, amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("Please enter the amount...")
		return

	bal = await update_bank(ctx.author)

	amount = round(int(amount))
	if amount>bal[1]:
		await ctx.send("You do not have that much money!")
		return

	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author, amount)
	await update_bank(ctx.author, -1*amount, "bank")

	await ctx.send(f"You withdrew **{amount}** coins!")


#WORK COMMAND
@bot.command(name = "work", help = "Work and earn money every 12 hours.")
@commands.cooldown(1, 3600 , type = commands.BucketType.user)
async def work(ctx):
	await open_account(ctx.author)
	user = ctx.author
	member= ctx.author
	
	homie = get(ctx.author.guild.roles, id=949287989559840768)
	guest = get(ctx.author.guild.roles, id=929732766516518973)
	roles = [homie, guest]
	
	no_ = 1
	for i in roles:
		if i in ctx.author.roles:
			no_+=1
			
	coins = random.randint(500,600*no_)
	await update_bank(ctx.author, int(coins))
	
	users = await get_bank_data()
	wallet_amount = users[str(user.id)]["wallet"]
	
	embed = discord.Embed(description = f"You earned **{coins}** coins through working! \nWallet balance: **{round(wallet_amount)}**",
	color = embed_color)
	await ctx.send(embed = embed)


#REWARD COMMAND
@bot.command(name = "reward", help = "Add coins to a specific user.")
@commands.is_owner()
async def reward(ctx, member:discord.Member, amount: int = 1000):
	await open_account(ctx.author)
	await update_bank(member, amount)
	await ctx.send(f"{member.name} has been rewarded **{amount}** coins!")


#DEPOSIT COMMAND
@bot.command(name = "deposit", help = "Deposit money into your bank balance.")
@commands.cooldown(1, 1800 , type = commands.BucketType.user)
async def deposit(ctx, amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("Please enter the amount...")
		return

	bal = await update_bank(ctx.author)

	amount = round(int(amount))
	if amount>bal[0]:
		await ctx.send("You do not have that much money!")
		return

	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author, -1*amount)
	await update_bank(ctx.author, amount, "bank")

	await ctx.send(f"You deposited **{amount}** coins!")


#SENDING MONEY COMMAND
@bot.command(name = "send", help = "Help someone out by sending them coins.")
@commands.cooldown(1, 43200 , type = commands.BucketType.user)
async def send(ctx, member:discord.Member,  amount = None):
	await open_account(ctx.author)
	await open_account(member)

	if amount == None:
		await ctx.send("Please enter the amount...")
		return

	if amount == "all":
		amount = round(bal[0])

	bal = await update_bank(ctx.author)
	amount = round(int(amount))
	
	if amount>bal[0]:
		await ctx.send("You do not have that much money!")
		return

	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author, -1*amount, "bank")
	await update_bank(member, amount, "bank")

	await ctx.send(f"You sent **{amount}** coins to **{member.name}**!")


#SLOTS COMMAND    
@bot.command(name = "slots", help = "Play a game of slots to earn coins.")
async def slots(ctx,amount = None):
	await open_account(ctx.author)
	user = ctx.author

	users = await get_bank_data()
	wallet_amount = users[str(user.id)]["wallet"]
	bank_amount = users[str(user.id)]["bank"]

	if amount == None or amount == 0:
		await ctx.send("Please enter an amount!")
		return
    
	try:
		amount = round(int(amount))
		amount = round(abs(amount))
	except:
		await ctx.send("Please enter a correct amount!")

	final = []
	bal = await update_bank(ctx.author)

	if round(bal[0]) >= amount:
		for i in range(3):
			a = random.choice([":coin:",":money_mouth:",":money_with_wings:"])

			final.append(a)


		if final[0]==final[1]==final[2]:
			await update_bank(ctx.author, amount*4)
			users = await get_bank_data()
			wallet_amount = users[str(user.id)]["wallet"]
			em = discord.Embed(title = f"{'  '.join(final)}" , description = f"{ctx.author.mention} you won **{amount*4}** coins!\nTotal coins: **{round(wallet_amount)}**",
			color = embed_color)
			await ctx.send(embed = em)
		
		else:
			await update_bank(ctx.author, -1*amount) 
			users = await get_bank_data()
			wallet_amount = users[str(user.id)]["wallet"]
			em = discord.Embed(title = f"{'  '.join(final)}" , description = f"{ctx.author.mention} you lost **{amount}** coins! \nTotal coins: **{round(wallet_amount)}**",
			color = embed_color)
			await ctx.send(embed = em)
    
	else:
		await ctx.send("You don't have enough coins!")


#BET COMMAND
@bot.command(name = "bet", help = "Gamble and earn coins.")
async def bet(ctx, amount = None):
	await open_account(ctx.author)
	user = ctx.author
	
	try:
		amount = round(int(amount))
		amount = round(abs(amount))
	
	except:
		await ctx.send("Please enter a correct amount")
		return
	
	bal = await update_bank(ctx.author)
	
	if amount>bal[0]:
		await ctx.send("You do not have that much money!")
		return
		return
    
	if amount == None or amount == 0:
		await ctx.send(embed = discord.Embed(title = "Huh",description = "Amount can't be Zero :D ",color = discord.Colour.red(),delete_after = 10))
		return

	mystrike = random.randint(1,12)
	botstrike = random.randint(2,12)
	if mystrike>botstrike:
		percent = random.randint(50,100)
		amount_add = int(amount*(percent/100))
		await update_bank(ctx.author, amount_add, "wallet")
	
		users = await get_bank_data()
		wallet_amount = users[str(user.id)]["wallet"]

		embed = Embed(description = f"You Won **{amount_add} coins** \nPercent Won: **{percent}%** \nNew Balance: **{round(wallet_amount)}**",
			color = embed_color,
			timestamp=datetime.utcnow())
		embed.set_author(name =f"Woow Seems like {ctx.author.name} plays well",icon_url=ctx.author.avatar_url)
		embed.add_field(name = f"**{ctx.author.name.title()}** ",value=f"Strikes `{mystrike}`")
		embed.add_field(name = f"**{bot.user.name.title()}** ",value=f"Strikes `{botstrike}`")
		await ctx.send(embed = embed)
	
	elif mystrike<botstrike:
		percent = random.randint(0,80)
		lost = int(amount*(percent/100))
		await update_bank(ctx.author, -1*lost)
		users = await get_bank_data()
		wallet_amount = users[str(user.id)]["wallet"]
		
		embed = discord.Embed(description = f"You Lost **{lost} coins** \nPercent Lost: **{percent}%** \nNew Balance: **{round(wallet_amount)}**",
		color = embed_color,
		timestamp=datetime.utcnow())
		embed.set_author(name = f"Crap Play {ctx.author.name} !",icon_url=ctx.author.avatar_url)
		embed.add_field(name = f"**{ctx.author.name.title()}** ",value=f"Strikes `{mystrike}`")
		embed.add_field(name = f"**{bot.user.name.title()}** ",value=f"Strikes `{botstrike}`")
		await ctx.send(embed = embed)

	else:
		embed = discord.Embed(description = f"**It was a tie!**",
			color = embed_color,
			timestamp=datetime.utcnow())
		embed.set_author(name = f"Tie",icon_url=ctx.author.avatar_url)
		embed.add_field(name = f"**{ctx.author.name.title()}** ",value=f"Strikes `{mystrike}`")
		embed.add_field(name = f"**{bot.user.name.title()}** ",value=f"Strikes `{botstrike}`")
		await ctx.send(embed = embed)


#ROB COMMAND
@bot.command(name = "rob", help = "Rob someone's bank balance.")
@commands.cooldown(1, 86400 , type = commands.BucketType.user)
async def rob(ctx, member:discord.Member):
	await open_account(ctx.author)
	await open_account(member)

	bal = await update_bank(member)

	if bal[0]<100:
		await ctx.send(f"**{member.name}** does not have more than 100 coins, it's not worth robbing him!")
		return

	earnings = random.randrange(1, bal[0])

	await update_bank(ctx.author, round(earnings))
	await update_bank(member, round(-1*earnings))

	await ctx.send(f"You robbed and got **{earnings}** coins!")


#SHOP COMMAND
@bot.command(nmae = "shop", help = "Displays all items which you can buy.")
async def shop(ctx):
	embed = Embed(title = "Shop",description = "Shop related commands are listed below \n`!buy <item> <amount>` \n`!sell <item> <amount>`", color = embed_color)

	for item in mainshop:
		name = item["name"]
		price = item["price"]
		description = item["description"]

		embed.add_field(name = name, value = f"${price} | {description}", inline = False)

	await ctx.send(embed = embed)


#BUY COMMAND
@bot.command(name = "buy", help = "Buy something from the shop.")
async def buy(ctx,item,amount = 1):
	await open_account(ctx.author)

	res = await buy_this(ctx.author,item,amount)

	if not res[0]:
		if res[1]==1:
			await ctx.send("That Object isn't there!")
			return
		if res[1]==2:
			await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
			return

	await ctx.send(f"You just bought {amount} {item}")


#SELL COMMAND
@bot.command(name = "sell", help = "Sell something from your inventory.")
async def sell(ctx,item,amount = 1):
	await open_account(ctx.author)

	res = await sell_this(ctx.author,item,amount)

	if not res[0]:
		if res[1]==1:
			await ctx.send("That item isn't there!")
			return
		if res[1]==2:
			await ctx.send(f"You don't have {amount} {item} in your bag.")
			return
		if res[1]==3:
			await ctx.send(f"You don't have {item} in your bag.")
			return

	await ctx.send(f"You just sold `{amount}` {item}")


#LEADERBOARD COMMAND
@bot.command(name = "leaderboard", aliases = ["lb"], help = "Check the current server leaderboard.")
async def leaderboard(ctx, number = 5):
	users = await get_bank_data()
	leader_board = {}
	total = []
	for user in users:
		name = int(user)
		total_amount = users[user]["wallet"] + users[user]["bank"]
		leader_board[total_amount] = name
		total.append(total_amount)

	total = sorted(total,reverse=True)    

	em = discord.Embed(title = f"Top {number} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = embed_color)
	index = 1
	for amt in total:
		id_ = leader_board[amt]
		member = bot.get_user(id_)
		name = member.name
		em.add_field(name = f"{index}. {name}" , value = f"{round(amt)}",  inline = False)
		if index == number:
			break
		else:
			index += 1

	await ctx.send(embed = em)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
#RUNNING THE BOT
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON READY EVENT
@bot.event
async def on_ready():
	config_channel = bot.get_guild(929473357311795310).get_channel(929702945111568435)
	gateway_channel = bot.get_guild(929473357311795310).get_channel(929474964619419708)
	
	await bot.change_presence(status = discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name="Emptiness"))
	choice = []
	
	await config_channel.send("https://media.discordapp.net/attachments/879392779036413957/929689504061739018/847601058904932362.png")
	print("Bot is Ready")

with open("./token.json") as f:
	config = json.load(f)

token = config.get("token")
bot.run(token)

