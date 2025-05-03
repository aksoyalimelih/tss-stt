import gradio as gr
import whisper
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
import os
import uuid
import tempfile
import time
import pandas as pd
import random
import Levenshtein  # Telaffuz doğruluğu için benzerlik hesaplamak

# Whisper modeli yükleniyor (STT için)
model = whisper.load_model("base")

# pyttsx3 motoru başlatılıyor (offline TTS için)
engine = pyttsx3.init()

# pyttsx3 motoru üzerinde ses seçimi
voices = engine.getProperty('voices')

# CSV'den kelimeleri oku
df = pd.read_csv("yeni_english_cefr_words.csv")  # Burada csv dosyanın ismi doğru olmalı!

# 🔊 Speech to Text (Ses -> Metin) fonksiyonu
def transcribe(audio_path):
    if audio_path is None:
        return "Lütfen bir ses dosyası yükleyin."
    
    result = model.transcribe(audio_path)
    detected_language = result["language"]
    print(f"Tespit Edilen Dil: {detected_language}")

    return result["text"]

# 🗣️ Text to Speech (Metin -> Ses) fonksiyonu
def synthesize(text, tts_engine, language):
    if not text:
        return None

    output_path = f"tts_output_{uuid.uuid4().hex}.mp3"

    if language == "Türkçe":
        if tts_engine == "gTTS (Online)":
            tts = gTTS(text=text, lang="tr")
            tts.save(output_path)
        elif tts_engine == "pyttsx3 (Offline)":
            engine.setProperty('voice', voices[0].id)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_path = temp_file.name
                engine.save_to_file(text, temp_path)
                engine.runAndWait()
                try:
                    sound = AudioSegment.from_wav(temp_path)
                    sound.export(output_path, format="mp3")
                except Exception as e:
                    return f"Ses dosyası dönüştürülürken hata: {str(e)}"
                finally:
                    time.sleep(1)
                    try:
                        os.remove(temp_path)
                    except PermissionError:
                        pass
    elif language == "İngilizce":
        if tts_engine == "gTTS (Online)":
            tts = gTTS(text=text, lang="en")
            tts.save(output_path)
        elif tts_engine == "pyttsx3 (Offline)":
            engine.setProperty('voice', voices[1].id)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_path = temp_file.name
                engine.save_to_file(text, temp_path)
                engine.runAndWait()
                try:
                    sound = AudioSegment.from_wav(temp_path)
                    sound.export(output_path, format="mp3")
                except Exception as e:
                    return f"Ses dosyası dönüştürülürken hata: {str(e)}"
                finally:
                    time.sleep(1)
                    try:
                        os.remove(temp_path)
                    except PermissionError:
                        pass

    return output_path

# Telaffuz doğruluğu kontrol fonksiyonu
def check_pronunciation(original_audio, user_audio):
    original_transcription = transcribe(original_audio)
    user_transcription = transcribe(user_audio)

    similarity = Levenshtein.ratio(original_transcription.lower(), user_transcription.lower()) * 100

    if similarity < 50:
        message = "Hmm... Telaffuzun biraz karışık. Endişelenme, gelişeceksin! 💪"
    elif similarity < 70:
        message = "İdare eder! Biraz daha çalışalım. 😎"
    elif similarity < 90:
        message = "Çok iyi! Ufak tefek hatalar var sadece. 🌟"
    elif similarity < 100:
        message = "Vay canına! Harika bir telaffuz. 👏"
    else:
        message = "Mükemmel! 🎉"

    return f"{message} \n\nBenzerlik: {similarity:.2f}%"

# 📚 CSV'den Kelime Seçme Fonksiyonu
def get_random_word(level=None):
    if level:
        filtered_df = df[df['seviye'] == level]
    else:
        filtered_df = df
    if filtered_df.empty:
        return None
    return random.choice(filtered_df['kelimeler'].tolist())

# 🔊 Kelimenin Doğru Telaffuzunu Üretme
def generate_word_audio(word):
    tts = gTTS(text=word, lang="en")
    output_path = f"word_audio_{uuid.uuid4().hex}.mp3"
    tts.save(output_path)
    return output_path

# 🧠 Kelime Telaffuz Test Fonksiyonu
def pronunciation_test(word, user_audio):
    user_text = transcribe(user_audio)
    similarity = Levenshtein.ratio(word.lower(), user_text.lower()) * 100

    if similarity < 50:
        message = "Hmm... Telaffuzun biraz zor anlaşılıyor. Denemeye devam! 💪"
    elif similarity < 70:
        message = "Fena değil, birkaç küçük hata var! Biraz daha çalışalım. 🔥"
    elif similarity < 90:
        message = "Çok iyi! Küçük hatalar dışında neredeyse mükemmel. 🌟"
    elif similarity < 100:
        message = "Vay! Neredeyse mükemmelsin. 👏"
    else:
        message = "Harika! Mükemmel telaffuz! 🎯"

    return f"Beklenen Kelime: '{word}' \n\nTespit Edilen: '{user_text}' \n\n{message} \n\nBenzerlik: {similarity:.2f}%"


# Kelime Listesi ve Seçim
def get_word_list(level=None):
    if level:
        filtered_df = df[df['seviye'] == level]
    else:
        filtered_df = df
    word_list = filtered_df[['kelimeler', 'seviye']].values.tolist()
    return [f"{word[0]} ({word[1]})" for word in word_list]

# Gradio Arayüzü
with gr.Blocks(title="Sesli Asistan Uygulaması") as demo:
    gr.Markdown("## 🎙️ Text-to-Speech ve Speech-to-Text Uygulaması")

    with gr.Tabs():
        # Ses'ten Metine
        with gr.Tab("Ses'ten Metine"):
            with gr.Row():
                audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath", label="🎤 Ses Yükle (STT)")
            transcribe_btn = gr.Button("🧠 Ses -> Metin")
            transcription_output = gr.Textbox(label="📄 Dönüştürülen Metin")
            transcribe_btn.click(transcribe, inputs=audio_input, outputs=transcription_output)

        # Metinden Sese
        with gr.Tab("Metinden Sese"):
            with gr.Row():
                text_input = gr.Textbox(label="📝 Metin Girin (TTS)")
                language_choice = gr.Radio(
                    choices=["Türkçe", "İngilizce"],
                    value="İngilizce",
                    label="🎤 Ses Asistani Seçin"
                )
                tts_engine_choice = gr.Radio(
                    choices=["gTTS (Online)", "pyttsx3 (Offline)"],
                    value="gTTS (Online)",
                    label="🔧 TTS Motoru Seç"
                )
            synthesize_btn = gr.Button("🎧 Metin -> Ses")
            audio_output = gr.Audio(label="🔊 Oluşturulan Ses", type="filepath")
            synthesize_btn.click(synthesize, inputs=[text_input, tts_engine_choice, language_choice], outputs=audio_output)

        # Telaffuz Doğruluğu
        with gr.Tab("Telaffuz Doğruluğu"):
            with gr.Row():
                original_audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath", label="🎤 Ses Yükle (STT) ve Telaffuz Kontrolü")
                user_audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath", label="🎤 Telaffuz Testi için Ses Kaydı Yapın")
            pronunciation_check_btn = gr.Button("🔍 Telaffuz Doğruluğunu Kontrol Et")
            pronunciation_output = gr.Textbox(label="📊 Telaffuz Doğruluğu")
            pronunciation_check_btn.click(check_pronunciation, inputs=[original_audio_input, user_audio_input], outputs=pronunciation_output)

        # 📚 Kelime Telaffuz Testi
        with gr.Tab("Kelime Telaffuz Testi"):
            with gr.Row():
                level_choice = gr.Dropdown(
                    choices=["A1", "A2", "B1", "B2", "C1", "C2"],
                    label="Seviye Seçin (İsterseniz)",
                    interactive=True
                )
                new_word_btn = gr.Button("🎯 Kelime Seç")
                word_list = gr.Dropdown(label="Kelime Listesi", choices=get_word_list())
            selected_word = gr.Textbox(label="Seçilen Kelime", interactive=False)
            word_audio_output = gr.Audio(label="🔊 Doğru Telaffuzu Dinle", type="filepath")

            with gr.Row():
                user_audio_input_word = gr.Audio(sources=["upload", "microphone"], type="filepath", label="🎤 Telaffuzunuzu Kaydedin")
            check_btn_word = gr.Button("🔍 Telaffuzu Kontrol Et")
            check_output_word = gr.Textbox(label="📊 Sonuç")

            # Butonlara fonksiyon bağlama
            new_word_btn.click(
                lambda level: (word := get_random_word(level), generate_word_audio(word))[0:2],
                inputs=[level_choice],
                outputs=[selected_word, word_audio_output]
            )
            check_btn_word.click(pronunciation_test, inputs=[selected_word, user_audio_input_word], outputs=check_output_word)

            # Kelime listesi üzerinden seçim yapılabilir
            word_list.change(
                lambda word: (word.split(" (")[0], generate_word_audio(word.split(" (")[0])),
                inputs=[word_list],
                outputs=[selected_word, word_audio_output]
            )

# Uygulama başlatılıyor
if __name__ == "__main__":
    demo.launch()
