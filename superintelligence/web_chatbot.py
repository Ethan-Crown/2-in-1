"""
Flask web app for the superintelligence chatbot agent.
Supports text chat via browser, routes all messages through the full pipeline.
"""
from flask import Flask, render_template_string, request, jsonify
from .input_module import get_multimodal_input
from .reasoning_module import multimodal_reasoning
from .agent_layer import agent_decision
from .evolution_module import evolve_actions
from .memory_module import save_run_history, load_history

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Superintelligence Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        #chat { width: 100%; max-width: 600px; margin: auto; }
        .msg { margin: 10px 0; }
        .user { color: #0074D9; }
        .agent { color: #2ECC40; }
        #sense-btn { margin-top: 10px; background: #FFDC00; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="chat">
        <h2>Superintelligence Chatbot</h2>
        <div id="messages"></div>
        <form id="chat-form">
            <input type="text" id="user-input" autocomplete="off" style="width:80%" placeholder="Type your message..." required />
            <button type="submit">Send</button>
        </form>
        <button id="sense-btn">Activate Senses (Sight & Hearing)</button>
    </div>
    <script>
        const form = document.getElementById('chat-form');
        const input = document.getElementById('user-input');
        const messages = document.getElementById('messages');
        const senseBtn = document.getElementById('sense-btn');
        form.onsubmit = async (e) => {
            e.preventDefault();
            const userMsg = input.value;
            messages.innerHTML += `<div class='msg user'><b>You:</b> ${userMsg}</div>`;
            input.value = '';
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg })
            });
            const data = await res.json();
            messages.innerHTML += `<div class='msg agent'><b>Agent:</b> ${data.response}</div>`;
            messages.scrollTop = messages.scrollHeight;
        };
        senseBtn.onclick = async () => {
            messages.innerHTML += `<div class='msg user'><b>You:</b> [Activated Senses]</div>`;
            const res = await fetch('/sense', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ activate: true })
            });
            const data = await res.json();
            messages.innerHTML += `<div class='msg agent'><b>Agent:</b> ${data.response}</div>`;
            messages.scrollTop = messages.scrollHeight;
        };
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    memory = load_history()
    input_data = get_multimodal_input(memory=memory, user_text=user_input)
    reasoned = multimodal_reasoning(input_data)
    agent_output = agent_decision(reasoned, memory=memory)
    run_data = {"input": input_data, "reasoned": reasoned, "agent_output": agent_output}
    evolution = evolve_actions(agent_output, run_data=run_data)
    run_data["feedback"] = evolution.get("feedback")
    run_data["rating"] = evolution.get("rating")
    run_data["memory_summary"] = evolution.get("memory_summary")
    run_data["meta_reason"] = evolution.get("meta_reason")
    run_data["multi_agent_results"] = evolution.get("multi_agent_results")
    save_run_history(run_data)
    response = agent_output.get("action", "I have nothing to say.")
    meta = evolution.get('meta_reason','')
    full_response = response + (f"\n(Meta: {meta})" if meta else "")
    return jsonify({"response": full_response})

@app.route("/sense", methods=["POST"])
def sense():
    # Activate all sense plugins and return their output
    from .registry import get_plugins
    sensory_data = None
    for sense_func in get_plugins("sense"):
        sensory_data = sense_func()
    if sensory_data:
        return jsonify({"response": f"Senses activated! Sensory data: {sensory_data}"})
    else:
        return jsonify({"response": "No senses available or failed to activate."})

if __name__ == "__main__":
    print("[Superintelligence] Starting Flask server on http://0.0.0.0:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
