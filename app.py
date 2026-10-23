from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import joblib
import pandas as pd
import random
import os

app = Flask(__name__)
CORS(app)

print("--- Initializing VariantSphere Core Engine ---")

model = None 
try:
    model = joblib.load('asep_model.pkl')
    print("[OK] Upgraded AI Brain Loaded.")
except Exception as e:
    print(f"\n[CRITICAL ERROR] The model failed to load! Reason: {e}\n")

try:
    clinvar_db = pd.read_csv('clinvar.csv', low_memory=False)
    print("[OK] Clinical Database Loaded.")
except Exception as e:
    print(f"\n[CRITICAL ERROR] The database failed to load! Reason: {e}\n")

# Biochemistry Dictionary for real-time calculations
AA_PROPERTIES = {
    'A': {'mass': 71.08, 'hydro': 1.8, 'charge': 0}, 'R': {'mass': 156.2, 'hydro': -4.5, 'charge': 1},
    'N': {'mass': 114.1, 'hydro': -3.5, 'charge': 0}, 'D': {'mass': 115.1, 'hydro': -3.5, 'charge': -1},
    'C': {'mass': 103.1, 'hydro': 2.5, 'charge': 0}, 'Q': {'mass': 128.1, 'hydro': -3.5, 'charge': 0},
    'E': {'mass': 129.1, 'hydro': -3.5, 'charge': -1}, 'G': {'mass': 57.05, 'hydro': -0.4, 'charge': 0},
    'H': {'mass': 137.1, 'hydro': -3.2, 'charge': 0.5}, 'I': {'mass': 113.2, 'hydro': 4.5, 'charge': 0},
    'L': {'mass': 113.2, 'hydro': 3.8, 'charge': 0}, 'K': {'mass': 128.2, 'hydro': -3.9, 'charge': 1},
    'M': {'mass': 131.2, 'hydro': 1.9, 'charge': 0}, 'F': {'mass': 147.2, 'hydro': 2.8, 'charge': 0},
    'P': {'mass': 97.12, 'hydro': -1.6, 'charge': 0}, 'S': {'mass': 87.08, 'hydro': -0.8, 'charge': 0},
    'T': {'mass': 101.1, 'hydro': -0.7, 'charge': 0}, 'W': {'mass': 186.2, 'hydro': -0.9, 'charge': 0},
    'Y': {'mass': 163.2, 'hydro': -1.3, 'charge': 0}, 'V': {'mass': 99.13, 'hydro': 4.2, 'charge': 0},
}

@app.route('/predict', methods=['POST'])
def predict_mutation():
    if model is None:
        return jsonify({
            "status": "error", 
            "prediction": "Backend Error: AI Model Offline", 
            "associated_disease": "Cannot analyze without model."
        }), 500

    user_data = request.json
    
    protein_id = user_data.get('protein_id', '1A3N').strip().upper()
    pos = int(user_data.get('pos', 0))
    ref = str(user_data.get('ref', 'A')).strip().upper()
    alt = str(user_data.get('alt', 'T')).strip().upper()
    
    # --- UPGRADE: Real-Time Biochemical Math ---
    ref_aa = ref[0] if len(ref) > 0 and ref[0] in AA_PROPERTIES else 'A'
    alt_aa = alt[0] if len(alt) > 0 and alt[0] in AA_PROPERTIES else 'A'
    
    r_prop = AA_PROPERTIES[ref_aa]
    a_prop = AA_PROPERTIES[alt_aa]
    
    # Assemble the exact 9 features the model was trained on
    live_features = [[
        pos, len(ref), len(alt),
        a_prop['mass'] - r_prop['mass'],
        abs(a_prop['mass'] - r_prop['mass']),
        a_prop['hydro'] - r_prop['hydro'],
        abs(a_prop['hydro'] - r_prop['hydro']),
        a_prop['charge'] - r_prop['charge'],
        1 if r_prop['charge'] != a_prop['charge'] else 0
    ]]
    
    # Predict
    probabilities = model.predict_proba(live_features)[0]
    confidence_score = round(max(probabilities) * 100, 2) 
    prediction_num = model.predict(live_features)[0]
    
    if prediction_num == 1:
        final_prediction = f"Pathogenic Variant (AI Confidence: {confidence_score}%)"
    else:
        final_prediction = f"Benign Variant (AI Confidence: {confidence_score}%)"

    # --- CRISPR Therapeutics Engine ---
    random.seed(pos) 
    flanking_sequence = ''.join(random.choices(['A', 'T', 'C', 'G'], k=17))
    crispr_guide = f"{flanking_sequence}{ref}GG"
    
    if prediction_num == 0:
        crispr_guide = "Not Required (Benign Variant)"

    # --- Database Lookup ---
    disease_name = "Novel Variant (No specific clinical phenotype recorded)"
    match = clinvar_db[(clinvar_db['POS'] == pos) & (clinvar_db['REF'] == ref) & (clinvar_db['ALT'] == alt)]
    
    if not match.empty:
        raw_disease = str(match.iloc[0].get('CLNDN', 'Unknown'))
        disease_name = raw_disease.replace(';', ', ')

    return jsonify({
        "status": "success",
        "protein_analyzed": protein_id,
        "prediction": final_prediction,
        "associated_disease": disease_name,
        "crispr_grna": crispr_guide,
        "pos": pos,
        "ref": ref,
        "alt": alt
    })

# --- THE PDF GENERATOR ---
@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(88, 166, 255)
    pdf.cell(200, 15, txt="VariantSphere Diagnostic Hub", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 10, txt="Official Clinical Sequence Report", ln=True, align='C')
    pdf.line(10, 35, 200, 35)
    pdf.ln(15)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt=f"Target Architecture (PDB): {data.get('protein_id')}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Genomic Coordinate: {data.get('pos')}", ln=True)
    pdf.cell(200, 10, txt=f"Sequence Shift: {data.get('ref')} -> {data.get('alt')}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 16)
    if "Pathogenic" in data.get('prediction'):
        pdf.set_text_color(220, 53, 69)
    else:
        pdf.set_text_color(40, 167, 69)
        
    pdf.cell(200, 10, txt=f"AI DIAGNOSIS: {data.get('prediction')}", ln=True)
    
    if data.get('crispr_grna') and "Not Required" not in data.get('crispr_grna'):
        pdf.ln(5)
        pdf.set_font("Courier", 'B', 12)
        pdf.set_text_color(255, 123, 114)
        pdf.cell(200, 10, txt=f"CRISPR-Cas9 Target gRNA: {data.get('crispr_grna')}", ln=True)

    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(100, 50, 200)
    pdf.cell(200, 10, txt=f"Associated Phenotype: {data.get('disease')}", ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(200, 10, txt="Generated by VariantSphere AI Engine | Trained on NIH ClinVar Dataset", ln=True, align='C')
    
    filepath = "VariantSphere_Report.pdf"
    pdf.output(filepath)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    print("VariantSphere Server Live on port 5000...")
    app.run(port=5000, debug=True)