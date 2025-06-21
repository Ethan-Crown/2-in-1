from superintelligence.registry import register
from darwin_social_game.game import SocialGame
from superintelligence.registry import get_plugins

AGENT_NAMES = ["Alice", "Bob", "Carol", "Dave"]
QUESTIONS = [
    "Should AI have rights?",
    "Is democracy the best system?",
    "Can machines be creative?",
    "Is persuasion ethical?"
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

game = SocialGame(AGENT_NAMES, QUESTIONS, orchestrator=orchestrator)

def run_social_game():
    print("[DarwinSocialGame] Playing a round...")
    round_data = game.play_round()
    return round_data

register("autonomy", run_social_game)
