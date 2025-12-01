from flask import Flask, request, jsonify, send_file
import os
import pandas as pd
from patient_profile_builder import PatientProfileBuilder, download_nhanes_file
from flask_cors import CORS
      
app = Flask(__name__)
CORS(app)  # This allows all routes to be accessed from your UI)
    
# Instantiate the PatientProfileBuilder with the callable download function.
profile_builder = PatientProfileBuilder(download_nhanes_file)

# Store the last merged file path globally (for visualization access)
MERGED_CSV_PATH = os.path.abspath("patient_profile_temp.csv")
    
      
@app.route('/', methods=['GET'])
def index():
    return "NHANES Profile API is running!"


@app.route('/profile', methods=['POST'])
def profile():
    """
    Expects a JSON payload with:
      - selections: a dictionary mapping categories to lists of file descriptio$
      - cycles: a list of cycle years.
    
    Returns:
      The merged patient profile as a CSV file.
    """
    data = request.get_json()
    selections = data.get("selections")
    cycles = data.get("cycles") 
      
    if not selections or not cycles:          return jsonify({'error': 'Please provide both "selections" and "cycles"$
    
    try:
        profile_df = profile_builder.build_profile(selections, cycles)
        if profile_df is None or profile_df.empty:
            return jsonify({'error': 'No data found for the given selections an$
    
        # Save CSV to a known path for later visualization access
        profile_df.to_csv(MERGED_CSV_PATH, index=False)
        return send_file(MERGED_CSV_PATH, as_attachment=True, download_name="pa$
    
    except Exception as e:
        print("Error in /profile endpoint:", str(e))
        return jsonify({'error': str(e)}), 500
            
    
@app.route('/visualization', methods=['GET'])
def visualization():
   """
    Returns processed data for visualization as JSON.
    It reads from the last saved merged CSV file.
   """
    try:
        if not os.path.exists(MERGED_CSV_PATH):
            return jsonify({'error': 'No merged profile found. Please run analy$

        df = pd.read_csv(MERGED_CSV_PATH)
       
        # Adjust these columns to match your data structure
        if 'RIDAGEYR' not in df.columns:
            return jsonify({'error': 'Age column not found in data.'}), 400
    
        # Collect data (adjust health_metric_col based on your data)
        age = df['RIDAGEYR'].tolist()

        # Example: choose first available numeric health metric      
        health_metric_col = None
        for col in df.columns:
            if col.startswith('DIQ010') or col.startswith('Blood') or col.start$
                health_metric_col = col
                break
        
        if not health_metric_col:
            return jsonify({'error': 'Health metric column not found in data.'}$
        
        health_metric = df[health_metric_col].tolist()
        
        # Optional: other labels for scatterplot
        labels = df['SEQN'].tolist() if 'SEQN' in df.columns else list(range(le$
                
        return jsonify({
            'age': age,
            'healthMetric': health_metric,
            'labels': labels,
            'metricName': health_metric_col
        })
        
    except Exception as e:
        print("Error in /visualization endpoint:", str(e))
        return jsonify({'error': str(e)}), 500
            
            
if __name__ == '__main__':   
    app.run(host='0.0.0.0', port=5050, debug=True)

