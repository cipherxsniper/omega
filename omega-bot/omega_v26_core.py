from omega_v26_node_scan import scan_all_nodes
from omega_v26_agents import Agent
from omega_v26_consensus import ConsensusEngine
from omega_v26_memory import SharedMemory

class OmegaV26:

    def __init__(self):

        self.nodes = scan_all_nodes()
        self.agents = [Agent(n["name"]) for n in self.nodes]

        self.consensus = ConsensusEngine()
        self.memory = SharedMemory()

    def tick(self, input_text):

        proposals = []

        # distribute thought across agents
        for agent in self.agents[:5]:

            analysis = agent.analyze(input_text)
            proposal = agent.propose_change(analysis)

            proposals.append(proposal)

            self.consensus.vote(agent.name, proposal["proposal"])

        # consensus step
        decisions = {}

        for p in proposals:
            decisions[p["proposal"]] = self.consensus.decide(p["proposal"])

        # update memory
        self.memory.update_belief("last_input", input_text)

        return {
            "nodes": len(self.nodes),
            "agents": len(self.agents),
            "decisions": decisions,
            "memory_size": len(self.memory.history)
        }
