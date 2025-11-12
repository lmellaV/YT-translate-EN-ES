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

from reportlab.lib.pagesizes import A5, portrait
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registrar fuente Times New Roman
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))  # asegúrate de tener "times.ttf" en tu carpeta

# Ruta de salida
output_pdf_path = "documento_lindo.pdf"

# Crear documento vertical con márgenes estéticos
doc = SimpleDocTemplate(
    output_pdf_path,
    pagesize=portrait(A5),
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Estilos personalizados
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='TituloBonito',
    fontName='Times-Roman',
    fontSize=18,
    leading=22,
    alignment=1,  # centrado
    spaceAfter=12,
))

styles.add(ParagraphStyle(
    name='TextoNormal',
    fontName='Times-Roman',
    fontSize=12,
    leading=16,
    alignment=4,  # justificado
    spaceAfter=8,
))

styles.add(ParagraphStyle(
    name='Cita',
    fontName='Times-Roman',
    fontSize=11,
    leading=14,
    leftIndent=1*cm,
    rightIndent=1*cm,
    textColor='gray',
    italic=True,
))

# Contenido del documento
story = []

story.append(Paragraph("Mi Libro Bonito en PDF", styles['TituloBonito']))
story.append(Spacer(1, 12))
story.append(Paragraph(
    "Este es un ejemplo de documento generado con ReportLab. "
    "El texto está justificado, con márgenes suaves y tipografía Times New Roman.",
    styles['TextoNormal']
))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "“El diseño limpio y el formato adecuado hacen la lectura más agradable.”",
    styles['Cita']
))
story.append(PageBreak())
story.append(Paragraph("Segunda página", styles['TituloBonito']))
story.append(Paragraph("Aquí podrías continuar con tu texto...", styles['TextoNormal']))

# Generar PDF
doc.build(story)
print("PDF creado con éxito:", output_pdf_path)