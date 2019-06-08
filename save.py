import pickle

class halo_song(object):
	def __init__(self, game, track):
		self.game = game
		self.track = track

	def get_url(self):
		return halo_songs[self.game][self.track][1]

	def get_name(self):
		return halo_songs[self.game][self.track][0]
		
class halo_server:
	def __init__(self, halo_voice_channel, halo_text_channel):
		self.halo_voice_channel	= halo_voice_channel # string
		self.halo_text_channel 	= halo_text_channel	# string
		
		self.song = halo_song("1", 0)
		
	def __str__(self):
		str = ""

		str += "halo_voice_channel: {}".format(self.halo_voice_channel)
		str += "\nhalo_text_channel: {}".format(self.halo_text_channel)

		return str

halo_servers = {}

halo_servers[0] = halo_server("test", "hi")
print(halo_servers[0])

with open('halo_servers.pkl', 'wb') as f:
	pickle.dump(halo_servers, f)
