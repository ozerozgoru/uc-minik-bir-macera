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

BACKGROUND=Image.open(R/'assets/forest.png').convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)

def draw(i,t):
 im=BACKGROUND.copy(); d=ImageDraw.Draw(im)
 poses=[[160,510,850],[80,440,750],[150,500,880]][i]
 for j,sprite in enumerate(sprites):
  x=poses[j]; y=650-sprite.height+int(3*math.sin(t*2+j))
  if i==1:
   x+=int(min(t/7,1)*90)
   if j==2: y-=int(30+12*math.sin(t*2))
  if i==2: x+=int(10*math.sin(t*.8+j))
  # Small ground shadow supports visual contact with the illustrated ground.
  d.ellipse((x+sprite.width*.2,642,x+sprite.width*.8,656),fill='#65844b')
  im.paste(sprite,(x,y),sprite)
 bx=1100 if i<2 else int(420+400*(.5+.5*math.sin(t*.8)))
 d=ImageDraw.Draw(im)
 d.ellipse((bx-28,602,bx+28,658),fill='#ed6871',outline='#b74b54',width=4)
 d.arc((bx-23,607,bx+23,653),200,285,fill='#ffb5b7',width=5)
 # Alternating wide and medium views every five seconds. Ease camera position.
 shot=int(t/5)%3
 if shot:
  width=950 if shot==1 else 1050; height=int(width*720/1280)
  cx=(400 if i==0 else 950 if i==1 else 700)+12*math.sin(t*.3)
  left=max(0,min(1280-width,int(cx-width/2)))
  top=min(720-height,max(0,int(450-height/2)))
  im=im.crop((left,top,left+width,top+height)).resize((1280,720),Image.Resampling.BICUBIC)
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((30,25,850,98),radius=22,fill='#fff9eb')
 d.text((52,39),scenes[i][0],font=font,fill='#415d66')
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
