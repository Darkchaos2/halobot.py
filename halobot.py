import discord
from discord.ext import commands
from discord.ext.commands import Bot
import youtube_dl
import pickle
import asyncio

client = commands.Bot(command_prefix = 'halo')

next_halo = {
	"1": "2", 
	"2": "3", 
	"3": "3odst", 
	"3odst": "reach", 
	"reach": "4", 
	"4": "5", 
	"5": "infinite", 
	"infinite": "1"
}

halo_songs = {
	"1": [
		["original theme", "https://www.youtube.com/watch?v=0jXTBAGv9ZQ"]
	],
	"2": [
		["original theme", "https://www.youtube.com/watch?v=xheb3JowLVs"]
	],
	"3": [
		["original theme", "https://www.youtube.com/watch?v=IiIltLoN-6Q"]
	],
	"3odst": [
		["original theme", "https://www.youtube.com/watch?v=2hqStgAJ1Io"]
	],
	"4": [
		["original theme", "https://www.youtube.com/watch?v=uWi6quC8zSk"]
	],
	"5": [
		["original theme", "https://www.youtube.com/watch?v=MKVbMZGeA3Y"]
	],
	"infinite": [
	]
}

halo_voice_channel = ""
halo_text_channel = ""
opts = {}

servers = {}
players = {}

class Halo_song(object):
	game = ""
	track = 0

	def __init__(self, game, track):
		self.game = game
		self.track = track

class DServer:
	def __init__(self, halo_voice_channel_id, halo_text_channel_id, voice_client):
		self.halo_voice_channel_id	= halo_voice_channel_id # string
		self.halo_text_channel_id 	= halo_text_channel_id	# string
		self.voice_client 			= voice_client			# discord.voice_client

		self.current_song 			= Halo_song("1", 0)		# Halo_song
		self.current_player 		= ""					# ytdlplayer

		self.next_halo_song 		= ""					# Halo_song
		self.next_halo_player 		= asyncio.Queue()		# list of players

		self.queue 					= asyncio.Queue()		# list of 

		self.play_next_song 		= asyncio.Event()		#
		self.audio_player 			= client.loop.create_task(self.audio_player_task())

	def toggle_next(self):
		print("toggled")
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

	async def audio_player_task(self):
		while True:
			print("1")
			self.play_next_song.clear()
			print("2")

			self.current_player = await self.next_halo_player.get()
			print("3")

			await self.bot.send_message(self.halo_text_channel_id, 'Now playing ' + str(self.current_song))
			print("4")
			self.player.start()
			print("5")
			await self.play_next_song.wait()
			print("6")

# async def find_next_song(server_id):
# 	if servers[server_id].queue != []:
# 		play_next_queued_song(server_id)
# 		return

# 	await play_next_autoplay_song(server_id)

async def find_next_queued_song(server_id):
	return servers[server_id].queue.pop(0)
	# await play(server_id, servers[server_id].current_song)

async def find_next_autoplay_song(server_id):
	current_game = servers[server_id].current_song.game
	current_track = servers[server_id].current_song.track

	if halo_songs[current_game][current_track + 1]:
		return Halo_song(current_game, current_track + 1)
	else:
		return Halo_song(next_halo[current_game], 0)

async def play_autosong(server_id):
	current_game = servers[server_id].current_song.game
	current_track = servers[server_id].current_song.track

	await play(server_id, halo_songs[current_game][current_track][1])

async def play(server_id, track):
	print(servers[server_id].current_player)
	print(servers[server_id].next_halo_player)
	dserver = servers[server_id]

	player = await dserver.voice_client.create_ytdl_player(track, ytdl_options = opts, after = lambda: dserver.toggle_next())
	servers[server_id].current_player = player
	player.start()

	if servers[server_id].queue != []:
		# stub
		# next_track = find_next_queued_song(server_id)
		# next_player = await dserver.voice_client.create_ytdl_player(next_track, ytdl_options = opts, after = lambda: dserver.toggle_next())
		# dserver.next
		return
	else:
		next_track = find_next_autoplay_song(server_id)
		next_player = await dserver.voice_client.create_ytdl_player(next_track, ytdl_options = opts, after = lambda: dserver.toggle_next())
		dserver.next_halo_song = next_track
		dserver.next_halo_player = next_player
		print(servers[server_id].current_player)
		print(servers[server_id].next_halo_player)

@client.event
async def on_ready():
	print("Ready")

	print("Connecting to Halo channel...")
	halo_voice_channel = client.get_channel("350441096259829760")
	halo_text_channel = client.get_channel("351468167928741888")

	for server_id, dserver in servers.items():
		print("Joining server: " + server_id)
		await client.join_voice_channel(servers[server_id].halo_voice_channel_id)

	print("Connected!")

	print("Downloading Halo music")
	opts = {
		'default_search': 'auto',
		'quiet': True,
	}

	# server = halo_voice_channel.server
	# voice_client = client.voice_client_in(server)
	# player = await voice_client.create_ytdl_player(halo_songs["1"][0][1], ytdl_options=opts, after=lambda: on_song_end(server.id))
	# servers[server.id] = DServer(player, Halo_song("1", 0))

	# print("Playing Halo music")
	# player.start()

	# for server_id, dserver in servers.items():
	# 	play_autosong()

@client.command(pass_context = True)
async def setchannel(ctx):
	author_voice_channel = ctx.message.author.voice_channel
	author_text_channel = ctx.message.channel
	server = ctx.message.server

	if author_voice_channel is None:
		await self.bot.say('Please join a voice channel.')
		return False

	await client.join_voice_channel(author_voice_channel)

	voice_client = client.voice_client_in(server)
	# player = await voice_client.create_ytdl_player(halo_songs["1"][0][1], ytdl_options=opts, after=lambda: on_song_end(server.id))
	servers[server.id] = DServer(author_voice_channel, author_text_channel, voice_client)

	print(servers[server.id].current_player)
	print(servers[server.id].next_halo_player)

	await play_autosong(server.id)

@client.command(pass_context = True)
async def skip(ctx):
	dserver = servers[ctx.message.server.id]
	dserver.current_player.stop()


client.run("ahhhh")