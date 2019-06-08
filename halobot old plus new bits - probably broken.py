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
		["original theme", "https://www.youtube.com/watch?v=sCxv2daOwjQ"]
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

class DServer(object):
	halo_voice_channel_id	= ""
	halo_text_channel_id 	= ""
	voice_client 			= ""
	next_autoplay_player 	= Halo_song("1", 0)
	current_song 			= ""
	current_player 			= ""
	queue 					= asyncio.Queue()
	play_next_song 			= asyncio.Event()

	def __init__(self, halo_voice_channel_id, voice_client, player, song):
		self.halo_voice_channel_id = halo_voice_channel_id
		self.voice_client = voice_client
		self.current_player = player
		self.song = song

	def toggle_next(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

	async def audio_player_task(self):
		while True:
			self.play_next_song.clear()
			self.current = await self.queue.get()
			await self.bot.send_message(self.halo_text_channel_id, 'Now playing ' + str(self.current_song))
			self.player.start()
			await self.play_next_song.wait()

# async def find_next_song(server_id):
# 	if servers[server_id].queue != []:
# 		play_next_queued_song(server_id)
# 		return

# 	await play_next_autoplay_song(server_id)

async def find_next_queued_song(server_id):
	return servers[server_id].current_song = servers[server_id].queue.pop(0)
	# await play(server_id, servers[server_id].current_song)

async def find_next_autoplay_song(server_id):
	current_game = servers[server_id].current_autoplay.game
	current_track = servers[server_id].current_autoplay.track

	if halo_songs[current_game][current_track + 1]:
		server[server_id].current_autoplay.track = current_track + 1
		await play_autosong(server_id)
	else:
		server[server_id].current_autoplay.game = next_halo[current_game]
		server[server_id].current_autoplay.track = 0
		await play_autosong(server_id)

async def play_autosong(server_id):
	current_game = servers[server_id].current_autoplay.game
	current_track = servers[server_id].current_autoplay.track

	await play(server_id, halo_songs[current_game][current_track][1])

async def play(server_id, track):
	dserver = servers[server_id]

	player = await dserver.voice_client.create_ytdl_player(track, ytdl_options = opts, after = lambda: dserver.toggle_next())
	servers[server_id].player = player
	player.start()

	if servers[server_id].queue != []:
		#stub
		# next_track = find_next_queued_song(server_id)
		# next_player = await dserver.voice_client.create_ytdl_player(next_track, ytdl_options = opts, after = lambda: dserver.toggle_next())
		# dserver.next
		return
	else:
		next_track = find_next_autoplay_song(server_id)
		next_player = await dserver.voice_client.create_ytdl_player(next_track, ytdl_options = opts, after = lambda: dserver.toggle_next())
		dserver.next_autoplay

	await play_next_autoplay_song(server_id)

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
	author_channel = ctx.message.author.voice_channel
	server = ctx.message.server

	if author_channel is None:
		await self.bot.say('Please join a voice channel.')
		return False

	await client.join_voice_channel(author_channel)

	# voice_client = client.voice_client_in(server)
	# player = await voice_client.create_ytdl_player(halo_songs["1"][0][1], ytdl_options=opts, after=lambda: on_song_end(server.id))
	# servers[server.id] = DServer(author_channel, voice_client, player, Halo_song("1", 0))

	await play_autosong(server.id)

@client.command(pass_context = True)
async def skip(ctx):
	dserver = servers[ctx.message.server.id]
	dserver.player.stop()


client.run("lol")