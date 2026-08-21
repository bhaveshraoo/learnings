import os
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'Mental_Health_Model.pkl')

# Load the pre-trained model pipeline safely without modifying it
print(f"Loading trained model from {MODEL_PATH}...")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully!")

# Categories expected by the model
TOP_COUNTRIES = ['Australia', 'Canada', 'France', 'Germany', 'India', 'Mexico', 'Other', 'Turkey', 'UK', 'USA']

def map_country(country_name):
    if country_name in TOP_COUNTRIES:
        return country_name
    return 'Other'

def generate_wellness_insights(score, data):
    """
    Generate personalized mental health insights and recommendations
    based on the predicted score and lifestyle habits.
    """
    insights = []
    
    # Sleep analysis
    sleep = float(data.get('Sleep_Hours_Per_Night', 7))
    if sleep < 6.5:
        insights.append({
            'title': 'Sleep Extension Needed',
            'desc': f'You are logging {sleep} hrs/night. Aim for 7–8 hours of restorative sleep to build cognitive resilience.'
        })
    elif sleep >= 7.0:
        insights.append({
            'title': 'Healthy Rest Habits',
            'desc': f'Great job maintaining {sleep} hrs of sleep! Consistent rest protects baseline mental well-being.'
        })

    # Screen time analysis
    screen_hrs = float(data.get('Avg_Daily_Usage_Hours', 5))
    unlocks = int(data.get('Daily_Unlocks', 150))
    if screen_hrs > 6 or unlocks > 180:
        insights.append({
            'title': 'Digital Detox Opportunity',
            'desc': f'High screen interaction ({screen_hrs} hrs, {unlocks} unlocks daily). Consider setting 30-minute tech-free windows before bed.'
        })
    else:
        insights.append({
            'title': 'Balanced Screen Habits',
            'desc': 'Your daily screen usage is within a healthy, mindful threshold.'
        })

    # Physical activity analysis
    activity = float(data.get('Physical_Activity_Hours', 1.5))
    if activity < 1.0:
        insights.append({
            'title': 'Physical Movement Boost',
            'desc': 'Adding even a 20-minute daily walk can significantly reduce anxiety and elevate mood scores.'
        })
    else:
        insights.append({
            'title': 'Active Lifestyle',
            'desc': f'Regular movement ({activity} hrs daily) boosts dopamine levels and supports stress recovery.'
        })

    # Determine status label and tier
    if score >= 7.5:
        status = "Optimal Well-being"
        summary = "Your habit profile indicates a strong foundation for mental balance, resilience, and vitality."
        color_class = "status-high"
    elif score >= 6.0:
        status = "Moderate Balance"
        summary = "Your mental score reflects good stability with potential for small lifestyle micro-adjustments."
        color_class = "status-med"
    else:
        status = "Elevated Strain / Care Needed"
        summary = "Your inputs signal high cognitive strain or burnout risk. Prioritize restorative breaks and self-care."
        color_class = "status-low"

    return {
        'status': status,
        'summary': summary,
        'color_class': color_class,
        'tips': insights
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        # Map inputs to DataFrame format expected by preprocessor
        study_hours = float(data.get('Study_Hours', 3.0))
        age = int(data.get('Age', 20))
        avg_usage = float(data.get('Avg_Daily_Usage_Hours', 4.5))
        unlocks = int(data.get('Daily_Unlocks', 150))
        physical_activity = float(data.get('Physical_Activity_Hours', 1.5))
        sleep_hours = float(data.get('Sleep_Hours_Per_Night', 7.0))
        stress_level = str(data.get('Stress_Level', 'Medium'))
        gender = str(data.get('Gender', 'Female'))
        academic_level = str(data.get('Academic_Level', 'Undergraduate'))
        platform = str(data.get('Most_Used_Platform', 'Instagram'))
        purpose = str(data.get('Purpose_Of_Use', 'Entertainment'))
        country_raw = str(data.get('Country', 'India'))
        grouped_country = map_country(country_raw)

        # Construct single-row DataFrame
        input_df = pd.DataFrame([{
            'Study_Hours': study_hours,
            'Age': age,
            'Avg_Daily_Usage_Hours': avg_usage,
            'Daily_Unlocks': unlocks,
            'Physical_Activity_Hours': physical_activity,
            'Sleep_Hours_Per_Night': sleep_hours,
            'Stress_Level': stress_level,
            'Gender': gender,
            'Academic_Level': academic_level,
            'Most_Used_Platform': platform,
            'Purpose_Of_Use': purpose,
            'grouped_countries': grouped_country
        }])

        # Generate prediction
        prediction = model.predict(input_df)[0]
        score_formatted = round(float(prediction), 2)
        
        # Clamp visual percentage for 0-10 score dial
        score_percent = min(max(round((score_formatted / 10.0) * 100, 1), 0), 100)

        analysis = generate_wellness_insights(score_formatted, data)

        return jsonify({
            'success': True,
            'score': score_formatted,
            'score_percent': score_percent,
            'status': analysis['status'],
            'summary': analysis['summary'],
            'color_class': analysis['color_class'],
            'tips': analysis['tips']
        })

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    print(f"Starting Mental Health Predictor app on http://127.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
