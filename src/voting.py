import os
import json
from collections import defaultdict
from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey

class Vote:
    def __init__(self, voter_id, candidate_id, signature):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.signature = signature

class VotingSystem:
    def __init__(self):
        self.votes = defaultdict(list)
        self.private_keys = {}
        self.public_keys = {}

    def register_voter(self, voter_id, private_key, public_key):
        self.private_keys[voter_id] = SigningKey.from_string(bytes.fromhex(private_key))
        self.public_keys[voter_id] = VerifyingKey.from_string(bytes.fromhex(public_key))

    def cast_vote(self, voter_id, candidate_id):
        private_key = self.private_keys[voter_id]
        signature = private_key.sign(f'{voter_id}:{candidate_id}'.encode())
        vote = Vote(voter_id, candidate_id, signature.hex())
        self.votes[candidate_id].append(vote)
        return vote

    def verify_vote(self, vote):
        public_key = self.public_keys[vote.voter_id]
        try:
            public_key.verify(bytes.fromhex(vote.signature), f'{vote.voter_id}:{vote.candidate_id}'.encode())
            return True
        except:
            return False

    def get_results(self):
        results = {}
        for candidate_id, votes in self.votes.items():
            valid_votes = [vote for vote in votes if self.verify_vote(vote)]
            results[candidate_id] = len(valid_votes)
        return results

if __name__ == '__main__':
    voting_system = VotingSystem()

    # Register voters
    voting_system.register_voter('voter1', '18e2e0b0d589378bc1b4c369b8b9dd1a0b7e8d8f88c78a64d51c41d3a1b44d01', '04a5b8e5f2b1d8c712d7a0a1f5b0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8')
    voting_system.register_voter('voter2', '8c7b6a5d4c3b2a1f0e9d8c7b6a5d4', '043b2a1f0e9d8c7b6a5d4c3b2a1f0e9d8c7b6a5d4c3b2a1f0e9d8c7b6a5d4')

    # Cast votes
    vote1 = voting_system.cast_vote('voter1', 'candidate1')
    vote2 = voting_system.cast_vote('voter2', 'candidate2')

    # Verify votes
    print(voting_system.verify_vote(vote1))  # True
    print(voting_system.verify_vote(vote2))  # True

    # Get results
    print(voting_system.get_results())  # {'candidate1': 1, 'candidate2': 1}