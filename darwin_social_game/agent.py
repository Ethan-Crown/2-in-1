"""
Agent logic for Darwin Social Game: agents communicate and persuade using natural language.
"""
import random

class SocialAgent:
    def __init__(self, name):
        self.name = name
        self.influence = 0
        self.history = []

    def receive_question(self, question):
        # Generate a natural language argument
        argument = f"{self.name} argues: '{self.generate_argument(question)}'"
        self.history.append((question, argument))
        return argument

    def generate_argument(self, question):
        # Placeholder: random argument
        return f"On '{question}', I believe {random.choice(['yes', 'no', 'maybe', 'it depends'])}."

    def vote(self, arguments):
        # Vote for the most persuasive argument (not own)
        choices = [arg for arg in arguments if not arg.startswith(self.name)]
        if choices:
            chosen = random.choice(choices)
            return chosen
        return None
