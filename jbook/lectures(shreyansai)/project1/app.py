import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Load ML artifacts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COLUMNS_PATH = os.path.join(BASE_DIR, 'columns.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')
MODEL_PATH = os.path.join(BASE_DIR, 'KNN_heart.pkl')

feature_cols = joblib.load(COLUMNS_PATH)
scaler = joblib.load(SCALER_PATH)
knn_model = joblib.load(MODEL_PATH)

def preprocess_patient_data(data):
    """
    Transforms raw user dictionary into scaled 2D array matching the trained KNN model.
    """
    raw_df = pd.DataFrame([{
        'Age': float(data.get('Age', 45)),
        'Sex': str(data.get('Sex', 'M')),
        'ChestPainType': str(data.get('ChestPainType', 'ATA')),
        'RestingBP': float(data.get('RestingBP', 120)),
        'Cholesterol': float(data.get('Cholesterol', 200)),
        'FastingBS': int(data.get('FastingBS', 0)),
        'RestingECG': str(data.get('RestingECG', 'Normal')),
        'MaxHR': float(data.get('MaxHR', 150)),
        'ExerciseAngina': str(data.get('ExerciseAngina', 'N')),
        'Oldpeak': float(data.get('Oldpeak', 0.0)),
        'ST_Slope': str(data.get('ST_Slope', 'Up'))
    }])
    
    # One-hot encode using get_dummies
    encoded_df = pd.get_dummies(raw_df)
    
    # Align columns with training dataset columns
    final_df = encoded_df.reindex(columns=feature_cols, fill_value=0)
    
    # Scale features using pre-fitted StandardScaler
    scaled_features = scaler.transform(final_df)
    return final_df, scaled_features

def analyze_risk_factors(data):
    """
    Generates clinical observations based on standard medical guidelines.
    """
    factors = []
    
    bp = float(data.get('RestingBP', 120))
    if bp >= 140:
        factors.append({'name': 'Stage 2 Hypertension', 'detail': f'Resting BP is high ({bp} mm Hg)', 'severity': 'high'})
    elif bp >= 130:
        factors.append({'name': 'Stage 1 Hypertension', 'detail': f'Resting BP is elevated ({bp} mm Hg)', 'severity': 'medium'})

    chol = float(data.get('Cholesterol', 200))
    if chol >= 240:
        factors.append({'name': 'Hypercholesterolemia', 'detail': f'Cholesterol level is high ({chol} mg/dL)', 'severity': 'high'})
    elif chol >= 200:
        factors.append({'name': 'Borderline High Cholesterol', 'detail': f'Cholesterol is elevated ({chol} mg/dL)', 'severity': 'medium'})

    if int(data.get('FastingBS', 0)) == 1:
        factors.append({'name': 'Elevated Fasting Blood Sugar', 'detail': 'Fasting blood sugar > 120 mg/dL', 'severity': 'medium'})

    oldpeak = float(data.get('Oldpeak', 0.0))
    if oldpeak >= 2.0:
        factors.append({'name': 'Significant ST Depression', 'detail': f'Oldpeak is high ({oldpeak} mm), indicating myocardial ischemia risk', 'severity': 'high'})
    elif oldpeak > 0.8:
        factors.append({'name': 'Moderate ST Depression', 'detail': f'Oldpeak is elevated ({oldpeak} mm)', 'severity': 'medium'})

    st_slope = data.get('ST_Slope', 'Up')
    if st_slope == 'Flat':
        factors.append({'name': 'Flat ST Slope', 'detail': 'Flat slope during peak exercise suggests coronary artery disease risk', 'severity': 'medium'})
    elif st_slope == 'Down':
        factors.append({'name': 'Downsloping ST Segment', 'detail': 'Downsloping ST segment is a strong indicator of ischemia', 'severity': 'high'})

    if data.get('ExerciseAngina') == 'Y':
        factors.append({'name': 'Exercise-Induced Angina', 'detail': 'Chest discomfort during physical exertion', 'severity': 'high'})

    if data.get('ChestPainType') == 'ASY':
        factors.append({'name': 'Asymptomatic Chest Pain', 'detail': 'Silent ischemia presentation (ASY pain type)', 'severity': 'high'})

    ecg = data.get('RestingECG')
    if ecg == 'LVH':
        factors.append({'name': 'Left Ventricular Hypertrophy', 'detail': 'Resting ECG shows LVH condition', 'severity': 'medium'})
    elif ecg == 'ST':
        factors.append({'name': 'ST-T Wave Abnormality', 'detail': 'Resting ECG shows ST-T wave changes', 'severity': 'medium'})

    return factors

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'model_type': 'K-Nearest Neighbors Classifier',
        'k_neighbors': int(knn_model.n_neighbors),
        'n_features': len(feature_cols),
        'features': feature_cols
    })

@app.route('/api/sample', methods=['GET'])
def get_sample_profiles():
    samples = [
        {
            'id': 'low_risk',
            'name': 'Healthy Adult (Low Risk)',
            'description': '40y Male with normal BP, healthy cholesterol, upsloping ST, and no angina.',
            'data': {
                'Age': 40, 'Sex': 'M', 'ChestPainType': 'ATA', 'RestingBP': 120,
                'Cholesterol': 210, 'FastingBS': 0, 'RestingECG': 'Normal',
                'MaxHR': 172, 'ExerciseAngina': 'N', 'Oldpeak': 0.0, 'ST_Slope': 'Up'
            }
        },
        {
            'id': 'moderate_risk',
            'name': 'Moderate Risk Adult',
            'description': '52y Female with borderline BP, flat ST slope, and non-anginal pain.',
            'data': {
                'Age': 52, 'Sex': 'F', 'ChestPainType': 'NAP', 'RestingBP': 135,
                'Cholesterol': 230, 'FastingBS': 0, 'RestingECG': 'Normal',
                'MaxHR': 142, 'ExerciseAngina': 'N', 'Oldpeak': 1.0, 'ST_Slope': 'Flat'
            }
        },
        {
            'id': 'high_risk',
            'name': 'High Risk Cardiac Profile',
            'description': '63y Male with high BP, high cholesterol, exercise angina, & flat ST slope.',
            'data': {
                'Age': 63, 'Sex': 'M', 'ChestPainType': 'ASY', 'RestingBP': 160,
                'Cholesterol': 288, 'FastingBS': 1, 'RestingECG': 'ST',
                'MaxHR': 108, 'ExerciseAngina': 'Y', 'Oldpeak': 2.5, 'ST_Slope': 'Flat'
            }
        }
    ]
    return jsonify(samples)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Preprocess and scale input
        raw_encoded, scaled_input = preprocess_patient_data(data)
        
        # KNN Prediction
        pred_class = int(knn_model.predict(scaled_input)[0])
        probabilities = knn_model.predict_proba(scaled_input)[0].tolist()
        
        high_risk_prob = round(probabilities[1] * 100, 1) if len(probabilities) > 1 else (100.0 if pred_class == 1 else 0.0)
        low_risk_prob = round(100.0 - high_risk_prob, 1)
        
        # Nearest Neighbors Analysis
        distances, indices = knn_model.kneighbors(scaled_input, n_neighbors=int(knn_model.n_neighbors))
        neighbor_list = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            neighbor_list.append({
                'rank': i + 1,
                'sample_index': int(idx),
                'distance': round(float(dist), 3)
            })
            
        risk_factors = analyze_risk_factors(data)
        
        response = {
            'status': 'success',
            'prediction': pred_class, # 0 = Normal, 1 = Heart Disease Risk
            'risk_label': 'High Risk of Heart Disease' if pred_class == 1 else 'Low Risk / Normal',
            'risk_level': 'HIGH' if pred_class == 1 else 'LOW',
            'risk_percentage': high_risk_prob,
            'probabilities': {
                'low_risk': low_risk_prob,
                'high_risk': high_risk_prob
            },
            'risk_factors': risk_factors,
            'nearest_neighbors': neighbor_list,
            'input_summary': data
        }
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Heart Disease Prediction Server on http://127.0.0.1:5005 ...")
    app.run(host='0.0.0.0', port=5005, debug=False)
