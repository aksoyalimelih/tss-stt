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

### 📄 **README (English)**

```markdown
# 🎧 Voice Assistant Application

This project is a **Text-to-Speech (TTS)**, **Speech-to-Text (STT)** and **pronunciation accuracy test** application running on a **Gradio** interface.  
It integrates libraries like Whisper, pyttsx3, gTTS, pydub, Levenshtein, and pandas.  
Additionally, it uses an English CEFR-level word CSV file to randomly pick words and test user pronunciation.

---

## 🔧 Setup

Before running the project, it is recommended to create a virtual environment.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# or (Mac/Linux)
source venv/bin/activate

#Install the required dependencies:

bash
pip install -r requirements.txt

#Running
To start the project:

bash
python app.py

