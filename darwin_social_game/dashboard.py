"""
Flask dashboard for visualizing Darwin Social Game debates and influence.
"""
from flask import Flask, render_template_string, request, jsonify
from .game import SocialGame

app = Flask(__name__)

AGENT_NAMES = ["Alice", "Bob", "Carol", "Dave"]
QUESTIONS = [
    "Should AI have rights?",
    "Is democracy the best system?",
    "Can machines be creative?",
    "Is persuasion ethical?"
]
game = SocialGame(AGENT_NAMES, QUESTIONS)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Darwin Social Game Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        #main { max-width: 700px; margin: auto; }
        .round { margin-bottom: 30px; }
        .influence { margin-top: 10px; }
        .vote { color: #888; }
    </style>
</head>
<body>
    <div id="main">
        <h2>Darwin Social Game Dashboard</h2>
        <button onclick="playRound()">Play Next Round</button>
        <div id="rounds"></div>
    </div>
    <script>
        async function playRound() {
            const res = await fetch('/play', {method: 'POST'});
            const data = await res.json();
            renderRounds(data.history);
        }
        function renderRounds(history) {
            let html = '';
            for (let i = 0; i < history.length; i++) {
                const r = history[i];
                html += `<div class='round'><b>Round ${i+1}:</b> <br> <b>Question:</b> ${r.question}<br>`;
                html += `<b>Arguments:</b><ul>`;
                for (const arg of r.arguments) html += `<li>${arg}</li>`;
                html += `</ul><b>Votes:</b><ul>`;
                for (const [agent, vote] of Object.entries(r.votes)) html += `<li>${agent} voted for: <span class='vote'>${vote||'None'}</span></li>`;
                html += `</ul><div class='influence'><b>Influence:</b> `;
                for (const [agent, inf] of Object.entries(r.influence)) html += `${agent}: ${inf} `;
                html += `</div></div>`;
            }
            document.getElementById('rounds').innerHTML = html;
        }
        // Initial render
        playRound();
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/play", methods=["POST"])
def play():
    round_data = game.play_round()
    return jsonify({"history": game.history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
