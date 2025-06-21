"""
Meta-dashboard for unified monitoring of all submodules (superintelligence, Darwin Social Game, Bit Sim Game, etc.).
Shows plugin status, recent actions, and allows triggering rounds or sense/learn steps.
"""
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from superintelligence.registry import get_plugins
from superintelligence.user_memory import get_pref, set_pref
import json
import os
from dotenv import load_dotenv

# Load .env for superintelligence
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)
# Load .env for SEAL
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../SEAL/.env'), override=True)
# Load .env for LibreChat
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../LibreChat/.env'), override=True)
# Load .env for AutoGPT
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../AutoGPT/autogpt_platform/.env'), override=True)

# --- Ensure all plugins are imported so they register themselves ---
import superintelligence.browser_plugin
import superintelligence.learn_dgm
import superintelligence.sense_vita
import darwin_social_game.plugin
import bit_sim_game.plugin
# Optionally import SEAL, LibreChat, AutoGPT plugins if they expose any
try:
    import SEAL
except ImportError:
    pass
try:
    import LibreChat
except ImportError:
    pass
try:
    import AutoGPT
except ImportError:
    pass

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Superintelligence Meta-Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        #main { max-width: 900px; margin: auto; }
        .section { margin-bottom: 30px; }
        button { margin: 5px; }
        pre { background: #f0f0f0; padding: 10px; }
    </style>
</head>
<body>
    <div id="main">
        <h2>Superintelligence Meta-Dashboard</h2>
        <div class="section">
            <h3>Plugin Status</h3>
            <div id="plugin-status"></div>
        </div>
        <div class="section">
            <h3>Actions</h3>
            <button onclick="trigger('sense')">Sense</button>
            <button onclick="trigger('learn')">Learn</button>
            <button onclick="trigger('replicate')">Replicate</button>
            <button onclick="trigger('api')">API</button>
            <button onclick="trigger('autonomy')">Autonomy</button>
            <div id="action-result"></div>
        </div>
        <div class="section">
            <h3>User Preferences</h3>
            <form id="prefs-form">
                <input type="text" id="pref-key" placeholder="Preference Key">
                <input type="text" id="pref-value" placeholder="Value">
                <button type="submit">Save</button>
            </form>
            <pre id="prefs"></pre>
        </div>
        <div class="section">
            <h3>Browser Supervision</h3>
            <button onclick="loadBrowserHistory()">Refresh Browser History</button>
            <div id="browser-history"></div>
        </div>
    </div>
    <script>
        async function loadStatus() {
            const res = await fetch('/status');
            const data = await res.json();
            let html = '<ul>';
            for (const [cap, plugins] of Object.entries(data)) {
                html += `<li><b>${cap}</b>: ${plugins.length} plugin(s)</li>`;
            }
            html += '</ul>';
            document.getElementById('plugin-status').innerHTML = html;
        }
        async function trigger(cap) {
            const res = await fetch('/trigger', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ capability: cap })
            });
            const data = await res.json();
            document.getElementById('action-result').innerHTML = `<pre>${data.result}</pre>`;
        }
        async function loadPrefs() {
            const res = await fetch('/prefs');
            const data = await res.json();
            document.getElementById('prefs').textContent = JSON.stringify(data, null, 2);
        }
        async function loadBrowserHistory() {
            const res = await fetch('/browser_history');
            const data = await res.json();
            let html = '<ul>';
            for (const entry of data) {
                html += `<li><b>${entry.title}</b>: <a href="${entry.url}" target="_blank">${entry.url}</a><br>`;
                if (entry.screenshot) {
                    html += `<img src="/${entry.screenshot}" width="300"><br>`;
                }
                html += '</li>';
            }
            html += '</ul>';
            document.getElementById('browser-history').innerHTML = html;
        }
        document.getElementById('prefs-form').onsubmit = async (e) => {
            e.preventDefault();
            const key = document.getElementById('pref-key').value;
            const value = document.getElementById('pref-value').value;
            await fetch('/prefs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ [key]: value })
            });
            loadPrefs();
        };
        loadStatus();
        loadPrefs();
        loadBrowserHistory();
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/status")
def status():
    status = {cap: get_plugins(cap) for cap in ["sense", "learn", "replicate", "api", "autonomy"]}
    # Only show plugin counts
    return jsonify({k: v for k, v in status.items()})

@app.route("/trigger", methods=["POST"])
def trigger():
    cap = request.json.get("capability")
    results = []
    for func in get_plugins(cap):
        try:
            result = func()
            results.append(str(result))
        except Exception as e:
            results.append(f"Error: {e}")
    return jsonify({"result": '\n'.join(results) or "No plugins registered."})

@app.route("/prefs", methods=["GET", "POST"])
def prefs():
    if request.method == "POST":
        data = request.json or {}
        for k, v in data.items():
            set_pref(k, v)
        return jsonify({"status": "updated", "prefs": get_pref(None)})
    # GET
    prefs = get_pref(None)
    return jsonify(prefs or {})

@app.route("/browser_history")
def browser_history():
    try:
        with open("browser_history.json", "r") as f:
            history = json.load(f)
    except Exception:
        history = []
    return jsonify(history)

@app.route("/screenshot_<int:ts>.png")
def screenshot(ts):
    # Serve screenshots from the current directory
    return send_from_directory(os.getcwd(), f"screenshot_{ts}.png")

if __name__ == "__main__":
    import sys
    port = 6000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except Exception:
            pass
    print(f"[MetaDashboard] Starting on http://0.0.0.0:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=True)
