"""Profil karakterleriyle EMA sesli kısa pilot; 20 dakikalık bölüm değildir."""
from pathlib import Path
import argparse, math, subprocess, wave
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent; O=R/'output'; O.mkdir(exist_ok=True)
p=argparse.ArgumentParser(); p.add_argument('--silent-test',action='store_true'); a=p.parse_args()
scenes=[('Üç Minik Bir Macera','Merhaba minik dostlar! Mino, Tosi ve Piko bugün ormanda buluştular. Mino kırmızı topuyla oynamak istiyordu. Ama topunu bıraktığı yerde bulamadı. Arkadaşları ona yardım etmeye karar verdiler.'),('Kırmızı top nerede?','Üç arkadaş çiçeklerin yanına baktılar. Sarı çiçeklerin arasında top yoktu. Piko ağacın yanına doğru uçtu. Bakın, dedi, kırmızı top ağacın yanında! Mino arkadaşlarına teşekkür etti.'),('Birlikte oynamak güzel!','Topunu bulan Mino arkadaşlarını oyuna çağırdı. Önce topu Tosiye yuvarladı. Tosi de Pikoya gönderdi. Üç arkadaş sırayla oynadılar. Yardımlaşınca topu bulmuş, paylaşınca daha çok eğlenmişlerdi.')]
sheet=Image.open(R/'assets/characters.png').convert('RGBA'); sprites=[]
for left,right,h in [(0,700,390),(700,1245,310),(1245,sheet.width,285)]:
 s=sheet.crop((left,0,right,sheet.height)); b=s.getchannel('A').getbbox()
 if not b: raise ValueError('Boş karakter')
 s=s.crop(b); s.thumbnail((390,h),Image.Resampling.LANCZOS); sprites.append(s)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',38)

def draw(i,t):
 im=Image.new('RGB',(1280,720),['#bceaf8','#c9edf3','#fce9bc'][i]); d=ImageDraw.Draw(im)
 d.ellipse((1020,35,1130,145),fill='#ffda72')
 d.ellipse((-300,390,950,1050),fill='#abd38b'); d.ellipse((650,380,1540,1050),fill='#98c77c')
 for x in ([970] if i==0 else [40,1010] if i==1 else [1090]):
  d.rectangle((x,245,x+45,570),fill='#b48864'); d.ellipse((x-100,120,x+145,360),fill='#6cb77c')
 if i==1:
  for x in [70,160,230,1110,1180]:
   d.line((x,610,x,665),fill='#548c4d',width=6); d.ellipse((x-16,590,x+16,622),fill='#ffdc65')
 poses=[[160,510,850],[80,440,750],[150,500,880]][i]
 for j,s in enumerate(sprites):
  x=poses[j]; y=675-s.height+int(4*math.sin(t*2+j))
  if i==1 and j==2: x+=int(55*math.sin(t*.45)); y-=int(20+12*math.sin(t*2))
  im.paste(s,(x,y),s)
 d=ImageDraw.Draw(im)
 bx=1100 if i<2 else int(420+400*(.5+.5*math.sin(t*.8)))
 d.ellipse((bx-28,602,bx+28,658),fill='#ed6871',outline='#b74b54',width=4)
 d.rounded_rectangle((30,25,850,98),radius=22,fill='white'); d.text((52,39),scenes[i][0],font=font,fill='#415d66')
 return im
if not a.silent_test:
 from ema_lightning import EMA
 tts=EMA()
parts=[]
for i,(title,text) in enumerate(scenes):
 wav=O/f'voice-{i}.wav'
 if a.silent_test: dur=2
 else:
  tts.say(text,speed=1.0,seed=0,path=str(wav))
  with wave.open(str(wav)) as w: dur=w.getnframes()/w.getframerate()+.5
 fps=24; nframes=math.ceil(dur*fps); dest=O/f'scene-{i}.mp4'
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','-']
 if not a.silent_test: cmd+=['-i',str(wav)]
 cmd+=['-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p']
 if not a.silent_test: cmd+=['-c:a','aac','-af','apad','-t',str(nframes/fps)]
 cmd+=[str(dest)]; proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for n in range(nframes): proc.stdin.write(draw(i,n/fps).tobytes())
 finally: proc.stdin.close()
 if proc.wait()!=0: raise RuntimeError('Sahne üretilemedi')
 parts.append(dest); print(f'Sahne {i+1} hazır',flush=True)
listing=O/'concat.txt'; listing.write_text('\n'.join("file '"+f.name+"'" for f in parts))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(O/'pilot.mp4')],check=True)
draw(2,1).save(O/'preview.jpg')
print('output/pilot.mp4 hazır')
