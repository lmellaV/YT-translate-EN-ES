# 🎬 YouTube Transcript Translator (EN → ES)

Este proyecto permite **descargar, limpiar y traducir automáticamente** las transcripciones de videos de YouTube desde inglés a español utilizando **Python** y modelos de traducción de **Hugging Face**.

---

## 🚀 Características

- Extrae automáticamente la transcripción de un video de YouTube.
- Limpia el texto eliminando numeración, líneas vacías y saltos innecesarios.
- Traduce el texto del inglés al español usando el modelo `Helsinki-NLP/opus-mt-en-es`.
- Genera tres archivos:
  1. `<video_id>.txt` — Transcripción original.
  2. `<video_id>_cleaned.txt` — Texto limpio en inglés.
  3. `<video_id>_es.txt` — Traducción completa al español.

---

## 🧩 Estructura del Proyecto

📁 youtube_translator/
│
├── functions.py # Funciones auxiliares (limpieza y traducción)
├── main.py # Script principal
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo

---

## ⚙️ Instalación

1. Clona el repositorio o copia los archivos a tu entorno local:

   ```bash
   git clone https://github.com/tuusuario/youtube-translator.git
   cd youtube-translator

2. Crea y activa un entorno virtual (opcional pero recomendado):

python -m venv venv
source venv/bin/activate     # En Linux/Mac
venv\Scripts\activate        # En Windows


3. Instala las dependencias necesarias:

pip install -r requirements.txt

## ▶️ Uso

1. Ejecuta el script principal:

python main.py


2. Ingresa el ID del video de YouTube cuando se te solicite (por ejemplo, dQw4w9WgXcQ).

3. El programa:

- Descargará la transcripción en inglés.
- Limpiará el texto.
- Traducirá el contenido al español.
- Al finalizar, tendrás tres archivos de salida:

dQw4w9WgXcQ.txt
dQw4w9WgXcQ_cleaned.txt
dQw4w9WgXcQ_es.txt

## 🧠 Cómo funciona

1. Descarga de transcripción

from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.fetch(video_id)


2. Limpieza del texto

- Se eliminan números y saltos de línea.
- Se combina en un solo párrafo limpio.

3. Traducción

- Se divide el texto en fragmentos de hasta 800 caracteres.
- Cada fragmento se traduce con el modelo Helsinki-NLP/opus-mt-en-es.

## 🛠️ Funciones principales

clean_transcript(input_path, output_path)
Limpia la transcripción cruda y genera un archivo de texto plano.

chunk_text_by_sentences(text, max_chars=800)
Divide el texto en fragmentos cortos para evitar errores del modelo de traducción.

translate_file_en_es(input_path, output_path, max_chars=800)
Traduce un archivo del inglés al español y guarda el resultado.

## 💡 Recomendaciones

Este script solo funciona con videos que tienen transcripción disponible (manual o generada automáticamente).

La primera ejecución puede tardar un poco mientras se descarga el modelo de traducción.

Si el texto es muy largo, el script lo traduce en partes para evitar errores de memoria.

## 📚 Créditos

YouTube Transcript API

Hugging Face Transformers

Modelo de traducción: Helsinki-NLP/opus-mt-en-es

## 🧑‍💻 Autor

Lucas Mella
Data Scientist y desarrollador.
🌍 Chile — 2025

## 🪪 Licencia

Este proyecto está bajo la licencia MIT.
Puedes usarlo, modificarlo y distribuirlo libremente con atribución.