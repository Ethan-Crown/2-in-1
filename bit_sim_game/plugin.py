from superintelligence.registry import register, get_plugins
from bit_sim_game.game import BitSimGame

AGENT_NAMES = [f"Agent{i}" for i in range(1, 11)]
QUESTIONS = [
    "What is the meaning of 8 bits?",
    "How would you solve a maze?",
    "What is the best pattern for flashing?",
    "How do you cooperate with others?"
]
# Use orchestrator from superintelligence if available
try:
    from superintelligence.main import Orchestrator
    orchestrator_plugins = {
        'vita': get_plugins('sense')[0] if get_plugins('sense') else None,
        'dgm': get_plugins('learn')[0] if get_plugins('learn') else None
    }
    orchestrator = Orchestrator(vita_plugin=orchestrator_plugins['vita'], dgm_plugin=orchestrator_plugins['dgm'])
except Exception:
    orchestrator = None

game = BitSimGame(AGENT_NAMES, QUESTIONS)

def run_bit_sim_game():
    print("[BitSimGame] Playing a round...")
    round_data = game.ask_question()
    return round_data

register("autonomy", run_bit_sim_game)
