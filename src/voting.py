import math

class VotingProtocol:
    def __init__(self, num_voters, num_proposals):
        self.num_voters = num_voters
        self.num_proposals = num_proposals
        self.voter_credits = [100 for _ in range(num_voters)]
        self.votes = [[0 for _ in range(num_proposals)] for _ in range(num_voters)]

    def cast_vote(self, voter_id, proposal_id, vote_amount):
        if vote_amount > self.voter_credits[voter_id]:
            raise ValueError(f'Voter {voter_id} does not have enough credits to cast a vote of {vote_amount}')
        self.votes[voter_id][proposal_id] += vote_amount
        self.voter_credits[voter_id] -= vote_amount

    def tally_votes(self):
        proposal_scores = [0 for _ in range(self.num_proposals)]
        for voter_id in range(self.num_voters):
            for proposal_id in range(self.num_proposals):
                proposal_scores[proposal_id] += math.sqrt(self.votes[voter_id][proposal_id])
        return proposal_scores

    def reset_votes(self):
        self.voter_credits = [100 for _ in range(self.num_voters)]
        self.votes = [[0 for _ in range(self.num_proposals)] for _ in range(self.num_voters)]
