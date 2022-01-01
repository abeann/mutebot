import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')

msg = None
vc  = None

@bot.event
async def on_ready():
    print("MuteBot is online!")

@bot.command()
@commands.has_permissions(administrator=True)
async def mbping(ctx):
    global msg
    msg = await ctx.send('Mute All')
    await msg.add_reaction('❗')
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def mbvc(ctx, arg: discord.VoiceChannel):
    global vc
    vc = arg
    await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    if (payload.user_id != 776571880194572288 and 
    payload.message_id == msg.id and 
    payload.member.guild_permissions.administrator and 
    payload.emoji.name == '❗'):
        member_ids = vc.voice_states.keys()
        for key in member_ids:
            member = await payload.member.guild.fetch_member(key)
            await member.edit(mute=True)

@bot.event 
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if (payload.message_id == msg.id and 
    message.author.guild_permissions.administrator and
    payload.emoji.name == '❗'):
        member_ids = vc.voice_states.keys()
        for key in member_ids:
            member = await message.author.guild.fetch_member(key)
            await member.edit(mute=False)

bot.run('token')
