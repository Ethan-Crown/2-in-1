"""
8-bit simulation game logic: manages agents, communication, questions, scoring, elimination, and reproduction.
"""
from .agent import BitAgent
import random

class BitSimGame:
    def __init__(self, agent_names, questions, grid_size=20):
        self.grid_size = grid_size
        self.agents = [BitAgent(name) for name in agent_names]
        self.questions = questions
        self.round = 0
        self.history = []

    def proximity_chat(self):
        # Each agent communicates visually and audibly
        comms = []
        for agent in self.agents:
            comms.append(agent.communicate('vision'))
            comms.append(agent.communicate('audio'))
        return comms

    def step(self):
        # Move all agents (each agent controls its own movement)
        for agent in self.agents:
            agent.move(self.grid_size)
        # Prevent overlap (simple physics: push apart)
        positions = {}
        for agent in self.agents:
            pos = (agent.x, agent.y)
            while pos in positions:
                agent.move(self.grid_size)
                pos = (agent.x, agent.y)
            positions[pos] = agent.name
        return positions

    def ask_question(self):
        self.step()  # Move before question
        question = random.choice(self.questions)
        answers = {agent.name: agent.answer_question(question) for agent in self.agents}
        ratings = {agent.name: agent.rate_answers(answers) for agent in self.agents}
        # Tally scores
        for agent in self.agents:
            agent.score = sum(r[agent.name] for r in ratings.values() if agent.name in r)
        self.round += 1
        # Elimination and reproduction
        sorted_agents = sorted(self.agents, key=lambda a: a.score)
        eliminated = sorted_agents[:5]
        survivors = sorted_agents[5:]
        top_scorers = sorted(survivors, key=lambda a: a.score, reverse=True)[:2]
        # Remove eliminated
        for agent in eliminated:
            self.agents.remove(agent)
        # Reproduce: top scorers blend to create as many as eliminated, up to 10 total
        offspring = []
        while len(self.agents) + len(offspring) < 10 and len(offspring) < len(eliminated):
            parent1, parent2 = random.sample(top_scorers, 2)
            child = BitAgent.blend(parent1, parent2)
            offspring.append(child)
        self.agents.extend(offspring)
        self.history.append({
            'question': question,
            'answers': answers,
            'ratings': ratings,
            'scores': {a.name: a.score for a in self.agents},
            'eliminated': [a.name for a in eliminated],
            'offspring': [c.name for c in offspring],
            'comms': self.proximity_chat()
        })
        # Add agent positions to history
        self.history[-1]['positions'] = {a.name: (a.x, a.y, a.color) for a in self.agents}
        return self.history[-1]
