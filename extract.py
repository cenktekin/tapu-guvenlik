import PyPDF2

with open('TAPU_TERIMLERI_SOZLUK.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = "".join(page.extract_text() for page in reader.pages)

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(text)
