# 🎧 Sesli Asistan Uygulaması

Bu proje, **Gradio** arayüzü üzerinden çalışan bir **Text-to-Speech (TTS)**, **Speech-to-Text (STT)** ve **telaffuz doğruluğu test** uygulamasıdır.  
Whisper, pyttsx3, gTTS, pydub, Levenshtein ve pandas kütüphanelerini bir arada kullanır.  
Ayrıca, İngilizce CEFR seviye kelimelerini içeren bir CSV dosyası ile rastgele kelime seçme ve telaffuz testi özelliği de vardır.

---

## 🔧 Kurulum

Projeyi çalıştırmadan önce bir sanal ortam (virtual environment) oluşturmanız tavsiye edilir.

```bash
# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin (Windows)
venv\Scripts\activate

# veya (Mac/Linux)
source venv/bin/activate

#Gerekli bağımlılıkları yükleyin:
pip install -r requirements.txt

#Uygualamayı başlatın:
python app.py



---



