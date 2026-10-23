import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

print("--- 1. Loading Real ClinVar Dataset ---")
df = pd.read_csv('clinvar.csv', low_memory=False)
print(f"Total raw records found: {len(df)}")

# --- 2. Data Cleaning ---
clean_df = df.dropna(subset=['CLASS', 'POS', 'REF', 'ALT']).copy()
clean_df['POS'] = pd.to_numeric(clean_df['POS'], errors='coerce')
clean_df = clean_df.dropna(subset=['POS'])
print(f"Usable clean training records: {len(clean_df)}")

# --- 3. The Biochemical Feature Engine ---
print("--- Extracting 9-Dimensional Biochemical Features ---")

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

def extract_biochem(row):
    ref_str = str(row['REF']).upper().strip()
    alt_str = str(row['ALT']).upper().strip()
    
    # Safely grab the first character, default to 'A' if unknown so the model doesn't crash
    ref_aa = ref_str[0] if len(ref_str) > 0 and ref_str[0] in AA_PROPERTIES else 'A'
    alt_aa = alt_str[0] if len(alt_str) > 0 and alt_str[0] in AA_PROPERTIES else 'A'
    
    ref = AA_PROPERTIES[ref_aa]
    alt = AA_PROPERTIES[alt_aa]
    
    return pd.Series({
        'REF_len': len(ref_str),
        'ALT_len': len(alt_str),
        'mass_diff': alt['mass'] - ref['mass'],
        'abs_mass_diff': abs(alt['mass'] - ref['mass']),
        'hydro_diff': alt['hydro'] - ref['hydro'],
        'abs_hydro_diff': abs(alt['hydro'] - ref['hydro']),
        'charge_diff': alt['charge'] - ref['charge'],
        'charge_class_change': 1 if ref['charge'] != alt['charge'] else 0
    })

# Apply the math engine to the dataset
features_df = clean_df.apply(extract_biochem, axis=1)
final_data = pd.concat([clean_df[['POS', 'CLASS']], features_df], axis=1)

# Define our robust Features (X) and Target (y)
feature_columns = [
    'POS', 'REF_len', 'ALT_len', 'mass_diff', 'abs_mass_diff', 
    'hydro_diff', 'abs_hydro_diff', 'charge_diff', 'charge_class_change'
]
X = final_data[feature_columns]
y = final_data['CLASS']

# --- 4. Training the Machine Learning Model ---
print("--- Training the Upgraded Random Forest AI ---")
model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
model.fit(X, y)

# --- 5. Saving the Model ---
joblib.dump(model, 'asep_model.pkl')
print("\n--- SUCCESS! ---")
print("Your highly advanced 9-dimensional AI Model has been saved as 'asep_model.pkl'.")