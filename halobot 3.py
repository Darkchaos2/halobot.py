import discord
from discord.ext import commands
from discord.ext.commands import Bot
import youtube_dl
import pickle
import asyncio

client = commands.Bot(command_prefix = 'halo')
# client.remove_command('help')

next_game = {
	"1": "2", 
	"2": "3", 
	"3": "3 ODST", 
	"3 ODST": "Reach", 
	"Reach": "4", 
	"4": "5", 
	"5": "1", 
	"Infinite": "1"
}
halo_songs = {
	"1": [['Halo: Combat Evolved OST 01 Opening Suite', 'https://www.youtube.com/watch?v=OpkSer8CNsA'], ['Halo: Combat Evolved OST 02 Truth and Reconciliation Suite', 'https://www.youtube.com/watch?v=lj91a6W91J8'], ['Halo: Combat Evolved OST 03 Brothers in Arms', 'https://www.youtube.com/watch?v=aQHZCP0ew88'], ['Halo: Combat Evolved OST 04 Enough Dead Heroes', 'https://www.youtube.com/watch?v=BVG6CPrLc8w'], ['Halo: Combat Evolved OST 05 Perilous Journey', 'https://www.youtube.com/watch?v=0obow-wqPb0'], ['Halo: Combat Evolved OST 06 A Walk in the Woods', 'https://www.youtube.com/watch?v=y6DdRv6NIyY'], ['Halo: Combat Evolved OST 07 Ambient Wonder', 'https://www.youtube.com/watch?v=YxCxOwIR7HU'], ['Halo: Combat Evolved OST 08 The Gun Pointed at the Head of the Universe', 'https://www.youtube.com/watch?v=4n0EUieJQsM'], ['Halo: Combat Evolved OST 09 Trace Amounts', 'https://www.youtube.com/watch?v=9jOl3ttI0Pk'], ['Halo: Combat Evolved OST 10 Under Cover of Night', 'https://www.youtube.com/watch?v=v_lGYVlcx_I'], ['Halo: Combat Evolved OST 11 What Once Was Lost', 'https://www.youtube.com/watch?v=8EBCsTeYU6Y'], ['Halo: Combat Evolved OST 12 Lament for PVT. Jenkins', 'https://www.youtube.com/watch?v=3prOeAcjQPQ'], ['Halo: Combat Evolved OST 13 Devils... Monsters', 'https://www.youtube.com/watch?v=56w4VLURmGI'], ['Halo: Combat Evolved OST 14 Covenant Dance', 'https://www.youtube.com/watch?v=A8Qo6Ex8PbI'], ['Halo: Combat Evolved OST 15 Alien Corridors', 'https://www.youtube.com/watch?v=EaBf2ofuScc'], ['Halo: Combat Evolved OST 16 Rock Anthem for Saving the World', 'https://www.youtube.com/watch?v=6Wcqnofddtc'], ['Halo: Combat Evolved OST 17 The Maw', 'https://www.youtube.com/watch?v=b-vfBD1XS9Y'], ['Halo: Combat Evolved OST 18 Drumrun', 'https://www.youtube.com/watch?v=n-JisjFOfK0'], ['Halo: Combat Evolved OST 19 On a Pale Horse', 'https://www.youtube.com/watch?v=cvaEIiboA8w'], ['Halo: Combat Evolved OST 20 Perchance to Dream', 'https://www.youtube.com/watch?v=PZVQ6s0IOhI'], ['Halo: Combat Evolved OST 21 Library Suite', 'https://www.youtube.com/watch?v=e87BLzzcwqQ'], ['Halo: Combat Evolved OST 22 The Long Run', 'https://www.youtube.com/watch?v=CulUEa_z71U'], ['Halo: Combat Evolved OST 23 Suite Autumn', 'https://www.youtube.com/watch?v=17EW8i5B_Wc'], ['Halo: Combat Evolved OST 24 Shadows', 'https://www.youtube.com/watch?v=kGT5ycHye5M'], ['Halo: Combat Evolved OST 25 Dust and Echoes', 'https://www.youtube.com/watch?v=oJtPF-Hh8sI'], ['Halo: Combat Evolved OST 26 Halo', 'https://www.youtube.com/watch?v=Bzrnw4niuTA']],
	"2": [['Halo 2 Anniversary OST - Halo Theme Gungnir Mix (feat. Steve Vai)', 'https://www.youtube.com/watch?v=L6R8fE2OU3E'], ['Halo 2 Anniversary OST - Skyline', 'https://www.youtube.com/watch?v=-1MaWNfo5xQ'], ['Halo 2 Anniversary OST - Not a Number', 'https://www.youtube.com/watch?v=F-QCjTBR0Pg'], ['Halo 2 Anniversary OST - Kilindini Harbour', 'https://www.youtube.com/watch?v=E0p_1CaiRoA'], ['Halo 2 Anniversary OST - Only a Star, Only the Sea', 'https://www.youtube.com/watch?v=-GhvkU1SNjs'], ['Halo 2 Anniversary OST - A Spartan Rises', 'https://www.youtube.com/watch?v=JZxMtTLk-GI'], ['Halo 2 Anniversary OST - Unforgotten Memories', 'https://www.youtube.com/watch?v=R2HS-xmHOdI'], ['Halo 2 Anniversary OST - Second Prelude', 'https://www.youtube.com/watch?v=Rpu8u4ghZ2E'], ['Halo 2 Anniversary OST - This Glittering Band', 'https://www.youtube.com/watch?v=9ZFFYtbwX3c'], ['Halo 2 Anniversary OST - Jeopardy', 'https://www.youtube.com/watch?v=5tEGjrKxVl8'], ['Halo 2 Anniversary OST - Halo Theme Scorpion Mix', 'https://www.youtube.com/watch?v=r_Wz4HVn2l8'], ['Halo 2 Anniversary OST - Punishment', 'https://www.youtube.com/watch?v=GIVW5JgYSns'], ['Halo 2 Anniversary OST - Promise the Girl', 'https://www.youtube.com/watch?v=9ZW9D6TBPs8'], ['Halo 2 Anniversary OST - Unsullied Memory', 'https://www.youtube.com/watch?v=r-H69Zngb6E'], ['Halo 2 Anniversary OST - Arise in Valor', 'https://www.youtube.com/watch?v=3IKeQB2dB_s'], ['Halo 2 Anniversary OST - Unwearied Heart', 'https://www.youtube.com/watch?v=-5qrsLVSWb8'], ["Halo 2 Anniversary OST - Spartan's Regret", 'https://www.youtube.com/watch?v=YuUREENIYjE'], ['Halo 2 Anniversary OST - Genesong (feat. Steve Vai)', 'https://www.youtube.com/watch?v=h6oHQhDM73w'], ['Halo 2 Anniversary OST - Breaking the Covenant', 'https://www.youtube.com/watch?v=4gXAcoBT_XI'], ['Halo 2 Anniversary OST - Follow In Flight', 'https://www.youtube.com/watch?v=lviYhyN_VKI'], ['Halo 2 Anniversary OST - Cryptic Whisper', 'https://www.youtube.com/watch?v=Dnt32i1Ck58'], ['Halo 2 Anniversary OST - Impart', 'https://www.youtube.com/watch?v=f86GM-17s-g'], ["Halo 2 Anniversary OST - Charity's Irony", 'https://www.youtube.com/watch?v=GB-rZzLH0l0'], ['Halo 2 Anniversary OST - Moon Over Mombasa', 'https://www.youtube.com/watch?v=tTi0EbPCCNo'], ['Halo 2 Anniversary OST - Trapped In Amber', 'https://www.youtube.com/watch?v=BfePwIuGxwo'], ["Halo 2 Anniversary OST - Builder's Legacy", 'https://www.youtube.com/watch?v=-HgiI3fXnqM'], ['Halo 2 Anniversary OST - Moon Over Mombasa (part 2)', 'https://www.youtube.com/watch?v=9y4bxue1rUU'], ["Halo 2 Anniversary OST - Librarian's Gift", 'https://www.youtube.com/watch?v=tsZAtqEzC24'], ['Halo 2 Anniversary OST - Zealous Champion', 'https://www.youtube.com/watch?v=1YIVQ_1G_Xo'], ['Halo 2 Anniversary OST - Steward, Sheperd, Lonely Soul', 'https://www.youtube.com/watch?v=Er-1D1uOK0Q'], ['Halo 2 Anniversary OST - Africa Suite', 'https://www.youtube.com/watch?v=YjGlLTqnirk'], ['Halo 2 Anniversary OST - Prophet Suite', 'https://www.youtube.com/watch?v=ycK3MUKTU30'], ['Halo 2 Anniversary OST - Cracked Legend', 'https://www.youtube.com/watch?v=KAgLsG48lec'], ['Halo 2 Anniversary OST - Menace No More', 'https://www.youtube.com/watch?v=B3i6cuLUqUE'], ['Halo 2 Anniversary OST - Into the Belly of the Beast', 'https://www.youtube.com/watch?v=MIkfnH-7VPs'], ['Halo 2 Anniversary (songs not on OST) - Home Field Invasion', 'https://www.youtube.com/watch?v=gLt4zUonohM'], ['Halo 2 Anniversary (songs not on OST) - Common Areas B1', 'https://www.youtube.com/watch?v=IBpAGanmM74'], ['Halo 2 Anniversary (songs not on OST) - A Day at the Beach', 'https://www.youtube.com/watch?v=RqrvTggMjtw'], ['Halo 2 Anniversary (songs not on OST) - Lethbridge Industrial', 'https://www.youtube.com/watch?v=td2vStQ-f5U'], ['Halo 2 Anniversary (songs not on OST) - Halo Theme Scarab Mix', 'https://www.youtube.com/watch?v=JhBWu700g-E'], ['Halo 2 Anniversary (songs not on OST) - Common Areas B2', 'https://www.youtube.com/watch?v=zsiKyJ6JOE8'], ['Halo 2 Anniversary (songs not on OST) - Trapped In a Postcard', 'https://www.youtube.com/watch?v=uVvDuyyeT1Y'], ['Halo 2 Anniversary (songs not on OST) - Flood Dance', 'https://www.youtube.com/watch?v=zsQwfVrtcuI'], ['Halo 2 Anniversary (songs not on OST) - Sacred, Sanctified, Defiled', 'https://www.youtube.com/watch?v=tZN5ZgzA_kg'], ['Halo 2 Anniversary (songs not on OST) - Scent of War', 'https://www.youtube.com/watch?v=ZbokPGU-yf4'], ['Halo 2 Anniversary (songs not on OST) - Shooting Gallery', 'https://www.youtube.com/watch?v=s2Y3D1TRPNQ'], ['Halo 2 Anniversary (songs not on OST) - "Shooting Gallery" and "Scent of War" remix', 'https://www.youtube.com/watch?v=9_Joznx0MJc'], ['Halo 2 Anniversary (songs not on OST) - Unyielding Soul', 'https://www.youtube.com/watch?v=M6EHkAvFKec'], ['Halo 2 Anniversary OST - "Peril" and "Jeopardy" remix', 'https://www.youtube.com/watch?v=Peeu5SfXT5g'], ['Halo 2 Anniversary OST - "Infected" and "Menace No More" remix', 'https://www.youtube.com/watch?v=GJ_92gMWOfw'], ['Halo 2 Anniversary OST - "Earth City" and "Kilindini Harbour" remix', 'https://www.youtube.com/watch?v=NfnQinfhNH8'], ['Halo 2 Anniversary OST - "Heretic, Hero" and "Zealous Champion" remix', 'https://www.youtube.com/watch?v=7mII29u0k0w'], ['Halo 2 Anniversary OST - "Flawed Legacy" and "Cracked Legend" remix', 'https://www.youtube.com/watch?v=n9w8QVhbIc0'], ['Halo 2 Anniversary OST - "In Amber Clad" and "Trapped in Amber" remix', 'https://www.youtube.com/watch?v=k2qbS8gqKZc'], ['Halo 2 Anniversary OST - "Pursuit of Truth" and "Charity\'s Irony" remix', 'https://www.youtube.com/watch?v=EJ1ykdne5mY']],
	"3": [['Halo 3 OST - Luck', 'https://www.youtube.com/watch?v=UbMxGrTVovg'], ['Halo 3 OST - Released', 'https://www.youtube.com/watch?v=BJAfrL889CQ'], ['Halo 3 OST - Infiltrate', 'https://www.youtube.com/watch?v=XhAjqJxk6go'], ['Halo 3 OST - Honorable Intentions', 'https://www.youtube.com/watch?v=ieMVzNKM47Y'], ['Halo 3 OST - Last of the Brave', 'https://www.youtube.com/watch?v=t74nS_wddyE'], ['Halo 3 OST - Brutes', 'https://www.youtube.com/watch?v=ChTaYGgJFh0'], ['Halo 3 OST - Out of Shadow', 'https://www.youtube.com/watch?v=DCCHhDkFaEU'], ['Halo 3 OST - To Kill a Demon', 'https://www.youtube.com/watch?v=Alp6GCgk44g'], ['Halo 3 OST - This is Our Land', 'https://www.youtube.com/watch?v=vWUNMs6xMas'], ['Halo 3 OST - This is the Hour', 'https://www.youtube.com/watch?v=ZqTdByrdh5U'], ['Halo 3 OST - Dread Intrusion', 'https://www.youtube.com/watch?v=yhN5s1DFGv8'], ['Halo 3 OST - Follow Our Brothers', 'https://www.youtube.com/watch?v=a0FMIAdzx_k'], ['Halo 3 OST - Farthets Outpost', 'https://www.youtube.com/watch?v=_KeI0-0hbJI'], ['Halo 3 OST - Behold a Pale Horse', 'https://www.youtube.com/watch?v=zJUuMk18sqQ'], ['Halo 3 OST - Edge Closer', 'https://www.youtube.com/watch?v=4ZrFVkS-Ya4'], ['Halo 3 OST - Three Gates', 'https://www.youtube.com/watch?v=d0zr33BwWMg'], ['Halo 3 OST - Black Tower', 'https://www.youtube.com/watch?v=q_UZnGb7Cj8'], ['Halo 3 OST - One Final Effort', 'https://www.youtube.com/watch?v=5b8zZmSZC_0'], ['Halo 3 OST - Gravemind', 'https://www.youtube.com/watch?v=xGzXCw8THmQ'], ['Halo 3 OST - No More Dead Heroes', 'https://www.youtube.com/watch?v=OhkuYus2r8Y'], ['Halo 3 OST - Keep What You Steal', 'https://www.youtube.com/watch?v=KEKdHtn2YHI'], ['Halo 3 OST - Halo Reborn', 'https://www.youtube.com/watch?v=zGdCBe9rQRw'], ['Halo 3 OST - Greatest Journey', 'https://www.youtube.com/watch?v=4Q0Jbv6ciRU'], ['Halo 3 OST - Tribute', 'https://www.youtube.com/watch?v=kghQc3Mc7UY'], ['Halo 3 OST - Roll Call', 'https://www.youtube.com/watch?v=fCecybn2aZI'], ['Halo 3 OST - Wake Me When You Need Me', 'https://www.youtube.com/watch?v=1XbqrI4IaeU'], ['Halo 3 OST - Legend', 'https://www.youtube.com/watch?v=lofnJcJ7MeY'], ['Halo 3 OST - Choose Wisely', 'https://www.youtube.com/watch?v=I08lFVkCiMc'], ['Halo 3 OST - Movement', 'https://www.youtube.com/watch?v=RRgZ7cJ4Q-E'], ['Halo 3 OST - Never Forget', 'https://www.youtube.com/watch?v=OOHXjgEY_RQ'], ['Halo 3 OST - Finish the Fight', 'https://www.youtube.com/watch?v=voCyz6aSMXk'], ['Halo 3 OST - LvUrFR3NZ', 'https://www.youtube.com/watch?v=P4tEHl_P98E']],
	"3 ODST": [['Halo 3: ODST Original Soundtrack - Overture', 'https://www.youtube.com/watch?v=z1vdgfaZ5-I'], ['Halo 3: ODST Original Soundtrack - The Rookie', 'https://www.youtube.com/watch?v=0YwVVB00ftA'], ['Halo 3: ODST Original Soundtrack - More Than His Share', 'https://www.youtube.com/watch?v=aKCz9tDZes8'], ['Halo 3: ODST Original Soundtrack - Deference For Darkness', 'https://www.youtube.com/watch?v=7bYXcTWdgcY'], ['Halo 3: ODST Original Soundtrack - The Menagerie', 'https://www.youtube.com/watch?v=So1nJcCFWfw'], ['Halo 3: ODST Original Soundtrack - Asphalt And Ablution', 'https://www.youtube.com/watch?v=luzfzTy_bso'], ['Halo 3: ODST Original Soundtrack - Traffic Jam', 'https://www.youtube.com/watch?v=kOa9FXAKA2o'], ['Halo 3: ODST Original Soundtrack - Neon Night', 'https://www.youtube.com/watch?v=VoyyNpRC3Eg'], ['Halo 3: ODST Original Soundtrack - The Office Of Naval Intelligence', 'https://www.youtube.com/watch?v=060MgSFc6EY'], ['Halo 3: ODST Original Soundtrack - Bits And Pieces', 'https://www.youtube.com/watch?v=zxqtcEUlF4s'], ['Halo 3: ODST Original Soundtrack - Skyline', 'https://www.youtube.com/watch?v=IHxFTQYAqfc'], ['Halo 3: ODST Original Soundtrack - No Stone Unturned', 'https://www.youtube.com/watch?v=0ecHn3mIUhg'], ['Halo 3: ODST Original Soundtrack - One Way Ride', 'https://www.youtube.com/watch?v=R5QlD3IO8Ng'], ['Halo 3: ODST Original Soundtrack - The Light At The End', 'https://www.youtube.com/watch?v=lAhaxxEtUr8'], ['Halo 3: ODST Original Soundtrack - Data Hive', 'https://www.youtube.com/watch?v=IfazRui6mg4'], ['Halo 3: ODST Original Soundtrack - Special Delivery', 'https://www.youtube.com/watch?v=xPIBts5NT_0'], ['Halo 3: ODST Original Soundtrack - Finale', 'https://www.youtube.com/watch?v=8hlcNReP54Q']],
	"Reach": [['Halo Reach Soundtrack - 01: Overture', 'https://www.youtube.com/watch?v=JhnuAlQPX_U'], ['Halo Reach Soundtrack - 02: Winter Contingency', 'https://www.youtube.com/watch?v=a5XdecSPAIw'], ['Halo Reach Soundtrack - 03: ONI: Sword Base', 'https://www.youtube.com/watch?v=Pl0qJQ83wJo'], ['Halo Reach Soundtrack - 04: Nightfall', 'https://www.youtube.com/watch?v=quUiVVCAPHQ'], ['Halo Reach Soundtrack - 05: Tip of the Spear', 'https://www.youtube.com/watch?v=6koj_oA3vng'], ['Halo Reach Soundtrack - 06: Long Night of Solace', 'https://www.youtube.com/watch?v=g81Js5zZiUM'], ['Halo Reach Soundtrack - 07: Exodus', 'https://www.youtube.com/watch?v=2IdPqOF7Cck'], ['Halo Reach Soundtrack - 08: New Alexandria', 'https://www.youtube.com/watch?v=w0_wV_XTQNI'], ['Halo Reach Soundtrack - 09: The Package', 'https://www.youtube.com/watch?v=Z-1H0-PDj4I'], ['Halo Reach Soundtrack - 10: The Pillar of Autumn', 'https://www.youtube.com/watch?v=eTRtAB7spno'], ['Halo Reach Soundtrack - 11: Epilogue', 'https://www.youtube.com/watch?v=t_cF8UlwOZE'], ['Halo Reach Soundtrack - 12: From the Vault', 'https://www.youtube.com/watch?v=hBZywUpOixU'], ['Halo Reach Soundtrack - 13: Ashes', 'https://www.youtube.com/watch?v=ktce1qctRbM'], ['Halo Reach Soundtrack - 14: Fortress', 'https://www.youtube.com/watch?v=TgMMA7dYbf8'], ["Halo Reach Soundtrack - 15: We're Not Going Anywhere", 'https://www.youtube.com/watch?v=6Ei8UgoMdCQ'], ['Halo Reach Soundtrack - 16: At Any Cost', 'https://www.youtube.com/watch?v=arCBz5I9Vio'], ['Halo Reach Soundtrack - 17: Both Ways (Remix)', 'https://www.youtube.com/watch?v=9YSUXNi4K1A'], ['Halo Reach OST Disk 2 Track 11 Walking Away', 'https://www.youtube.com/watch?v=u4Y3C4Zds_U'], ['Halo Reach OST Disk 2 Track 12 Ghosts and Glass', 'https://www.youtube.com/watch?v=WDbDtCragPU'], ['Halo Reach OST Disk 2 Track 13 We Remember', 'https://www.youtube.com/watch?v=qaWqyUQZ2mw']],
	"4": [['Halo 4 OST - Awakening', 'https://www.youtube.com/watch?v=9Oj41t-UES0'], ['Halo 4 OST - Belly of the Beast', 'https://www.youtube.com/watch?v=vX5VI0GgO5U'], ['Halo 4 OST - Requiem', 'https://www.youtube.com/watch?v=kcuddfEvwtw'], ['Halo 4 OST - Legacy', 'https://www.youtube.com/watch?v=Zq5WfR4K3zA'], ['Halo 4 OST - Faithless', 'https://www.youtube.com/watch?v=zzyr_ZooBqo'], ['Halo 4 OST - Nemesis', 'https://www.youtube.com/watch?v=ctZhKWviOuc'], ['Halo 4 OST - Haven', 'https://www.youtube.com/watch?v=zYVGXMWkr7w'], ['Halo 4 OST - Ascendancy', 'https://www.youtube.com/watch?v=Hlxco4irGl8'], ['Halo 4 OST - Solace', 'https://www.youtube.com/watch?v=SKuJ2SLTYE4'], ['Halo 4 OST - To Galaxy', 'https://www.youtube.com/watch?v=x_oKF0uA7pk'], ['Halo 4 OST - Immaterial', 'https://www.youtube.com/watch?v=83MWUk_0sew'], ['Halo 4 OST - 117', 'https://www.youtube.com/watch?v=PUrsOQanozo'], ['Halo 4 OST - Arrival', 'https://www.youtube.com/watch?v=miwmCI7VS58'], ['Halo 4 OST - Revival', 'https://www.youtube.com/watch?v=Etksc3mrIQU'], ['Halo 4 OST - Green and Blue', 'https://www.youtube.com/watch?v=QBHxDMSlrdg'], ['Halo 4 Bonus Tracks - Desecration', 'https://www.youtube.com/watch?v=jUtkgmsVNr8'], ['Halo 4 Bonus Tracks - Never Forget', 'https://www.youtube.com/watch?v=yJVpF0b23O8'], ['Halo 4 [Original Soundtrack Vol. 2] - Atonement', 'https://www.youtube.com/watch?v=1wm8gk3Doj4'], ['Halo 4 [Original Soundtrack Vol. 2] - Gravity', 'https://www.youtube.com/watch?v=QxvGxLRPSp8'], ['Halo 4 [Original Soundtrack Vol. 2] - Wreckage', 'https://www.youtube.com/watch?v=oms7rs_Br-0'], ['Halo 4 [Original Soundtrack Vol. 2] - Aliens', 'https://www.youtube.com/watch?v=lTv0-jCjUIM'], ['Halo 4 [Original Soundtrack Vol. 2] - Kantele Bow', 'https://www.youtube.com/watch?v=bvXd6y1dVdI'], ['Halo 4 [Original Soundtrack Vol. 2] - Pylons', 'https://www.youtube.com/watch?v=06ZPHg-2CkI'], ['Halo 4 [Original Soundtrack Vol. 2] - Escape', 'https://www.youtube.com/watch?v=hkihFCrMiTA'], ['Halo 4 [Original Soundtrack Vol. 2] - Swamp', 'https://www.youtube.com/watch?v=kZk_ENO54i4'], ['Halo 4 [Original Soundtrack Vol. 2] - Push Trough', 'https://www.youtube.com/watch?v=rEOY1vZfhbI'], ['Halo 4 [Original Soundtrack Vol. 2] - Convoy', 'https://www.youtube.com/watch?v=G-OT_g0EWmk'], ['Halo 4 [Original Soundtrack Vol. 2] - To Galaxy (Extended Version)', 'https://www.youtube.com/watch?v=k4SaHWtWJyw'], ["Halo 4 [Original Soundtrack Vol. 2] - Lasky's Theme", 'https://www.youtube.com/watch?v=Q1HeWatTU6U'], ['Halo 4 [Original Soundtrack Vol. 2] - Foreshadow', 'https://www.youtube.com/watch?v=p7D5SAhevUo'], ['Halo 4 [Original Soundtrack Vol. 2] - Cloud City', 'https://www.youtube.com/watch?v=SVO4AmcRNWA'], ['Halo 4 [Original Soundtrack Vol. 2] - This Armour', 'https://www.youtube.com/watch?v=LYa9dBBMV0c'], ['Halo 4 [Original Soundtrack Vol. 2] - Intruders', 'https://www.youtube.com/watch?v=ycUGUHZv39g'], ['Halo 4 [Original Soundtrack Vol. 2] - Mantis', 'https://www.youtube.com/watch?v=m5lvDzALrso'], ['Halo 4 [Original Soundtrack Vol. 2] - Sacrifice', 'https://www.youtube.com/watch?v=qzgex4RCzb0'], ['Halo 4 [Original Soundtrack Vol. 2] - Never Forget (Midnight Version)', 'https://www.youtube.com/watch?v=qcRAnXVeFyc'], ['Halo 4 [Original Soundtrack Vol. 2] - Majestic', 'https://www.youtube.com/watch?v=hOzJ6e4vDZU']],
	"5": [['Halo 5 Guardians Original Soundtrack CD1 - 01 Halo Canticles', 'https://www.youtube.com/watch?v=LkTHGtRLj5s'], ['Halo 5 Guardians Original Soundtrack CD1 - 02 Light Is Green', 'https://www.youtube.com/watch?v=cIjFzQRvkKQ'], ['Halo 5 Guardians Original Soundtrack CD1 - 03 Kamchatka', 'https://www.youtube.com/watch?v=6HOTSDdMhfI'], ['Halo 5 Guardians Original Soundtrack CD1 - 04 Return To The Fold', 'https://www.youtube.com/watch?v=CRlyjmKs8sI'], ['Halo 5 Guardians Original Soundtrack CD1 - 05 Rock And Ice', 'https://www.youtube.com/watch?v=m452g13Pw-E'], ['Halo 5 Guardians Original Soundtrack CD1 - 06 Argent Moon', 'https://www.youtube.com/watch?v=nYMo_m7uiNo'], ['Halo 5 Guardians Original Soundtrack CD1 - 07 Scavengers', 'https://www.youtube.com/watch?v=S6A6DNIKYVA'], ['Halo 5 Guardians Original Soundtrack CD1 - 08 In Absentia', 'https://www.youtube.com/watch?v=9VOOkTMdSrM'], ['Halo 5 Guardians Original Soundtrack CD1 - 09 Meridian Crossing', 'https://www.youtube.com/watch?v=PpoDJqWQIY4'], ['Halo 5 Guardians Original Soundtrack CD1 - 10 Unearthed', 'https://www.youtube.com/watch?v=TQ0gt_SMsK0'], ['Halo 5 Guardians Original Soundtrack CD1 - 11 Unconfirmed Reports', 'https://www.youtube.com/watch?v=ToHQz8jRgpA'], ['Halo 5 Guardians Original Soundtrack CD1 - 12 Keeper of Secrets', 'https://www.youtube.com/watch?v=v0Xxub6D_Sk'], ['Halo 5 Guardians Original Soundtrack CD1 - 13 Cavalier', 'https://www.youtube.com/watch?v=zlUWnUzpzSA'], ['Halo 5 Guardians Original Soundtrack CD1 - 14 Crossed Paths', 'https://www.youtube.com/watch?v=ELyrPQd0XBQ'], ['Halo 5 Guardians Original Soundtrack CD1 - 15 Untethered', 'https://www.youtube.com/watch?v=fMwOxNp-q08'], ['Halo 5 Guardians Original Soundtrack CD1 - 16 Skeleton Crew', 'https://www.youtube.com/watch?v=oz3KatqLNzc'], ['Halo 5 Guardians Original Soundtrack CD1 - 17 Siren Song', 'https://www.youtube.com/watch?v=kuwHqhIU2Ws'], ['Halo 5 Guardians Original Soundtrack CD1 - 18 Enemy of my Enemy', 'https://www.youtube.com/watch?v=gjbr_L9NuNE'], ["Halo 5 Guardians Original Soundtrack CD1 - 19 Honor's Song", 'https://www.youtube.com/watch?v=Sv8bJ2ZtYJg'], ['Halo 5 Guardians Original Soundtrack CD1 -  20 Warrior World', 'https://www.youtube.com/watch?v=_t68xu3M_-s'], ['Halo 5 Guardians Original Soundtrack CD1 - 21 Covenant Prayers', 'https://www.youtube.com/watch?v=PzCWEn86VXY'], ['Halo 5 Guardians Original Soundtrack CD1 - 22 Cloud Chariot', 'https://www.youtube.com/watch?v=x9iCfrsKLMM'], ['Halo 5 Guardians Original Soundtrack CD1 - 23 Sentry Battle', 'https://www.youtube.com/watch?v=5_RjyjloHvA'], ['Halo 5 Guardians Original Soundtrack CD1 - 24 Worldquake', 'https://www.youtube.com/watch?v=UVwwM3GBH3w'], ['Halo 5 Guardians Original Soundtrack CD2 - 01 Advent', 'https://www.youtube.com/watch?v=5TmTWZrkr5Y'], ['Halo 5 Guardians Original Soundtrack CD2 - 02 Walk Softly', 'https://www.youtube.com/watch?v=5Wb77PPaGKY'], ['Halo 5 Guardians Original Soundtrack CD2 - 03 Genesis', 'https://www.youtube.com/watch?v=sPo-MipU8yY'], ['Halo 5 Guardians Original Soundtrack CD2 - 04 Dominion', 'https://www.youtube.com/watch?v=gBS327FzNIE'], ['Halo 5 Guardians Original Soundtrack CD2 - 05 The Trials', 'https://www.youtube.com/watch?v=hBwjlVNgHik'], ['Halo 5 Guardians Original Soundtrack CD2 - 06 Sentinel Song', 'https://www.youtube.com/watch?v=_gI18-YUjM0'], ['Halo 5 Guardians Original Soundtrack CD2 - 07 Crypt', 'https://www.youtube.com/watch?v=WZ5Ic4N-tEU'], ['Halo 5 Guardians Original Soundtrack CD2 - 08 End Game', 'https://www.youtube.com/watch?v=EbPxKqGU8PM'], ['Halo 5 Guardians Original Soundtrack CD2 - 09 Reunion', 'https://www.youtube.com/watch?v=OL4Tg-IC6po'], ['Halo 5 Guardians Original Soundtrack CD2 - 10 Blue Team', 'https://www.youtube.com/watch?v=bZaZqdmDRlI'], ['Halo 5 Guardians Original Soundtrack CD2  - 11 Jameson Locke', 'https://www.youtube.com/watch?v=meMgUSDslA4'], ['Halo 5 Guardians Original Soundtrack CD2 - 12 Osiris Suite, Act 1', 'https://www.youtube.com/watch?v=FIWJrnTHvrw'], ['Halo 5 Guardians Original Soundtrack CD2 - 13 Osiris Suite, Act 2', 'https://www.youtube.com/watch?v=GWSCJxr-FHM'], ['Halo 5 Guardians Original Soundtrack CD2 - 14 Osiris Suite, Act 3', 'https://www.youtube.com/watch?v=R7kDsuq0yng'], ['Halo 5 Guardians Original Soundtrack CD2 - 15 Osiris Suite, Act 4', 'https://www.youtube.com/watch?v=s26CwWhoyOE']],
	"Infinite": []
}
halo_icons = {
	"1": "https://orig00.deviantart.net/072c/f/2016/322/1/9/halo_combat_evolved___icon_by_blagoicons-daosyh9.png",
	"2": "https://orig00.deviantart.net/7d19/f/2011/160/e/9/halo_2_icon_01_by_kamizanon-d3igxxn.png",
	"3": "https://orig00.deviantart.net/b3d3/f/2012/051/1/d/halo_3__3__by_solobrus22-d4qdrie.png",
	"3 ODST": "https://orig00.deviantart.net/d149/f/2016/322/4/3/halo_3_odst___icon_by_blagoicons-daosyon.png",
	"Reach": "https://orig00.deviantart.net/950f/f/2016/322/2/4/halo_reach___icon_by_blagoicons-daosytj.png",
	"4": "https://orig00.deviantart.net/acf0/f/2016/322/6/e/halo_4___icon_by_blagoicons-daosywg.png",
	"5": "https://orig00.deviantart.net/a852/f/2016/322/b/d/halo_5_guardians___icon_by_blagoicons-daosyys.png",
	"Infinite": ""
}

opts = {
	'default-search': 'auto',
	'quiet': True,
}

halo_servers = {}
halo_servers_mark_to_delete = []

class halo_song(object):
	def __init__(self, game, track):
		self.game = game
		self.track = track

	def __str__(self):
		str = "[{}, {}] - {}".format(self.game, self.track, self.get_name())
		return str

	def get_url(self):
		return halo_songs[self.game][self.track][1]

	def get_name(self):
		return halo_songs[self.game][self.track][0]

class halo_server:
	def __init__(self, halo_voice_channel, halo_text_channel, halo_message, halo_song = halo_song("1", 0)):
		self.halo_voice_channel	= halo_voice_channel
		self.halo_text_channel 	= halo_text_channel
		self.halo_message 		= halo_message
		
		self.song = halo_song

		self.voice_client = None
		self.player = None

		self.play_next_song = asyncio.Event()
		self.audio_player = client.loop.create_task(self.audio_player_task())

	def __str__(self):
		str =  "halo_voice_channel: {}".format(self.halo_voice_channel)
		str += "\nhalo_text_channel: {}".format(self.halo_text_channel)
		str += "\nsong: {}".format(self.song)
		str += "\nvoice_client: {}".format(self.voice_client)
		str += "\nplayer: {}".format(self.player)
		str += "\nplay_next_song: {}".format(self.play_next_song)
		str += "\naudio_player: {}".format(self.audio_player)
		return str

	def __unload(self):
		try:
			self.audio_player.cancel()
			if state.voice:
				client.loop.create_task(voice_client.disconnect())
		except:
			pass

	def toggle_next(self):
		client.loop.call_soon_threadsafe(self.play_next_song.set)

	async def audio_player_task(self):
		while True:
			# print("audio_player_task() 1")
			self.play_next_song.clear()
			# print("audio_player_task() 2")
			await self.play_next_song.wait()
			# print("audio_player_task() 3")
			await self.next_song()
			# print("audio_player_task() 5")

	async def next_song(self):
		# print("next_song() start")
		current_game = self.song.game
		current_track = self.song.track
		# print("next_song() 1")

		try:
			# return halo_song(current_game, current_track + 1)
			if halo_songs[current_game][current_track + 1]:
				# print("next_song() 2a")
				self.song.track = self.song.track + 1
		except Exception as e:
			# print("next_song() 2b")
			# return halo_song(next_game[current_game], current_track)
			self.song = halo_song(next_game[current_game], 0)

		# print("next_song() 3")

		save_halo_servers()

		await self.play()
		# print("next_song() end")

	async def play(self):
		song = self.song.get_url()

		prettyPrint.print("Playing {}".format(self.song))
		self.player = await self.voice_client.create_ytdl_player(song, ytdl_options = opts, after = lambda: self.toggle_next())
		self.player.start()
		await self.send_song_to_channel()
		#await client.send_message(self.halo_text_channel, 'Now playing ' + str(self.song.get_name()))

	async def stop(self):
		if self.voice_client:
			self.player.stop()

		try:
			self.audio_player.cancel()
			await self.voice_client.disconnect()
		except:
			pass

	async def send_song_to_channel(self):
		# async for message in self.halo_text_channel.history(limit=5):
		# 	if message == self.halo_message:
		# 		await client.edit_message(self.halo_message, None, embed=gen_song_embed()) 
		# 	else:
		# 		await client.send_message(self.halo_message, None, embed=gen_song_embed()) 
		await client.send_message(self.halo_text_channel, None, embed=self.gen_song_embed()) 

	def gen_song_embed(self):
		embed = discord.Embed(
			title = "Currently Playing:",
			description = self.song.get_name(),
			color = 0x8ea72f,
		)
		embed.set_thumbnail(url=halo_icons[self.song.game])
		# embed.set_author(name=client.user.name,icon_url=client.user.avatar_url)
		embed.set_footer(text=client.user.name,icon_url=client.user.avatar_url)
		return embed

	def pickleify(self):
		return(halo_server_pickleable(self.halo_voice_channel, self.halo_text_channel, self.halo_message, self.song))

class halo_server_pickleable:
	def __init__(self, halo_voice_channel, halo_text_channel, halo_message, halo_song):
		self.halo_voice_channel	= halo_voice_channel
		self.halo_text_channel 	= halo_text_channel
		self.halo_message 	 	= halo_message
		self.song 				= halo_song

	def __str__(self):
		str =  "halo_voice_channel: {}".format(self.halo_voice_channel)
		str += "\nhalo_text_channel: {}".format(self.halo_text_channel)
		str += "\nhalo_message: {}".format(self.halo_message)
		str += "\nsong: {}".format(self.song)
		return str

	def unpickleify(self):
		return(halo_server(self.halo_voice_channel, self.halo_text_channel, self.halo_message, self.song))

class prettyPrint:
	indentLevel = 0
	multiplyer = 2
	is_new_line = True

	@staticmethod
	def indent(value = 1):
		prettyPrint.indentLevel = prettyPrint.indentLevel + 1 

	@staticmethod
	def unindent(value = 1):
		prettyPrint.indentLevel = prettyPrint.indentLevel - 1

	@staticmethod
	def print(input = "", new_lines = 0, end = "\n"):
		if prettyPrint.is_new_line:
			print(prettyPrint.get_indentation() + input + prettyPrint.get_lines(), end = end)
		else:
			print(input + prettyPrint.get_lines(), end = end)

		if end == "\n":
			prettyPrint.is_new_line = True
		else:
			prettyPrint.is_new_line = False

	@staticmethod
	def get_indentation(input = ""):
		output = ""

		for i in range(0, prettyPrint.indentLevel * prettyPrint.multiplyer):
			output += " "

		return output

	@staticmethod
	def get_lines(new_lines = 0):
		output = ""

		for i in range(0, new_lines):
			output += "\n"

		return output

def save_halo_servers():
	halo_servers_pickleable = {}
	prettyPrint.print("Saving...")

	prettyPrint.indent()
	for title, value in halo_servers.items():
		prettyPrint.print("{}...".format(title))
		halo_servers_pickleable[title] = value.pickleify()
		halo_server_saveable = halo_servers_pickleable[title]
	prettyPrint.unindent()

	with open('halo_servers.pkl', 'wb') as f:
		pickle.dump(halo_servers_pickleable, f)

	prettyPrint.print("Saved!")

def load_halo_servers():
	print("Loading...")

	try:
		with open('halo_servers.pkl', 'rb') as f:
			halo_servers_pickleable = pickle.load(f)
	except Exception as e:
		print("Error! Cannot find halo_servers.pkl")
		halo_servers_pickleable = {}

		print("Recreating halo_servers.pkl...")
		save_halo_servers()

	prettyPrint.indent()
	for title, value in halo_servers_pickleable.items():
		prettyPrint.print("{}".format(title))
		halo_servers[title] = value.unpickleify()
	prettyPrint.unindent()

	print("Loaded!")

def autocorrect_to_halo_song(requested_song_name):
	for halo_game, halo_game_songs in halo_songs.items():
		for song in range(len(halo_game_songs)):
			if halo_game_songs[song][0] == requested_song_name:
				return halo_song(halo_game, song - 1)

def add_embed_fields(embed, title, string_list):
	str = ""
	embed_count = 0

	for string in string_list:
		if len(str) + len(string) + len("\n") < 1024:
			str += string + "\n"
		else:
			embed_count = embed_count + 1
			if len(embed.fields) < 25:
				embed.add_field(name="Halo {} - Part {}".format(title, embed_count), value=str)
				str = string
			else:
				return

	embed_count = embed_count + 1
	embed.add_field(name="Halo {} - Part {}".format(title, embed_count), value=str, inline=False)

load_halo_servers()

@client.event
async def on_ready():
	print("{} started!".format(client.user.name))

	await client.change_presence(game=discord.Game(name="every Halo song! All day. Every day."))

	# halo_voice_channel = client.get_channel("350441096259829760")
	# halo_text_channel = client.get_channel("351468167928741888")
	# server_id = halo_text_channel.server.id
	# halo_servers[server_id] = halo_server(halo_voice_channel, halo_text_channel)
	print("{} Halo channels found!".format(len(halo_servers)))
	print("Connecting...")

	prettyPrint.indent()
	for server_id, hserver in halo_servers.items():
		prettyPrint.print("{}...".format(server_id), end=" ")

		try:
			voice_client = await client.join_voice_channel(hserver.halo_voice_channel)
		except Exception as e:
			prettyPrint.print("error")

			prettyPrint.indent()
			prettyPrint.print("Requesting user input...", end=" ")
			try:
				await client.send_message(hserver.halo_text_channel, "Cannot join the assigned Halo voice channel! Please use `halosetchannel` to reassign.")
			except Exception as e:
				prettyPrint.print("error")
				prettyPrint.print("Marking for deletion.")
				halo_servers_mark_to_delete.append(server_id)
			else:
				prettyPrint.print("success")
				prettyPrint.unindent()
		else:
			halo_servers[server_id].voice_client = voice_client
			prettyPrint.print("connected")

			prettyPrint.indent()
			await halo_servers[server_id].play()
			prettyPrint.unindent()

	if len(halo_servers_mark_to_delete) != 0:
		for server_id in halo_servers_mark_to_delete:
			del halo_servers[server_id]
			save_halo_servers()

	prettyPrint.unindent()
	prettyPrint.print("Connected!")

@client.command(pass_context = True)
async def set(ctx):
	requested_voice_channel = ctx.message.author.voice_channel # client.get_channel("350441096259829760")
	requested_text_channel = ctx.message.channel
	server = ctx.message.server
	server_id = server.id

	if requested_voice_channel is None:
		await self.bot.say('Please join a voice channel.')
		return

	try:
		hserver = halo_servers[server_id]
	except Exception as e:
		hserver = None


	if hserver == None:
		embed = discord.Embed(title = "Loading...")
		halo_message = await client.send_message(requested_text_channel, embed=embed)

		halo_servers[server_id] = halo_server(requested_voice_channel, requested_text_channel, halo_message)
		hserver = halo_servers[server_id]

		try:
			new_voice_client = await client.join_voice_channel(hserver.halo_voice_channel)
		except Exception as e:
			await client.send_message(hserver.halo_text_channel, "Cannot join your channel.")
			return
		else:
			hserver.halo_voice_channel = hserver.halo_voice_channel
			hserver.voice_client = new_voice_client
			await hserver.play()
	else:
		hserver = halo_servers[server_id]

		prettyPrint.indent()
		if requested_text_channel != hserver.halo_text_channel:
			prettyPrint.print("Server {} text changed: {} ->".format(server_id, hserver.halo_text_channel.id), end = " ")
			hserver.halo_text_channel = requested_text_channel
			prettyPrint.print(hserver.halo_text_channel.id)

		if requested_voice_channel != hserver.halo_voice_channel:
			prettyPrint.print("Server {} voice changed: {} ->".format(server_id, hserver.halo_voice_channel.id), end = " ")
			hserver.halo_voice_channel = requested_voice_channel

			await hserver.voice_client.move_to(requested_voice_channel)
			hserver.voice_client = server.voice_client
			prettyPrint.print(hserver.halo_voice_channel.id)
		prettyPrint.unindent()

		await client.send_message(hserver.halo_text_channel, "Halo channels updated!")

	save_halo_servers()

@client.command(pass_context = True)
async def remove(ctx):
	await halo_servers[ctx.message.server.id].stop()
	del halo_servers[ctx.message.server.id]

	save_halo_servers()

	await client.send_message(ctx.message.channel, "Channel assignment removed.")

@client.command(pass_context = True)
async def skip(ctx):
	hserver = halo_servers[ctx.message.server.id]
	hserver.player.stop()

@client.command(pass_context = True)
async def play(ctx, *, requested_song_name):
	server_id = ctx.message.server.id
	hserver = halo_servers[server_id]

	if hserver == None:
		await client.send_message(hserver.halo_text_channel, "Please use `halosetchannel` to set up your audio channel before using play.")
		return

	halo_song = autocorrect_to_halo_song(requested_song_name)

	if halo_song == None:
		await client.send_message(hserver.halo_text_channel, "Cannot find song: `{}`".format(requested_song_name))
		return

	hserver.song = halo_song
	hserver.player.stop()

@client.command(pass_context = True)
async def songs(ctx, requested_game):
	embed = discord.Embed(
		title = "List of Halo songs",
		thumbnail = client.user.avatar_url,
		color = 0x8ea72f,
		footer = client.user.name
	)

	try:
		song_list = halo_songs[requested_game]
	except Exception as e:
		await client.send_message(ctx.message.channel, "Cannot find game: `{}`. Please use one of the following:\n`1`\n`2`\n`3`\n`\"3 ODST\"`\n`Reach`\n`4`\n`5`".format(requested_game))
		return

	str_list = []
	for song in song_list:
		str_list.append(song[0])

	add_embed_fields(embed, requested_game, str_list)

	print(embed.to_dict())
	await client.send_message(ctx.message.channel, embed=embed)

client.run("your bot id idk")