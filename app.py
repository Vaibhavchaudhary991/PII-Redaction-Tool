import subprocess
print("📦 Installed packages:")
print(subprocess.check_output(["pip", "list"]).decode())


from flask import Flask, request, send_file
import io
from docx import Document

# Import your redaction logic
from redactor import create_analyzer
from main import redact_document

app = Flask(__name__)

# Initialize analyzer once
analyzer = create_analyzer()

@app.route('/', methods=['GET', 'POST'])
def redact_file():
    # GET request - show instructions
    if request.method == 'GET':
        return {
            "message": "PII Redaction Tool API",
            "usage": "POST a .docx file to / with key 'file'",
            "example": "curl -X POST -F 'file=@Input.docx' https://pii-redaction-tool.onrender.com/"
        }
    
    # POST request - redact the file
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400
    
    file = request.files['file']
    
    # Validate file type
    if not file.filename.endswith('.docx'):
        return {"error": "Only .docx files are supported"}, 400
    
    try:
        # Read uploaded file
        doc = Document(io.BytesIO(file.read()))
        
        # Redact the document
        redact_document(doc, analyzer)
        
        # Save to bytes
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        # Return redacted file
        return send_file(
            output,
            as_attachment=True,
            download_name=f'redacted_{file.filename}',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}, 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PII Redaction Tool",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)