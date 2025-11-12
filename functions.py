from transformers import pipeline
import re

def clean_transcript(filepath, output_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        line = line.strip()
        # Ignora líneas vacías
        if not line:
            continue
        # Elimina numeración si existe al inicio
        line = line.lstrip("0123456789. ")
        cleaned.append(line)

    # Une todo en un solo párrafo
    plain_text = " ".join(cleaned)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(plain_text)

    print("Archivo plano creado:", output_path)

    
def chunk_text_by_sentences(text, max_chars=800):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())  # divide por punto, signo o exclamación
    chunks, current = [], ""

    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current += s + " "
        else:
            chunks.append(current.strip())
            current = s + " "
    if current:
        chunks.append(current.strip())
    return chunks

def translate_file_en_es(input_path, output_path, max_chars=800):
    print("Cargando modelo (solo la primera vez tarda unos minutos)...")
    translator = pipeline(
        "translation",
        model="Helsinki-NLP/opus-mt-en-es",
        src_lang="eng_Latn",
        tgt_lang="spa_Latn"
    )

    with open(input_path, 'r', encoding='utf-8-sig') as f:
        text = f.read().replace('\ufeff', '').strip()

    chunks = chunk_text_by_sentences(text, max_chars=max_chars)
    print(f"Número de fragmentos: {len(chunks)}")

    translated_parts = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Traduciendo parte {i}/{len(chunks)} ({len(chunk)} caracteres)...")
        try:
            result = translator(chunk)
            translated_parts.append(result[0]['translation_text'])
        except Exception as e:
            print(f"Error en parte {i}: {e}")
            translated_parts.append("[Error al traducir este fragmento]")

    translated_text = "\n".join(translated_parts)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_text)

    print("✅ Traducción completada. Guardado en:", output_path)

from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def make_pdf_book(input_path, output_pdf_path, title="YouTube Transcript Translation"):

    # Leer el texto
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    # Crear documento PDF
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=landscape(A5),
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    story = []

    # Estilo para el título
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Estilo del texto principal
    body_style = ParagraphStyle(
        name="BodyStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
    )

    # Agregar título
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    # Dividir texto en párrafos
    paragraphs = text.split("\n")
    for p in paragraphs:
        if p.strip():
            story.append(Paragraph(p.strip(), body_style))
            story.append(Spacer(1, 8))

    # Agregar salto de página opcional si el texto es largo
    if len(paragraphs) > 80:
        story.append(PageBreak())

    # Construir PDF
    doc.build(story)
    print("📖 PDF generado como libro en:", output_pdf_path)
