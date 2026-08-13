from flask import Flask, request, send_file
import io
from docx import Document

app = Flask(__name__)

@app.route('/', methods=['POST'])
def redact_file():
    file = request.files['file']
    doc = Document(io.BytesIO(file.read()))

    # 🟢 Add your redaction logic here.

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='redacted.docx')