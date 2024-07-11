from flask import Flask, jsonify, request, render_template, send_file, url_for
import sqlite3
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/prescriptions'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('medicamentos.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    query = """
    SELECT substancia, produto, apresentacao, laboratorio 
    FROM medicamentos 
    WHERE substancia LIKE ? OR produto LIKE ?
    """
    results = query_db(query, ('%' + term + '%', '%' + term + '%'))
    
    def extract_dose(text):
        match = re.search(r'(\d+)', text)
        return int(match.group(1)) if match else 0
    
    suggestions = sorted(
        [
            {
                'substancia': row['substancia'],
                'produto': row['produto'],
                'apresentacao': row['apresentacao'],
                'laboratorio': row['laboratorio']
            } for row in results
        ],
        key=lambda x: (x['substancia'], x['produto'], extract_dose(x['apresentacao']))
    )
    
    return jsonify(suggestions)

@app.route('/generate_prescription', methods=['POST'])
def generate_prescription():
    medications = request.json.get('medications', [])
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Título centralizado
    story.append(Paragraph("Prescrição Médica", styles['Title']))
    story.append(Spacer(1, 12))

    for med in medications:
        text = f"{med['label']}, {med['apresentacao']} ({med['laboratorio']})"
        story.append(Paragraph(text, styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'prescricao.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    return jsonify({'url': url_for('static', filename='prescriptions/prescricao.pdf')})

if __name__ == '__main__':
    app.run(debug=True)
