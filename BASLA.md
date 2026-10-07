# Minik Orman Dostları — ilk bulut denemesi

Bu paket kısa teknik pilot üretir. 20 dakikalık tam bölüm, haftalık takvim ve YouTube yükleme henüz uygulanmadı. Çizimler özgün, ses eSpeak NG Türkçe sentezidir; ses robotik olabilir. Bu örnek yayın kalitesini değil ücretsiz bulut üretimini test eder.

## Kurulum
1. GitHub hesabında yeni **Public** depo aç: `minik-orman-dostlari`.
2. ZIP'i bilgisayarında çıkar. `render.py` ve `BASLA.md` dosyalarını depoya yükle.
3. GitHub'da Add file > Create new file seç. Dosya adına `.github/workflows/pilot.yml` yaz. Paketteki aynı dosyanın içeriğini yapıştır ve kaydet. Windows'ta gizli klasörün atlanmaması için bu yöntem önerilir.
4. Actions > Minik Orman Pilot > Run workflow seç.
5. Tamamlanan çalışmada Artifacts altındaki `minik-orman-pilot` dosyasını indir, ZIP içindeki videoyu izle.

Görev başladıktan sonra bilgisayarın açık kalması gerekmez. Public depoda standart GitHub runner kullanılır. Hiçbir anahtar, token veya şifreyi dosyalara koyma. Şimdilik secret veya YouTube bağlantısı gerekmiyor. Videoda müzik yoktur. Görev yalnızca elle başlatılır; otomatik yayın yapmaz.

## Kontrol
Görüntüde tavşan, kırmızı top ve sarı çiçek görünmeli. Türkçe ses duyulmalı. Bu denemede dudak senkronu yoktur. Yerel sessiz test: `python render.py --silent-test` (Pillow ve FFmpeg gerekir).

## 20 dakika hedefi
0–1 dk: Karakterler ve renkleri keşfetme hedefi.
1–5 dk: Kırmızı topu arama; kırmızı nesneleri tanıma.
5–9 dk: Sarı çiçekler ve mavi dere; renkleri karşılaştırma.
9–13 dk: Hikâyeye bağlı üç renk eşleştirme etkinliği; kısa cevap süreleri.
13–18 dk: Arkadaşlarla renkli uçurtma yapma ve paylaşma.
18–20 dk: Hikâyenin çözümü, renkleri hatırlama ve kapanış.

Tam bölüm için özgün senaryo, farklı sahneler, tutarlı karakter varlıkları ve daha doğal ücretsiz ses seçimi gerekir. Süre doldurmak için pilot döngüye alınmayacak veya konuşma yavaşlatılmayacak. Önce pilot ses ve görsel onayı, sonra tam bölüm üretimi. Son aşamada çocuklara özel işaretleme, ayrı kanal OAuth bağlantısı, kalıcı bölüm kaydı ve yükleme hata yönetimi hazırlanacak.

## Kaynaklar
https://docs.github.com/en/actions/concepts/billing-and-usage
https://github.com/espeak-ng/espeak-ng
https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md
