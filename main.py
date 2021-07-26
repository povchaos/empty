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

bot = commands.Bot(description = "Chaos op", command_prefix = "!")
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

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
@slash.slash(name="help",description="Stop it, Get some help")
async def show_help(ctx):
	guild = ctx.guild
	embed = Embed(title="Help",
		description=f"I have a total of **8** commands",
		color=0x000000)
	embed.add_field(name = "Miscellaneous Commands", value = " `ping`, `setnick`, `avatar`, `role`, `remindme`", inline = False)
	embed.add_field(name = "Moderation Commands", value = "`kick`, `ban`", inline = False)
	embed.set_thumbnail(url = guild.me.avatar_url)
	await ctx.send(embed=embed)


#ROLE COMMAND
@slash.slash(name="role", description="Add or remove user roles")
async def roles(ctx, target: discord.Member, role: discord.Role):
	try:	
		if role not in target.roles:
			await target.add_roles(role)
			embed = Embed(description=f"Added **{role.mention}** to **{target.mention}**", color=0x000000)
			await ctx.send(embed=embed)

		else:
			await target.remove_roles(role)
			embed = Embed(description=f"Removed **{role.mention}** from **{target.mention}**",  color=0x000000)
			await ctx.send(embed=embed)
	
	except Forbidden:
		embed = Embed(description=f"You cannot edit roles for {target.mention}", color=0x000000)
		await ctx.send(embed=embed)

@bot.command(name="say")
async def say(ctx, message):
	await ctx.channel.send(f"{message}")

@bot.command(name="embed")
async def embed(ctx, message):
	embed = Embed(description = f"{message}", color = 0x000000)
	await ctx.channel.send(embed=embed)


#SET NICK COMMAND
@slash.slash(name="setnick", description="Change User Nicknames")
async def set_nick(ctx, target: discord.Member, nickname):
	try:
		await target.edit(nick=nickname)
		embed = Embed(description=f"Changed **{target.name}#{target.discriminator}**'s name to **{nickname}**", color=0x000000)
		await ctx.send(embed=embed)
	except Forbidden:
		await ctx.send(f"I cant change **{target.name}#{target.discriminator}**'s name")


#REMINDER COMMAND
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
			color=0x000000)
		try:
			await ctx.author.send(embed=embed)
		
		except:
			await ctx.channel.send(f"||{ctx.author.mention}||",embed=embed)

	except:
		return await ctx.send("Please enter either `s`, `m`, `h` or `d` after the integer in reminder time!")


#AV COMMAND
@slash.slash(name="avatar",description="User avatar")
async def avatar(ctx, target: Optional[discord.Member]):
	target = target or ctx.author
	embed = Embed(title=f"{target.display_name}'s Avatar",url=f"{target.avatar_url}",color=0x000000)
	embed.set_image(url=f"{target.avatar_url}")
	await ctx.send(embed = embed)


#PING COMMAND
@slash.slash(name="ping", description="Bot Latency")
async def ping(ctx):
	embed = Embed(description=f"Pong! Latency is **{round(bot.latency*1000)}** ms",color=0x000000)
	await ctx.send(embed=embed)


#KICK COMMAND
@slash.slash(name="kick", description="Kick Users")
async def kick(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.kick(reason = reason)
	embed = Embed(description=f"Successfully kicked **{target.name}#{target.discriminator}**", color=0x000000)
	await ctx.send(embed=embed)


#BAN COMMAND
@slash.slash(name="ban", description="Ban Users")
async def ban(ctx, target: discord.Member, reason = Optional[str] == "No reason provided"):
	await target.ban(reason = reason)
	embed = Embed(description=f"Successfully banned **{target.name}#{target.discriminator}**", color=0x000000)
	await ctx.send(embed=embed)


#ON MESSAGE EVENT
@bot.event
async def on_message(message):
	if bot.user.mentioned_in(message) and message.content.startswith("<") and message.content.endswith(">"):
		await message.reply(content="Try using slash commands aka `/`")
	
	if not message.author.bot:
		if isinstance(message.channel, DMChannel):
			logs_channel = bot.get_guild(795726142161944637).get_channel(868251065546584124)
			embed = Embed(title="DM Received",
				description=f"**Message By:** \n {message.author.mention}丨{message.author.name}#{message.author.discriminator} \n\n **Message:** \n {message.content}",
				color=0x000000,
				timestamp=datetime.utcnow())
			embed.set_thumbnail(url = f"{message.author.avatar_url}")
			await logs_channel.send(embed=embed)
			await message.add_reaction("✅")

	if message.channel.id == 842185255221198858 or message.channel.id == 859122987071569950:
		choice = ["<:blush~2:846912330465017886>", "<:uhh:847601058904932362>", "<:hug:846912225431126076>", "<:salute:846442131400556564>", "<:Boznis:851800792926257152>",
		"<:umm:842192405754806342", ":aamna:862291911611777054>", "<:whenlifegetsyou:862326647976624188>", "<:sweat~1:820756196876615710>"]
		emoji = randchoice(choice)
		
		if "chaos" in message.content or "Chaos" in  message.content or "ahmed" in  message.content or "Ahmed" in message.content:
			await message.add_reaction(f"{emoji}")
		
		if "aamna" in message.content or "Aamna" in  message.content:
			await message.add_reaction(f"{emoji}")

		if "hades" in message.content or "Hades" in message.content:
			await message.add_reaction(f"{emoji}")

		if "dirtygamer" in message.content or "Dirtygamer" in message.content or "Hashir" in message.content or "hashir" in message.content:
			await message.add_reaction(f"{emoji}")
		
		
	if message.channel.id == 842185255221198858:
		if "ily" in message.content or "Ily" in message.content:
			await message.reply(f"Ily 2 nibbe {emoji}")


	if not bot.user == message.author:
		if message.channel.id == 869011766066163742:
			if "@everyone" not in message.content and "@here" not in message.content:
				
				try:
					async with randomstuff.AsyncClient(api_key="tQeJ9s1ZRUQt") as client:
						response = await client.get_ai_response(message.content)
						await message.reply(response.message)
				
				except:
					pass
					
			else:
				await message.reply("You really thought that would work? <:yay:867816037079318568>")
 

#ON MEMBER JOIN EVENT
@bot.event
async def on_member_join(ctx, member):
	logs_channel = bot.get_guild(795726142161944637).get_channel(868251065546584124)
	
	embed = Embed(title=f"{member.name} Just joined {ctx.guild.name}!", 
						color =0x000000, timestap=datetime.utcnow())
	embed.set_thumbnail(url=member.avatar_url)
	fields = [("Name", f"{member.mention}丨{member.name}#{member.discriminator}", False),
				("ID", f"{member.id}", False),				
				("Joined at", member.joined_at.strftime("%d/%m/%Y"), True),
				("Create at", member.created_at.strftime("%d/%m/%Y"), True),
				("Status", str(member.status).title(), True)]	
	for name, value, inline in fields:
		embed.add_field(name=name, value=value, inline=inline)

	await logs_channel.send("`@everyone`",embed=embed)

	embed_2 = Embed(title="Member Roles",
		description=f"Do you want me to hand out <@&818950383216623696> role to {member.mention}? \n Please react accordingly",
		color=0x000000)

	this = await logs_channel.send(embed=embed_2)
	await this.add_reaction("✅")
	await this.add_reaction("❌")


#ON MESSAGE DELETE EVENT
@bot.event
async def on_message_delete(message):
	logs_channel = bot.get_guild(795726142161944637).get_channel(826461301806334003)
	guild = bot.get_guild(795726142161944637)
	if message.mentions:
		if not message.author == guild.me:
			for s in message.mentions:
				channel_embed=Embed(title="Ghost Ping",
					description=f"**{s.mention} was ghost pinged by {message.author.mention}**",
					color=0x000000, 
					timestamp=datetime.utcnow())
				fields = [("Message", f"{message.content}", False)]
				for name, value, inline in fields:
					channel_embed.add_field(name=name, value=value, inline=inline)
				await message.channel.send(embed=channel_embed)
				
				log_embed=Embed(title="Ghost Ping",color=0x000000, timestamp=datetime.utcnow())
				log_embed.set_thumbnail(url=f"{message.author.avatar_url}")
				fields = [("Ping By", f"{message.author.name}#{message.author.discriminator}", True),
						("Ping To", f"{s.name}#{s.discriminator}", False),
						("Channel", message.channel.mention , True),
						("Message", message.content , False)]
				for name, value, inline in fields:
					log_embed.add_field(name=name, value=value, inline=inline)
				return await logs_channel.send(embed=log_embed)

#ON READY EVENT
@bot.event
async def on_ready():
	config_channel = bot.get_guild(795726142161944637).get_channel(859726638111260692)
	await bot.change_presence(status = discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name="Emptiness"))
	await config_channel.send("<:uhh:847601058904932362>")
	print("Bot is Ready")

with open("./token.json") as f:
	config = json.load(f)

token = config.get("token")
bot.run(token)

