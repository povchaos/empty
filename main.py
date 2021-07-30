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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command("help")
embed_color = 0x588642

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

#HELP COMMAND
@bot.command(name="help",description="Stop it, Get some help")
async def show_help(ctx):
	guild = ctx.guild
	embed = Embed(title="Help",
		description=f"I have a total of **{len(bot.commands)}** commands \n My current prefix is **{ctx.prefix}**",
		color=embed_color)
	embed.add_field(name = "Miscellaneous Commands", value = " `ping`, `setnick`, `avatar`, `role`, `remindme`", inline = False)
	embed.add_field(name = "Moderation Commands", value = "`kick`, `ban`", inline = False)
	embed.add_field(name = "Functions", value = "**・**Replys to `imy`, `ily`, `ihy`, `gay` and `ban` \n **・** Ai-chat aka <#869011766066163742> \n **・** Ghost ping detector \n **・** Modmail system \n **・** Keyword reactions", inline = False)
	embed.add_field(name = "Chad Developer", value = "<@726480855689724105>丨Lord Chaos#3393", inline = False)
	embed.set_thumbnail(url = guild.me.avatar_url)
	await ctx.channel.send(embed=embed)

#ROLE COMMAND
@bot.command(name="role", description="Add or remove user roles")
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

#SAY COMMAND
@bot.command(name="say")
async def say(ctx, message):
	await ctx.channel.send(f"{message}")

#EMBED COMMAND
@bot.command(name="embed")
async def embed(ctx, message):
	embed = Embed(description = f"{message}", color = embed_color)
	await ctx.channel.send(embed=embed)

#SETNICK COMMAND
@bot.command(name="setnick", description="Change User Nicknames")
async def set_nick(ctx, target: discord.Member, nickname):
	try:
		await target.edit(nick=nickname)
		embed = Embed(description=f"Changed **{target.name}#{target.discriminator}**'s name to **{nickname}**", color=embed_color)
		await ctx.channel.send(embed=embed)
	except Forbidden:
		await ctx.channel.send(f"I cant change **{target.name}#{target.discriminator}**'s name")

#REMINDME COMMAND
@bot.command(name="remindme", description="Set a reminder")
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
		return await ctx.channel.send("Please enter either `s`, `m`, `h` or `d` after the integer in reminder time!")

#AVATAR COMMAND
@bot.command(name="avatar",description="User avatar")
async def avatar(ctx, target: Optional[discord.Member]):
	target = target or ctx.author
	embed = Embed(title=f"{target.display_name}'s Avatar",url=f"{target.avatar_url}",color=embed_color)
	embed.set_image(url=f"{target.avatar_url}")
	await ctx.channel.send(embed = embed)

#PING COMMAND
@bot.command(name="ping", description="Bot Latency")
async def ping(ctx):
	embed = Embed(description=f"Pong! Latency is **{round(bot.latency*1000)}** ms",color=embed_color)
	await ctx.channel.send(embed=embed)

#KICK COMMAND
@bot.command(name="kick", description="Kick Users")
async def kick(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.kick(reason = reason)
	embed = Embed(description=f"Successfully kicked **{target.name}#{target.discriminator}**", color=embed_color)
	await ctx.channel.send(embed=embed)

#BAN COMMAND
@bot.command(name="ban", description="Ban Users")
async def ban(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.ban(reason = reason)
	embed = Embed(description=f"Successfully banned **{target.name}#{target.discriminator}**", color=embed_color)
	await ctx.channel.send(embed=embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#HELP COMMAND [Slash]
@slash.slash(name="help",description="Stop it, Get some help")
async def show_help(ctx):
	guild = ctx.guild
	embed = Embed(title="Help",
		description=f"I have a total of **{len(bot.commands)}** commands \n My current prefix is **{ctx.prefix}**",
		color=embed_color)
	embed.add_field(name = "Miscellaneous Commands", value = " `ping`, `setnick`, `avatar`, `role`, `remindme`", inline = False)
	embed.add_field(name = "Moderation Commands", value = "`kick`, `ban`", inline = False)
	embed.add_field(name = "Functions", value = "**・**Replys differently to `imy`, `ily`, `ihy`, `gay` and `ban` depending on the situation` \n **・** Ai-chat aka <#869011766066163742> \n **・** Ghost ping detector \n **・** Modmail System \n **・** Keyword reactions", inline = False)
	embed.add_field(name = "Chad Developer", value = "<@726480855689724105>丨Lord Chaos#3393", inline = False)
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
		return await ctx.send("Please enter either `s`, `m`, `h` or `d` after the integer in reminder time!")

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



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON MESSAGE EVENT
@bot.event
async def on_message(message):	
	options = ["<:yay:867816037079318568>", "<:whenlifegetsyou:862326647976624188>", "<:weird:820756635609464832>", "<:uwu:864433286993149962>", "<:umm:842192405754806342>",
	"<:uhh:847601058904932362>", "<:think:847799821096189953>", "<:tears:846841174010363966>", "<:sneer:820757567960776715>", "<:shutupgay:820756688424140851>",
	"<:shut:820756805809340457>", "<:shreklook:867815784997716039>", "<:sheesh:842440600774246430>", "<:salute:846442131400556564>", "<:sad:847799874698084362>",
	"<:pleading:848260381436936212>", "<:ping:823857027314483201>", "<:paink:847800523519164457>", "<:oknooneasked:847800595188416522>", "<:notstonks:820756458928209940>",
	"<:nigga:855224644201087016>", "<:lmao:847799547475263490>", "<:lmao_2:847799640967217152>", "<:sweat_1:820756196876615710>", "<:lipbite:842440703598395464>", "<:laugh:847778083888955393>",
	"<:king:820757205703589938>", "<:hug:846912225431126076>", "<:hmm:867836166044778496>", "<:hehe:842192741986467841>", "<:grr:846443331738796105>", "<:faku:847526893842464798>",
	"<:dorime:847800082589286410>", "<:cry_1:820756773585551410>", "<:cringe:842192069678334014>", "<:cringe_1:854735604972912640>", "<:cool_1:820757300720828536>",
	"<:chuko:867684163674046484>", "<:chapal:847799929909149696>", "<:chad:847799756495388702>", "<:cap:847562740339310663>", "<:bruh:854678522412924928>", "<:Boznis:851800792926257152>",
	"<:blush_1:820757757187588137>", "<:suit_blush:846912330465017886>", "<:binladen:842192274721210408>", "<:alright:820757595173552128>", "<:aamna:862291911611777054>"]
	e = (f"{randchoice(options)}")

	if message.channel.id == 826460762695270432:
		await message.delete(delay=60)

	#BOT MENTION EVENT
	if bot.user.mentioned_in(message) and message.content.startswith("<") and message.content.endswith(">"):
		if not message.author.bot:
			choice_69 = ["Try using slash commands aka `/`", "Slash commands || aka  `/` || exist for a reason. Consider using them???", "My prefix is `!` but slash commands || aka `/` || are better, no cap",
			"`/help` for help", "Need help? Just use slash help command || aka `/help` ||"]
			await message.reply(f"{randchoice(choice_69)}")
		
		
	#BOT DMS EVENT
	if isinstance(message.channel, DMChannel):
		if not message.author.bot:
			logs_channel = bot.get_guild(795726142161944637).get_channel(868251065546584124)
			embed = Embed(title="DM Received",
				description=f"**Message By:** \n {message.author.mention}丨{message.author.name}#{message.author.discriminator} \n\n **Message:** \n {message.content}",
				color=embed_color,
				timestamp=datetime.utcnow())
			embed.set_thumbnail(url = f"{message.author.avatar_url}")
			await logs_channel.send(embed=embed)
			await message.add_reaction("✅")

		
	#KEYWORD EVENTS
	if not message.author.bot:
		
		#REACTION EVENTS
		if "chaos" in message.content or "Chaos" in  message.content or "ahmed" in  message.content or "Ahmed" in message.content:
			await message.add_reaction(f"{e}")
		
		if "aamna" in message.content or "Aamna" in  message.content:
			await message.add_reaction(f"{e}")

		if "hades" in message.content or "Hades" in message.content or "Taha" in message.content or "taha" in message.content:
			await message.add_reaction(f"{e}")

		if "dirtygamer" in message.content or "Dirtygamer" in message.content or "Hashir" in message.content or "hashir" in message.content:
			await message.add_reaction(f"{e}")
		
		if "Vusion" in message.content or "vusion" in message.content:
			await message.add_reaction(f"{e}")

			
		#MY PING EVENT	
		if "726480855689724105" in message.content or "862428136166916096" in message.content:
			options = ["Yeah hes dead...", "Hes more dead than alive...", "He's gone to get milk...", "He'll be back soon... I hope so", "That user is MIA...",
			"He's dead bhai...", "Hes dead, find peace dude...", "That user is afk... Since 69 years", "Last online 10 years ago...", "Last online 69 years ago...", "Last online 420 years ago...",
			"Stop it he's already dead...", "He went to get milk...", "That user is KIA..."]
			options_2 = ["<:yay:867816037079318568>", "<:whenlifegetsyou:862326647976624188>", "<:weird:820756635609464832>", "<:umm:842192405754806342>",
			"<:uhh:847601058904932362>", "<:think:847799821096189953>", "<:tears:846841174010363966>", "<:sneer:820757567960776715>", "<:sheesh:842440600774246430>",
			"<:salute:846442131400556564>", "<:sad:847799874698084362>", "<:ping:823857027314483201>", "<:paink:847800523519164457>", "<:notstonks:820756458928209940>", "<:sweat_1:820756196876615710>", "<:king:820757205703589938>","<:hmm:867836166044778496>", "<:cry_1:820756773585551410>", "<:chad:847799756495388702>", "<:bruh:854678522412924928>", "<:aamna:862291911611777054>"]
			return await message.reply(f"{randchoice(options_2)} {randchoice(options)}")
		

		#ILY EVENT [Specific]
		if "Ily" in message.content or "ily" in message.content or "I love you" in message.content or "i love you" in message.content:
			if message.reference is not None:
				if message.reference.cached_message is None:
					channel = bot.get_channel(message.reference.channel_id)
					msg = await channel.fetch_message(message.reference.message_id)
					if msg.author != bot.user:
						return await message.reply(f"Where is my ily???")					
				
				else:
					if message.reference.cached_message.author != bot.user:
						return await message.reply(f"Where is my ily???")
			
			if message.author.id == 723242226855182468:
				choice = [f"Ily 2 nibbe {e}", f"Ily 2 nibbe {e}", f"Ily 2 nibbe  {e}", f"Ily 2 nibbe  {e}", f"Ily 2 nibbe  {e}", f"Ily 2 nibbe  {e}", "ew <:cringe:842192069678334014>", "ew <:cringe:854735604972912640>", "k, no one asked <:faku:847526893842464798>",
				"but who asked? <:faku:847526893842464798>", "Stap it. Get some help <:cringe:854735604972912640>", "Stap it. Get some help <:cringe:842192069678334014>", "k?"]
				return await message.reply(f" {randchoice(choice)}")
			
			else:
				return await message.reply(f"Ily 2 king {e}")


		#IHY EVENT [Specific]
		if "Ihy" in message.content or "ihy" in message.content or "I hate you" in message.content or "i hate you" in message.content:
			if message.reference is not None:
				if message.reference.cached_message is None:
					channel = bot.get_channel(message.reference.channel_id)
					msg = await channel.fetch_message(message.reference.message_id)
					if msg.author != bot.user:
						return await message.reply(f"Spread legs not hate...")					
				
				else:
					if message.reference.cached_message.author != bot.user:
						return await message.reply(f"Spread legs not hate...")
			
			if message.author.id == 723242226855182468:
				choice = ["k", "k?", "Rude", "Mean tou na ho", "Kitne mean ho", "Ajeeb", "Meanie", "Ihy 2", "Sigh", "Stupid ass", "Ok shorty", "Ok fatty"]
				return await message.reply(f" {randchoice(choice)}")
			
			else:
				choice = ["k", "k?", "Rude", "Mean tou na ho", "Kitnay mean ho", "Ajeeb", "Meanie", "Ihy 2", "Sigh"]
				return await message.reply(f" {randchoice(choice)}")

		
		#IMY EVENT [Specific]
		if message.content == "I miss you" or message.content == "i miss you" or message.content == "Imy" or message.content == "imy":
			if message.reference is not None:
				if message.reference.cached_message is None:
					channel = bot.get_channel(message.reference.channel_id)
					msg = await channel.fetch_message(message.reference.message_id)
					if msg.author != bot.user:
						return await message.reply(f"And you dont miss me???")					
				
				else:
					if message.reference.cached_message.author != bot.user:
						return await message.reply(f"And you dont miss me???")
			
			if message.author.id == 723242226855182468:
				choice = [f"Ily 2 nibbe {e}", f"Imy 2 nibbe {e}", f"Imy 2 nibbe {e}", f"Imy 2 nibbe {e}", f"Imy 2 nibbe {e}", f"Imy 2 nibbe {e}", "ew <:cringe:842192069678334014>", "ew <:cringe:854735604972912640>", "k, no one asked <:faku:847526893842464798>",
				"but who asked? <:faku:847526893842464798>", "Stap it. Get some help <:cringe:854735604972912640>", "Stap it. Get some help <:cringe:842192069678334014>", "k?"]
				return await message.reply(f" {randchoice(choice)}")
			
			else:
				return await message.reply(f"Imy 2 king {e}")

		
		#BAN EVENT [Specific]
		if message.content == "Ban" or message.content == "ban":
			if message.reference is not None:
				if message.reference.cached_message is None:
					channel = bot.get_channel(message.reference.channel_id)
					msg = await channel.fetch_message(message.reference.message_id)
					if msg.author != bot.user:
						return await msg.reply(f"Ayo dont make me ban you")
					
					else:
						return await message.reply("Ban myself? Aight")

				else:
					msg = message.reference.cached_message
					if msg.author != bot.user:
						return await msg.reply(f"Ayo dont make me ban you")

					else:
						return await message.reply("Ban myself? Aight")
			else:
				if message.author.id == 723242226855182468:
					return await message.reply("Ban who nibbe?")
				
				else:
					return await message.reply("Ban who nibba?")
		
		
		#GAY EVENT [Specific]
		if message.content == "gay" or message.content == "Gay" or message.content == "Gae" or message.content == "gae":
			if message.reference is not None:
				if message.reference.cached_message is None:
					channel = bot.get_channel(message.reference.channel_id)
					msg = await channel.fetch_message(message.reference.message_id)
					if msg.author != bot.user:
						if msg.author.id == 726480855689724105 or msg.author.id == 862428136166916096:
							return await message.reply("Chaos is chad stfu")
						
						else:
							return await msg.reply("https://tenor.com/view/why-uganda-are-you-gay-you-gif-12775398")
							
					else:
						return await message.reply("https://tenor.com/view/obama-what-seriously-wtf-gif-12341428")

				else:
					msg = message.reference.cached_message
					if msg.author != bot.user:
						if msg.author.id == 726480855689724105 or msg.author.id == 862428136166916096:
							return await message.reply("Chaos is chad stfu")

						else:
							return await msg.reply("https://tenor.com/view/why-uganda-are-you-gay-you-gif-12775398")
							
					else:
						return await message.reply("https://tenor.com/view/obama-what-seriously-wtf-gif-12341428")

			else:
				if message.author.id == 723242226855182468:
					return await message.reply("<@478815409177362432> <@569163565160857620> U 2")
				
				else:
					return await message.reply("<@723242226855182468> U")

		
	#AI CHAT FUNCTION
	if message.channel.id == 870630067187879997:
		if "@everyone" not in message.content and "@here" not in message.content:
			
			async with randomstuff.AsyncClient(api_key="tQeJ9s1ZRUQt") as client:
				response = await client.get_ai_response(message.content)
				await message.reply(response.message)	
					
		else:
			await message.reply("You really thought that would work? <:yay:867816037079318568>")

	
	else:
		await bot.process_commands(message)
 

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON MEMBER JOIN EVENT
@bot.event
async def on_member_join(member):
	logs_channel = bot.get_guild(795726142161944637).get_channel(868251065546584124)
	empty_role = bot.get_guild(795726142161944637).get_role(818950383216623696)
	
	embed = Embed(title=f"{member.name} Just joined {member.guild.name}!", 
						color =embed_color, timestap=datetime.utcnow())
	embed.set_thumbnail(url=member.avatar_url)
	fields = [("Name", f"**{member.mention}丨{member.name}#{member.discriminator}**", False),
				("ID", f"{member.id}", False),				
				("Joined on", member.joined_at.strftime("%d/%m/%Y"), True),
				("Create on", member.created_at.strftime("%d/%m/%Y"), True),
				("Status", str(member.status).title(), True),
				("Roles Status", f"Do you want me to hand out <@&818950383216623696> role to {member.mention}?** \n **Please react accordingly within `12 hours`** \n __**Roles Status:**__ Pending")]	
	for name, value, inline in fields:
		embed.add_field(name=name, value=value, inline=inline)

	this = await logs_channel.send("@everyone",embed=embed)
	await this.add_reaction("✅")

	def check(reaction, user):
		return user.id == 726480855689724105 or user.id == 723242226855182468 and str(reaction.emoji) == '✅'

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
					("Status", str(member.status).title(), True),
					("Roles Status", f"Session Expired!")]	
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await this.edit(embed=embed)

	else:
		await this.clear_reaction("✅")
		await member.add_roles(empty_role)
		embed = Embed(title=f"{member.name} Just joined {member.guild.name}!", 
						color =embed_color, timestap=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
		fields = [("Name", f"**{member.mention}丨{member.name}#{member.discriminator}**", False),
					("ID", f"{member.id}", False),				
					("Joined on", member.joined_at.strftime("%d/%m/%Y"), True),
					("Create on", member.created_at.strftime("%d/%m/%Y"), True),
					("Status", str(member.status).title(), True),
					("Roles Status", f"Roles Added Successfully!")]	
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await this.edit(embed=embed)



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON MESSAGE DELETE EVENT
@bot.event
async def on_message_delete(message):
	logs_channel = bot.get_guild(795726142161944637).get_channel(868251065546584124)
	guild = bot.get_guild(795726142161944637)
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



# #LOOPS
# @tasks.loop(seconds = 86400*2)
# async def how_are_you():
# 	await asyncio.sleep(86400)
# 	this_channel = bot.get_guild(795726142161944637).get_channel(842185255221198858)
# 	greetings = ["Whats up nibbe", "Hows it going nibbe?", "How have you been nibbe?", "How are you doing nibbe?", "Check pins",
# 	"Whats cooking nibbe?", "Long time no see nibbe...", "Sup nibbe?", "Hey nibbe", "What’s up Ameena", "Whats cooking nibbe?",
# 	"Kiya howa?", "Kiya chal raha hay?", "You ok nibbe?", "Idk why im doing this...", "Why am i doing this again...?", "Sigh"]
# 	# return await this_channel.send(f"<@723242226855182468> {randchoice(greetings)}")
# 	print({randchoice(greetings)})

# @tasks.loop(seconds = 86400*2)
# async def playlist():
# 	await asyncio.sleep(86400)
# 	embed = Embed(description="**[My stupid playlist](spotify:playlist:1eoCjzINYSgvJXDbt6T7kA) \n [Ahh Sad Boy Hours Sigh](spotify:playlist:7Mu7AxSsveFAWtN9kUnOEf) \n [Take this one also cuz why not](spotify:playlist:5ESl8XOwhjt8PD2gHzWMxn) \n Idk why im doing this...**",
# 		color=embed_color)
# 	# return await this_channel.send(embed=embed)
# 	print("2nd loop")



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#



#ON READY EVENT
@bot.event
async def on_ready():
	config_channel = bot.get_guild(795726142161944637).get_channel(859726638111260692)
	# how_are_you.start()
	# playlist.start()
	await bot.change_presence(status = discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name="Emptiness"))
	choice = ["`/help` for help!", "Stop getting pissed on me restarting please, get a life", "Just mute this channel bruh", "Sorry i cant help it", "Use `/help` to view all my commands and functions!",
	"Use `/help` to view all commands", "Why am i doing this again?", "Uhhh ffs", "Send help please", "No one here to say `ily` to me?",
	"No one here to say `imy` to me?", "Reply to someone with either `gay` or `ban`, then watch the magic happen...", "Send nudes please \n k thx bye", "But that still doesnt change the fact that quantum mechanics allows particles to be created and destroyed and requires only the presence of suitable interactions carrying sufficient energy. Quantum field theory also stipulates that the interactions can extend over a distance only if there is a particle, or field quantum, to carry the force.",
	"But that still doesnt change the fact that theory of plate tectonics states that the Earth's solid outer crust, the lithosphere, is separated into plates that move over the asthenosphere, the molten upper portion of the mantle. Oceanic and continental plates come together, spread apart, and interact at boundaries all over the planet.",
	"Osama bin Mohammed bin Awad bin Laden, aka <@868540085971341362>, March 10, 1957 – May 2, 2011, also rendered as Usama bin Ladin, was a founder of the pan-Islamic militant organization al-Qaeda.He was a Saudi Arabian citizen until 1994 and a member of the wealthy bin Laden family. Bin Laden's father was Mohammed bin Awad bin Laden, a Saudi millionaire from Hadhramaut, Yemen, and the founder of the construction company, Saudi Binladin Group. His mother, Alia Ghanem, was from a secular middle-class family in Latakia, Syria. He was born in Saudi Arabia and studied at university in the country until 1979, when he joined Mujahideen forces in Pakistan fighting against the Soviet Union in Afghanistan. He helped to fund the Mujahideen by funneling arms, money, and fighters from the Arab world into Afghanistan, and gained popularity among many Arabs. In 1988, he formed al-Qaeda. He was banished from Saudi Arabia in 1992, and shifted his base to Sudan, until U.S. pressure forced him to leave Sudan in 1996. After establishing a new base in Afghanistan, he declared a war against the United States, initiating a series of bombings and related attacks. Bin Laden was on the American Federal Bureau of Investigation's (FBI) lists of Ten Most Wanted Fugitives and Most Wanted Chad for his involvement in the 1998 U.S. embassy bombings.",
	"Im gonna fly some planes into a couple buildings in Manhattan \n I-m I-m <@868540085971341362> \n Run tell Obama \n Im your fucking uncle...", "Are you in the mood for 72 virgins? \n And i dont mean dudes who get your computer working", "Will there ever be Middle East peace? \n Nigga please... \n There will always be one or two jehads *atleast*", "Hey <@868540085971341362> kill Obama bismillah..."]
	
	await config_channel.send("<:uhh:847601058904932362>")
	await config_channel.send(f"{randchoice(choice)}")
	
	# gateway = bot.get_guild(795726142161944637).get_channel(826460762695270432)
	# embed = Embed(description="**Ping either <@726480855689724105> or <@723242226855182468> for roles**", color=embed_color)
	# embed.set_author(name="Welcome To Empty", icon_url = "https://cdn.discordapp.com/emojis/847601058904932362.png?v=1")
	# await gateway.send(embed=embed)
	
	print("Bot is Ready")


with open("./token.json") as f:
	config = json.load(f)

token = config.get("token")
bot.run(token)

