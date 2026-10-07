"""Üç Minik Bir Macera: EMA anlatıcılı, üç sahneli 720p pilot."""
from pathlib import Path
import argparse, math, subprocess, wave
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
p=argparse.ArgumentParser(); p.add_argument('--silent-test', action='store_true'); a=p.parse_args()
SCENES=[
 ('Üç Minik Bir Macera', 'Merhaba minik dostlar! Bugün Mino, Tosi ve Piko ile ormanda güzel bir maceraya çıkıyoruz. Mino tavşandır. Tosi bir kaplumbağa, Piko ise küçük bir kuştur. Üç arkadaş birlikte oynamayı çok sever.'),
 ('Kırmızı top nerede?', 'Mino kırmızı topunu arıyordu. Tosi, ağacın yanına bakalım, dedi. Piko da arkadaşlarına katıldı. Bakın, sarı bir çiçek var! Çiçek sarı, ama aradığımız top kırmızı. Ağacın yanında ne görüyorsunuz? Evet, kırmızı top!'),
 ('Birlikte oynamak güzel!', 'Mino topunu bulunca çok sevindi. Teşekkür ederim arkadaşlarım, dedi. Üç arkadaş topu sırayla birbirlerine yuvarladılar. Piko, birlikte oynamak ne güzel, dedi. Yardımlaşınca aradıklarını bulmuş, paylaşınca oyunları daha da eğlenceli olmuştu.')
]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',40)
if not a.silent_test:
 from ema_lightning import EMA
 tts=EMA()

# Consistent original geometric puppets. Not the detailed avatar illustrations.
def character(kind, t, talking):
 im=Image.new('RGBA',(300,350)); d=ImageDraw.Draw(im)
 ink='#5b4940'; cream='#fff4df'; green='#9bcf66'; yellow='#ffd55c'
 def oval(box,fill): d.ellipse(box,fill=fill,outline=ink,width=5)
 if kind=='mino':
  oval((78,8,124,142),cream); oval((169,8,215,142),cream)
  d.ellipse((91,29,112,119),fill='#f6b7bd'); d.ellipse((182,29,203,119),fill='#f6b7bd')
  oval((66,198,232,320),cream); oval((52,108,246,250),cream)
  oval((46,295,136,339),cream); oval((163,295,253,339),cream)
  d.ellipse((138,190,160,205),fill='#ef9faa'); eyes_y=166
 elif kind=='tosi':
  oval((20,160,268,304),'#6fba75')
  for box in [(55,191,121,247),(126,185,193,245),(99,244,168,292)]: oval(box,'#87cc88')
  oval((45,276,120,333),green); oval((183,276,267,333),green)
  oval((132,97,292,236),green); eyes_y=149
 else:
  oval((55,93,245,310),yellow); oval((25,185,97,276),yellow); oval((205,185,277,276),yellow)
  d.polygon([(136,182),(164,182),(151,205)],fill='#f3a445',outline=ink)
  d.line((115,303,110,332),fill='#f3a445',width=8); d.line((184,303,188,332),fill='#f3a445',width=8)
  eyes_y=154
 xs=(112,187) if kind!='tosi' else (188,251)
 for x in xs:
  if int(t*20)%89<3: d.line((x-11,eyes_y,x+11,eyes_y),fill=ink,width=5)
  else:
   oval((x-15,eyes_y-23,x+15,eyes_y+18),'white')
   d.ellipse((x-7,eyes_y-10,x+9,eyes_y+12),fill=ink)
   d.ellipse((x-4,eyes_y-9,x+2,eyes_y-3),fill='white')
 if kind!='piko':
  mx=151 if kind=='mino' else 222
  if talking and int(t*8)%2==0: oval((mx-12,eyes_y+52,mx+12,eyes_y+70),'#b96464')
  else: d.arc((mx-19,eyes_y+27,mx+19,eyes_y+62),0,180,fill=ink,width=4)
 return im

def frame(scene,t,duration):
 im=Image.new('RGB',(1280,720),'#b9e9f7'); d=ImageDraw.Draw(im)
 d.ellipse((940,40,1060,160),fill='#ffdc72')
 for x,y in [(110,90),(420,60)]:
  d.ellipse((x,y,x+150,y+55),fill='#f4fcff'); d.ellipse((x+35,y-25,x+115,y+55),fill='#f4fcff')
 d.ellipse((-250,380,820,950),fill='#b3de93'); d.ellipse((650,375,1520,940),fill='#a1d17f')
 d.rectangle((1010,240,1060,550),fill='#b88b65'); d.ellipse((905,105,1170,345),fill='#6bbc80')
 # Three different staging layouts; the ball is discovered in scene two.
 poses=[[(190,310),(510,355),(820,325)],[(70,330),(390,355),(715,315)],[(130,330),(500,355),(870,325)]][scene]
 for i,kind in enumerate(['mino','tosi','piko']):
  x,y=poses[i]; y+=int(math.sin(t*2.5+i)*4)
  im.paste(character(kind,t,scene==i), (x,y),character(kind,t,scene==i))
 d=ImageDraw.Draw(im)
 if scene==1:
  x=1085; y=555
 elif scene==2:
  x=int(360+470*(.5+.5*math.sin(t*.85))); y=620
 else: x=1100; y=570
 d.ellipse((x-31,y-31,x+31,y+31),fill='#f06d72',outline='#b94e58',width=4)
 for fx in [70,1160]:
  d.line((fx,570,fx,625),fill='#558e50',width=6)
  for ang in range(0,360,72):
   dx=math.cos(math.radians(ang))*15; dy=math.sin(math.radians(ang))*15
   d.ellipse((fx+dx-12,555+dy-12,fx+dx+12,555+dy+12),fill='#ffd765')
  d.ellipse((fx-8,547,fx+8,563),fill='#e6a14f')
 d.rounded_rectangle((32,25,850,98),radius=24,fill='#ffffff')
 d.text((53,37),SCENES[scene][0],font=font,fill='#3f5964')
 return im

parts=[]
for i,(title,text) in enumerate(SCENES):
 wav=OUT/f'voice-{i}.wav'
 if a.silent_test: duration=2
 else:
  tts.say(text,speed=1.0,seed=0,path=str(wav))
  with wave.open(str(wav)) as w: duration=w.getnframes()/w.getframerate()+.6
 fps=24; count=math.ceil(duration*fps); dest=OUT/f'scene-{i}.mp4'
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','-']
 if not a.silent_test: cmd+=['-i',str(wav)]
 cmd+=['-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p']
 if not a.silent_test: cmd+=['-c:a','aac','-af','apad','-t',str(count/fps)]
 cmd+=[str(dest)]; proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for n in range(count): proc.stdin.write(frame(i,n/fps,duration).tobytes())
 finally: proc.stdin.close()
 if proc.wait()!=0: raise RuntimeError(f'Sahne {i} üretilemedi')
 parts.append(dest)
 print(f'Sahne {i+1}: {count/fps:.2f} saniye',flush=True)
listing=OUT/'concat.txt'; listing.write_text('\n'.join("file '"+x.name+"'" for x in parts),encoding='utf-8')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/'pilot.mp4')],check=True)
frame(2,1,2).save(OUT/'preview.jpg')
print('Tamamlandı: output/pilot.mp4',flush=True)
