"""
Game logic for Darwin Social Game: manages rounds, questions, and agent interactions.
Now delegates learning/perception to orchestrator plugins (DGM, VITA, etc.).
Optimized for performance, clarity, and extensibility.
"""
from .agent import SocialAgent
import random

class SocialGame:
    def __init__(self, agent_names, questions, orchestrator=None):
        self.agents = [SocialAgent(name) for name in agent_names]
        self.questions = questions
        self.round = 0
        self.history = []
        self.orchestrator = orchestrator

    def play_round(self):
        if not self.agents:
            return {"error": "No agents left."}
        question = random.choice(self.questions)
        # Use orchestrator for perception (VITA) if available
        if self.orchestrator and hasattr(self.orchestrator, 'perceive'):
            perceptions = [self.orchestrator.perceive(agent, question) for agent in self.agents]
        else:
            perceptions = [agent.receive_question(question) for agent in self.agents]
        # Use orchestrator for learning (DGM) if available
        if self.orchestrator and hasattr(self.orchestrator, 'learn'):
            for agent, perception in zip(self.agents, perceptions):
                self.orchestrator.learn(agent, perception)
        arguments = perceptions
        votes = {agent.name: agent.vote(arguments) for agent in self.agents}
        # Tally influence efficiently
        influence_map = {agent.name: 0 for agent in self.agents}
        for voted in votes.values():
            if voted:
                for agent in self.agents:
                    if voted.startswith(agent.name):
                        influence_map[agent.name] += 1
        for agent in self.agents:
            agent.influence += influence_map[agent.name]
        self.round += 1
        # Elimination and reproduction logic
        influences = [agent.influence for agent in self.agents]
        min_votes = min(influences)
        max_votes = max(influences)
        eliminated = [agent for agent in self.agents if agent.influence == min_votes]
        top_agents = [agent for agent in self.agents if agent.influence == max_votes]
        # Remove eliminated agents safely
        eliminated_names = set(a.name for a in eliminated)
        self.agents = [agent for agent in self.agents if agent.name not in eliminated_names]
        # Reproduce: each top agent produces len(eliminated) offspring
        offspring = []
        if top_agents and eliminated:
            for parent1 in top_agents:
                for _ in range(len(eliminated)):
                    parent2 = random.choice(top_agents)
                    child_name = f"{parent1.name}-{parent2.name}-child{random.randint(1000,9999)}"
                    child = SocialAgent(child_name)
                    # Combine characteristics (for now, just average influence)
                    child.influence = int((parent1.influence + parent2.influence) / 2)
                    offspring.append(child)
            self.agents.extend(offspring)
        self.history.append({
            'question': question,
            'arguments': arguments,
            'votes': votes,
            'influence': {a.name: a.influence for a in self.agents},
            'eliminated': [a.name for a in eliminated],
            'offspring': [c.name for c in offspring]
        })
        return self.history[-1]
