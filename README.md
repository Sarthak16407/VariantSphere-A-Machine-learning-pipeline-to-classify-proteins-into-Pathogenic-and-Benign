# VariantSphere-A-Machine-learning-pipeline-to-classify-proteins-into-Pathogenic-and-Benign

# 🧬 VariantSphere — AI-Powered Genetic Variant Analysis

**VariantSphere** is a lightweight AI-powered platform designed to analyze genetic variants and predict their potential classification as **Benign** or **Pathogenic**. It combines machine learning, biochemical feature analysis, ClinVar database lookup, protein structure visualization, and automated PDF report generation into an interactive analysis workflow.

The project aims to make genetic variant analysis more accessible for educational purposes, bioinformatics research, and exploratory genomic studies.

> **Disclaimer:** VariantSphere is an academic and research-oriented project. Its predictions are experimental and must not be used for clinical diagnosis, medical decisions, or treatment planning in humans.

## ✨ Key Features

- **AI-Based Variant Classification:** Predicts whether a genetic variant is classified as Benign or Pathogenic using a trained Random Forest model.
- **Prediction Confidence:** Displays the model's highest predicted class probability as a percentage.
- **Biochemical Feature Analysis:** Extracts features related to amino acid mass, hydrophobicity, and charge differences.
- **ClinVar Database Integration:** Searches for matching variant records and retrieves associated disease or phenotype information when available.
- **Protein Structure Visualization:** Supports interactive 3D visualization of protein structures using a Protein Data Bank (PDB) identifier.
- **Simulated CRISPR-Cas9 Guide RNA Generation:** Produces an exploratory guide RNA-like sequence for variants classified as pathogenic.
- **Automated PDF Reports:** Generates downloadable reports containing analysis details and prediction results.
- **Interactive Analysis Workflow:** Brings multiple variant-analysis capabilities together in one platform.

*Note: Protein visualization depends on the frontend implementation. The CRISPR guide RNA output is simulated and is not validated for experimental use.*

---

## 🧬 How It Works

VariantSphere follows a workflow that combines input processing, biochemical feature extraction, machine learning, database lookup, and report generation.

1. **Input:** The user provides the protein PDB ID, genomic position, reference allele, and alternate allele.
2. **Feature Extraction:** The backend derives numerical features from the position and biochemical properties associated with the reference and alternate inputs.
3. **AI Prediction:** A trained Random Forest classifier predicts the variant class and provides a confidence score.
4. **Database Lookup:** The application searches the ClinVar dataset for a matching position, reference allele, and alternate allele.
5. **Additional Output:** The application generates a simulated CRISPR guide RNA-like sequence for variants classified as pathogenic.
6. **Report Generation:** The backend creates a PDF report containing the analysis details and results.

### Machine Learning Features

The current training pipeline uses nine input features:

| Feature | Description |
|---|---|
| Genomic position | Position supplied for the variant |
| Reference length | Length of the reference allele |
| Alternate length | Length of the alternate allele |
| Mass difference | Signed difference in amino acid mass |
| Absolute mass difference | Magnitude of the mass difference |
| Hydrophobicity difference | Signed difference in hydrophobicity |
| Absolute hydrophobicity difference | Magnitude of the hydrophobicity difference |
| Charge difference | Signed difference in amino acid charge |
| Charge class change | Indicates whether the assigned charges differ |

The model is configured as a `RandomForestClassifier` with 100 trees, a maximum depth of 15, and a fixed random seed of 42.

**Important implementation note:** The current feature extraction code uses the first character of the reference and alternate inputs to look up amino acid properties. DNA nucleotide alleles and protein amino acid substitutions are different representations. Consequently, the current model pipeline should be validated carefully before interpreting its predictions as biologically meaningful genetic-variant classifications.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and machine learning |
| Flask | Backend API |
| Flask-CORS | Cross-origin API access |
| Scikit-learn | Random Forest classification |
| Pandas | Dataset processing and ClinVar lookup |
| Joblib | Saving and loading the trained model |
| FPDF | PDF report generation |
| ClinVar dataset | Variant classification and phenotype information |
| Protein Data Bank (PDB) | Protein structure identification for visualization |

---

## 📂 Project Structure

The repository can be organized as follows:

```text
VariantSphere/
│
├── app.py
├── train_model.py
├── clinvar.csv
├── asep_model.pkl
├── requirements.txt
├── README.md
│
└── docs/
    └── images/
        ├── dashboard.png
        ├── prediction.png
        ├── protein-visualization.png
        ├── variant-details.png
        └── report.png
```

- `app.py` — Flask backend containing prediction, database lookup, and PDF report endpoints.
- `train_model.py` — Data cleaning, feature extraction, Random Forest training, and model serialization.
- `clinvar.csv` — Variant dataset used by the training pipeline and backend lookup.
- `asep_model.pkl` — Serialized trained model loaded by the backend.
- `requirements.txt` — Python package dependencies.
- `docs/images/` — Screenshots used in this README.

The frontend source files and any additional visualization assets should also be included in the repository according to the actual frontend implementation.

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Sarthak16407/VariantSphere.git
cd VariantSphere
```

Replace `Sarthak16407` with your GitHub username.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file containing:

```text
Flask
Flask-Cors
pandas
scikit-learn
joblib
fpdf
```

Install the packages:

```bash
pip install -r requirements.txt
```

For reproducible results, use the dependency versions tested with the project.

### 4. Prepare the Dataset and Model

Ensure that `clinvar.csv` is present in the project directory.

To train the model, run:

```bash
python train_model.py
```

This generates `asep_model.pkl`, which is loaded by the Flask backend.

Alternatively, if a compatible trained model is already available, place it in the expected project directory without retraining.

**Dataset requirement:** The training script expects the columns `CLASS`, `POS`, `REF`, and `ALT`. Ensure that the class labels are encoded consistently with the prediction logic in `app.py`.

### 5. Start the Backend

```bash
python app.py
```

The Flask server starts on:

```text
http://127.0.0.1:5000
```

The backend exposes the following endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/predict` | POST | Predicts a variant class and returns analysis information |
| `/generate_report` | POST | Generates and returns a PDF report |

The frontend, if separate, must be configured to communicate with this backend address during local development.

---

## 🔌 API Usage

### Predict a Genetic Variant

**Endpoint:** `POST /predict`

Example JSON request:

```json
{
  "protein_id": "1A3N",
  "pos": 12345,
  "ref": "A",
  "alt": "T"
}
```

Example response structure:

```json
{
  "status": "success",
  "protein_analyzed": "1A3N",
  "prediction": "Benign Variant (AI Confidence: 85.0%)",
  "associated_disease": "Novel Variant (No specific clinical phenotype recorded)",
  "crispr_grna": "Not Required (Benign Variant)",
  "pos": 12345,
  "ref": "A",
  "alt": "T"
}
```

*The values above are illustrative and do not represent a verified prediction. Actual responses depend on the trained model and dataset.*

### Generate a PDF Report

**Endpoint:** `POST /generate_report`

The endpoint accepts JSON containing the variant details, prediction, associated phenotype, and CRISPR output, then returns a downloadable PDF document.

---

## 📊 Dataset & Model Considerations

VariantSphere uses a ClinVar-derived dataset to support model training and variant information lookup.

Before using the model for scientific analysis, consider the following:

- Verify the dataset's source, version, licensing, and class-label definitions.
- Check for class imbalance and missing or inconsistent values.
- Evaluate performance on independent, held-out data.
- Avoid data leakage between training and evaluation records.
- Report appropriate metrics, including precision, recall, F1-score, and specificity.
- Validate whether the input features represent the biological variant correctly.
- Treat confidence scores as model probabilities, not as proof of biological certainty.

A high prediction confidence does not necessarily mean a prediction is accurate or clinically reliable.

---

## ⚠️ Limitations & Responsible Use

VariantSphere is an educational and exploratory research project. Its current implementation has important limitations:

- It is not a clinically validated diagnostic system.
- The current model's feature extraction requires further biological validation, particularly for nucleotide alleles versus amino acid substitutions.
- The prediction confidence score is not, by itself, a measure of clinical certainty.
- ClinVar matches depend on the dataset's contents and the exact variant representation.
- The generated CRISPR guide RNA-like sequence is simulated and is not guaranteed to target the intended genomic location or satisfy experimental design requirements.
- Protein visualization depends on the frontend and its integration with protein structure data.
- Results may be incomplete, incorrect, or affected by dataset limitations.

**Do not use VariantSphere to make medical decisions, diagnose disease, select treatments, or perform gene-editing experiments.** All outputs require independent validation by qualified researchers before any scientific interpretation.

---

## 🚀 Future Enhancements

Potential improvements include:

- More biologically appropriate variant feature engineering.
- Independent model evaluation and probability calibration.
- Integration of additional variant annotation resources.
- Improved validation of genomic coordinates and allele representations.
- Enhanced 3D protein visualization and mutation highlighting.
- Biologically validated CRISPR guide design using appropriate reference sequences.
- Expanded PDF reports with model evaluation metrics and data provenance.
- Support for larger datasets and reproducible analysis workflows.



---

## ⭐ Acknowledgements

- **NCBI ClinVar** — Genetic variant classification and associated clinical significance information.
- **Protein Data Bank (PDB)** — Protein structure data and identification.
- **Scikit-learn** — Machine learning tools used to train the Random Forest classifier.
- The open-source Python ecosystem for supporting the development of this project.

---

**VariantSphere — Exploring genetic variation through AI and bioinformatics.**
