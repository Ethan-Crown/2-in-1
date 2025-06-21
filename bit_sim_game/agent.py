"""
8-bit simulation agent: controls an 8-bit body, can flash (vision) or whistle (audio), and answers questions.
"""
import random
import string

class BitAgent:
    def __init__(self, name, bits=None, x=None, y=None):
        self.name = name
        self.bits = bits if bits is not None else [random.randint(0,1) for _ in range(8)]
        self.score = 0
        self.history = []
        # 2D position
        self.x = x if x is not None else random.randint(0,19)
        self.y = y if y is not None else random.randint(0,19)
        self.color = f"#{random.randint(0,0xFFFFFF):06x}"
        self.target = None  # (x, y) target for movement

    def set_target(self, x, y):
        self.target = (x, y)

    def move(self, grid_size=20):
        # Move toward target if set, else stay
        if self.target:
            dx = self.target[0] - self.x
            dy = self.target[1] - self.y
            if dx != 0:
                self.x += 1 if dx > 0 else -1
            elif dy != 0:
                self.y += 1 if dy > 0 else -1
            # Clamp to grid
            self.x = max(0, min(grid_size-1, self.x))
            self.y = max(0, min(grid_size-1, self.y))
            # If reached target, clear it
            if (self.x, self.y) == self.target:
                self.target = None

    def communicate(self, mode):
        # mode: 'vision' or 'audio'
        if mode == 'vision':
            return f"{self.name} flashes: {random.choice(['on','off'])}"
        elif mode == 'audio':
            return f"{self.name} whistles: {random.choice(['high','low'])}"
        return ""

    def answer_question(self, question):
        # Generate a random 8-bit answer
        answer = ''.join(str(random.randint(0,1)) for _ in range(8))
        self.history.append((question, answer))
        return answer

    def rate_answers(self, answers):
        # Rate all answers except own, 1-10
        ratings = {}
        for name, ans in answers.items():
            if name != self.name:
                ratings[name] = random.randint(1,10)
        return ratings

    @staticmethod
    def blend(parent1, parent2):
        # Blend names and bits
        name = parent1.name[:4] + parent2.name[-4:]
        bits = [(b1 if random.random()<0.5 else b2) for b1, b2 in zip(parent1.bits, parent2.bits)]
        return BitAgent(name, bits)
