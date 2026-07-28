from flask import Flask, render_template_string, request, jsonify
from vedic_logic import VedicCalculator  # Assuming you save your previous class in vedic_logic.py

app = Flask(__name__)
calc = VedicCalculator()

# Simple HTML/CSS/JS Frontend embedded for simplicity
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vedic DevOps Calculator</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 400px; }
        h2 { text-align: center; color: #333; }
        .input-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; transition: background 0.2s; }
        button:hover { background: #1d4ed8; }
        #result { margin-top: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 6px; border-left: 4px solid #2563eb; display: none; }
        .step { margin-bottom: 0.5rem; font-size: 0.9rem; }
        .step-desc { color: #555; }
        .step-calc { color: #2563eb; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🕉️ Vedic Calculator</h2>
        <div class="input-group">
            <label>Operation</label>
            <select id="opType">
                <option value="square">Square (Ending in 5)</option>
                <option value="multiply">Multiply (2-digit)</option>
                <option value="add">Addition Sequence</option>
            </select>
        </div>
        <div class="input-group">
            <label>Number(s)</label>
            <input type="text" id="nums" placeholder="e.g., 55 or 94,62 or 5,8,2,3">
        </div>
        <button onclick="calculate()">Calculate</button>
        
        <div id="result"></div>
    </div>

    <script>
        async function calculate() {
            const op = document.getElementById('opType').value;
            const val = document.getElementById('nums').value;
            const resDiv = document.getElementById('result');
            
            resDiv.style.display = 'none';
            resDiv.innerHTML = 'Processing...';

            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ operation: op, input: val })
                });
                const data = await response.json();
                
                let html = `<strong>Result: ${data.result}</strong><br><br>`;
                data.steps.forEach((step, idx) => {
                    html += `<div class="step"><div class="step-desc">${idx+1}. ${step.explanation}</div><div class="step-calc">${step.calculation}</div></div>`;
                });
                resDiv.innerHTML = html;
                resDiv.style.display = 'block';
            } catch (err) {
                resDiv.innerHTML = 'Error: ' + err.message;
                resDiv.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.json
    op = data.get('operation')
    input_val = data.get('input')
    
    try:
        if op == 'square':
            n = int(input_val)
            res = calc.square_ending_in_5(n)
        elif op == 'multiply':
            parts = [int(x) for x in input_val.split(',')]
            res = calc.multiply_general(parts[0], parts[1])
        elif op == 'add':
            parts = [int(x) for x in input_val.split(',')]
            res = calc.add_with_ekadhika(parts)
        else:
            return jsonify({"error": "Invalid operation"}), 400
            
        # Format steps for JSON
        steps = [{"explanation": s.explanation, "calculation": s.calculation} for s in calc.steps]
        return jsonify({"result": res, "steps": steps})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Host 0.0.0.0 is critical for Docker accessibility
    app.run(host='0.0.0.0', port=5000)   