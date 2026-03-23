import os
import sys
import time
import random
from typing import List, Dict
from .governance import GovernanceEngine
from .agents import AgentManager
from .policy import PolicyManager

class DeGovNode:
    def __init__(self, config: Dict):
        self.agent_manager = AgentManager(config['agents'])
        self.policy_manager = PolicyManager(config['policies'])
        self.governance_engine = GovernanceEngine(config['governance'])

    def run(self):
        while True:
            self.agent_manager.update_agents()
            self.policy_manager.enforce_policies()
            self.governance_engine.process_proposals()
            time.sleep(random.uniform(1, 5))