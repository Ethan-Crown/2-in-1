"""
Flask dashboard for 8-bit simulation game: watch agents communicate, answer, rate, and evolve.
"""
from flask import Flask, render_template_string, request, jsonify
from .game import BitSimGame

app = Flask(__name__)

AGENT_NAMES = [f"Agent{i}" for i in range(1,11)]
QUESTIONS = [
    "What is the meaning of 8 bits?",
    "How would you solve a maze?",
    "What is the best pattern for flashing?",
    "How do you cooperate with others?"
]
game = BitSimGame(AGENT_NAMES, QUESTIONS)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>8-bit Simulation Game Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        #main { max-width: 900px; margin: auto; }
        .round { margin-bottom: 30px; }
        .eliminated { color: #B22222; }
        .offspring { color: #228B22; }
        .comms { color: #888; }
        canvas { border: 1px solid #333; background: #f0f0f0; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div id="main">
        <h2>8-bit Simulation Game Dashboard</h2>
        <button onclick="playRound()">Play Next Round</button>
        <canvas id="simCanvas" width="400" height="400"></canvas>
        <div id="rounds"></div>
    </div>
    <script>
        let lastPositions = {};
        let moveInterval = null;
        async function playRound() {
            const res = await fetch('/play', {method: 'POST'});
            const data = await res.json();
            renderRounds(data.history);
            if (data.history.length > 0) {
                lastPositions = data.history[data.history.length-1].positions;
                drawAgents(lastPositions);
                // Start real-time movement
                if (moveInterval) clearInterval(moveInterval);
                moveInterval = setInterval(stepAgents, 300);
            }
        }
        async function stepAgents() {
            const res = await fetch('/step', {method: 'POST'});
            const data = await res.json();
            if (data.positions) drawAgents(data.positions);
        }
        function drawAgents(positions) {
            const canvas = document.getElementById('simCanvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0,0,canvas.width,canvas.height);
            const grid = 20;
            const cell = canvas.width / grid;
            for (const [name, [x, y, color]] of Object.entries(positions)) {
                ctx.fillStyle = color;
                ctx.fillRect(x*cell+2, y*cell+2, cell-4, cell-4);
                ctx.fillStyle = '#000';
                ctx.font = '10px monospace';
                ctx.fillText(name, x*cell+4, y*cell+cell/2);
            }
        }
        function renderRounds(history) {
            let html = '';
            for (let i = 0; i < history.length; i++) {
                const r = history[i];
                html += `<div class='round'><b>Round ${i+1}:</b><br>`;
                html += `<b>Proximity Chat:</b> <span class='comms'>${r.comms.join(' | ')}</span><br>`;
                html += `<b>Question:</b> ${r.question}<br>`;
                html += `<b>Answers:</b><ul>`;
                for (const [agent, ans] of Object.entries(r.answers)) html += `<li>${agent}: ${ans}</li>`;
                html += `</ul><b>Ratings:</b><ul>`;
                for (const [agent, ratings] of Object.entries(r.ratings)) {
                    html += `<li>${agent} rated: `;
                    for (const [target, score] of Object.entries(ratings)) html += `${target}: ${score} `;
                    html += `</li>`;
                }
                html += `</ul><b>Scores:</b> `;
                for (const [agent, score] of Object.entries(r.scores)) html += `${agent}: ${score} `;
                html += `<br><span class='eliminated'><b>Eliminated:</b> ${r.eliminated.join(', ')}</span>`;
                html += `<br><span class='offspring'><b>Offspring:</b> ${r.offspring.join(', ')}</span>`;
                html += `</div>`;
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
    round_data = game.ask_question()
    return jsonify({"history": game.history})

@app.route("/step", methods=["POST"])
def step():
    positions = game.step()
    return jsonify({"positions": {a.name: (a.x, a.y, a.color) for a in game.agents}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
