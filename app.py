from flask import Flask, jsonify, Response
import folium
from database import DataTier

app = Flask(__name__)
db = DataTier()

@app.route('/')
def home():
    states = db.get_states()
    options = ''.join(f'<option value="{s}">{s}</option>' for s in states)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Real Estate Land Rates</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #2c3e50; text-align: center; }}
        .form-group {{ margin: 15px 0; }}
        label {{ display: block; font-weight: bold; margin-bottom: 5px; }}
        select {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }}
        #result {{ margin-top: 30px; padding: 20px; background: white; border-radius: 8px; display: none; }}
        #rate {{ font-size: 28px; font-weight: bold; color: #27ae60; text-align: center; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>🏡 Real Estate Land Rates</h1>
    <div class="form-group">
        <label>State</label>
        <select id="state" onchange="loadDistricts()">
            <option value="">-- Select State --</option>
            {options}
        </select>
    </div>
    <div class="form-group">
        <label>District</label>
        <select id="district" onchange="loadMandals()" disabled>
            <option value="">-- Select District --</option>
        </select>
    </div>
    <div class="form-group">
        <label>Mandal</label>
        <select id="mandal" onchange="loadInfo()" disabled>
            <option value="">-- Select Mandal --</option>
        </select>
    </div>
    <div id="result">
        <div id="rate"></div>
        <div id="map-container"></div>
    </div>
    <script>
        function loadDistricts() {{
            const state = document.getElementById('state').value;
            const d = document.getElementById('district');
            const m = document.getElementById('mandal');
            d.innerHTML = '<option value="">-- Select District --</option>';
            m.innerHTML = '<option value="">-- Select Mandal --</option>';
            d.disabled = true; m.disabled = true;
            document.getElementById('result').style.display = 'none';
            if (!state) return;
            fetch(`/api/districts/${{state}}`).then(r=>r.json()).then(data=>{{
                data.forEach(x=>d.innerHTML+=`<option value="${{x}}">${{x}}</option>`);
                d.disabled = false;
            }});
        }}
        function loadMandals() {{
            const state = document.getElementById('state').value;
            const district = document.getElementById('district').value;
            const m = document.getElementById('mandal');
            m.innerHTML = '<option value="">-- Select Mandal --</option>';
            m.disabled = true;
            document.getElementById('result').style.display = 'none';
            if (!district) return;
            fetch(`/api/mandals/${{state}}/${{district}}`).then(r=>r.json()).then(data=>{{
                data.forEach(x=>m.innerHTML+=`<option value="${{x}}">${{x}}</option>`);
                m.disabled = false;
            }});
        }}
        function loadInfo() {{
            const state = document.getElementById('state').value;
            const district = document.getElementById('district').value;
            const mandal = document.getElementById('mandal').value;
            if (!mandal) return;
            fetch(`/api/info/${{state}}/${{district}}/${{mandal}}`).then(r=>r.json()).then(data=>{{
                if (data.error) {{ alert(data.error); return; }}
                document.getElementById('rate').textContent = `Land Rate: ${{data.rate}} / sq.yd`;
                document.getElementById('map-container').innerHTML = data.map_html;
                document.getElementById('result').style.display = 'block';
            }});
        }}
    </script>
</body>
</html>"""
    return Response(html, mimetype='text/html')

@app.route('/api/districts/<state>')
def get_districts(state):
    return jsonify(db.get_districts(state))

@app.route('/api/mandals/<state>/<district>')
def get_mandals(state, district):
    return jsonify(db.get_mandals(state, district))

@app.route('/api/info/<state>/<district>/<mandal>')
def get_info(state, district, mandal):
    result = db.get_mandal_info(state, district, mandal)
    if result is None:
        return jsonify({'error': 'No data found'}), 404
    rate, lat, lon = result
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], popup=f"<b>{mandal}</b><br>Rate: ₹{rate:,}/sq.yd",
        icon=folium.Icon(color="green", icon="info-sign")).add_to(m)
    return jsonify({'rate': f"₹ {rate:,}", 'map_html': m._repr_html_()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
