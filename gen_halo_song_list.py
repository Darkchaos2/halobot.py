from __future__ import unicode_literals
import youtube_dl

url = 'https://www.youtube.com/watch?v=UbMxGrTVovg&list=PLVFu5mCs8PVi9gzKmuNwqDmRTMNYmHgDR'

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)

def my_hook(d):
	print(d)
	if d['status'] == 'finished':
		print('Done downloading, now converting ...')
		# halo_songs["1"].append(d.filename)

ydl_opts = {
	'format': 'best',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
}

halo_songs = []

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	info_dict = ydl.extract_info(url, download=False)

	for video in info_dict["entries"]:
		halo_songs.append([video["title"], video["webpage_url"]])


print(halo_songs)