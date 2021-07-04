import discord, json, pyfiglet, time
from discord.ext import commands
from discord import Embed, DMChannel
import asyncio
from discord.ext import tasks
from datetime import datetime
from discord_slash import SlashCommand
from discord.errors import Forbidden
from typing import Optional


bot = commands.Bot(description = "Chaos op", command_prefix = "!")
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)


#HELP COMMAND
@slash.slash(name="help",description="Stop it, Get some help")
async def show_help(ctx):
	guild = ctx.guild
	embed = Embed(title="Help",
		description=f"I have a total of **{len(bot.commands)}** commands",
		color=0x000000)
	embed.add_field(name = "Miscellaneous Commands", value = " `ping`, `setnick`, `avatar`, `role`", inline = False)
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


#SET NICK COMMAND
@slash.slash(name="setnick", description="Change User Nicknames")
async def set_nick(ctx, target: discord.Member, nickname):
	try:
		await target.edit(nick=nickname)
		embed = Embed(description=f"Changed **{target.name}#{target.discriminator}**'s name to **{nickname}**", color=0x000000)
		await ctx.send(embed=embed)
	except Forbidden:
		await ctx.send(f"I cant change **{target.name}#{target.discriminator}**'s name")


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
		await message.reply(content="My prefix is `!` \n Im based on slash commands aka `/`")
		print(bot.commands)


#ON READY EVENT
@bot.event
async def on_ready():
	config_channel = bot.get_guild(795726142161944637).get_channel(859726638111260692)
	await bot.change_presence(status = discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name="Mistakes"))
	print("Bot is Ready")

with open("./token.json") as f:
	config = json.load(f)

token = config.get("token")
bot.run(token)

