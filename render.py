"""Bulut üretim denemesi; yayınlanacak tam bölüm değildir."""
import math, subprocess, wave, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
p=argparse.ArgumentParser(); p.add_argument('--silent-test',action='store_true'); args=p.parse_args()
text='Merhaba! Ben Mino. Bugün ormanda kırmızı topumu arıyorum. İşte sarı bir çiçek. Çok güzel, ama topum sarı değil. Bakın! Ağacın yanında kırmızı bir top var. Topumu buldum! Şimdi arkadaşlarımla birlikte oynayabilirim.'
if args.silent_test:
    duration=4
else:
    (OUT/'narration.txt').write_text(text,encoding='utf-8')
    subprocess.run(['espeak-ng','-v','tr','-s','135','-f',str(OUT/'narration.txt'),'-w',str(OUT/'voice.wav')],check=True)
    with wave.open(str(OUT/'voice.wav')) as w: duration=w.getnframes()/w.getframerate()+1
fps=20; total=math.ceil(duration*fps)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(font_path,26)
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','640x360','-r',str(fps),'-i','-']
if not args.silent_test: cmd+=['-i',str(OUT/'voice.wav')]
cmd+=['-c:v','libx264','-preset','fast','-pix_fmt','yuv420p']
if not args.silent_test: cmd+=['-c:a','aac','-af','apad','-t',str(total/fps)]
cmd+=[str(OUT/'pilot.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
    for n in range(total):
        t=n/fps; phase=n/total
        im=Image.new('RGB',(640,360),'#bdeaff'); d=ImageDraw.Draw(im)
        d.ellipse((480,20,540,80),fill='#ffd45b'); d.rectangle((0,255,640,360),fill='#9ed976')
        d.rectangle((485,140,512,270),fill='#a46b43'); d.ellipse((425,60,565,190),fill='#4baf62')
        x=int(100+min(phase*2,1)*280); y=224+int(4*math.sin(t*5))
        d.ellipse((x-30,y-4,x+30,y+66),fill='#faf5ef',outline='#79665b',width=2)
        d.ellipse((x-20,y-77,x-4,y-22),fill='#faf5ef',outline='#79665b',width=2)
        d.ellipse((x+4,y-77,x+20,y-22),fill='#faf5ef',outline='#79665b',width=2)
        d.ellipse((x-30,y-37,x+30,y+18),fill='#faf5ef',outline='#79665b',width=2)
        for ex in (x-11,x+11):
            if n%85<3: d.line((ex-3,y-13,ex+3,y-13),fill='#3b3331',width=2)
            else: d.ellipse((ex-3,y-16,ex+3,y-10),fill='#3b3331')
        d.ellipse((x-4,y-5,x+4,y+1),fill='#eaa4a4')
        d.ellipse((440,265,480,305),fill='#ef5656',outline='#b73333',width=2)
        d.line((205,280,205,310),fill='#478b42',width=4); d.ellipse((192,264,218,290),fill='#ffdc55')
        title='Mino ve Kırmızı Top' if phase<.8 else 'Birlikte oynamak ne güzel!'
        d.text((25,20),title,font=font,fill='#29475b')
        proc.stdin.write(im.tobytes())
finally:
    proc.stdin.close()
if proc.wait()!=0: raise RuntimeError('Video üretilemedi')
print(f'Üretildi: {OUT / "pilot.mp4"} ({total/fps:.1f} saniye)')
