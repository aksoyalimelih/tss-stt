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
