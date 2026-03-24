# Quadratic Voting Implementation with Conviction Scaling
from typing import Dict, List
from decimal import Decimal
from datetime import datetime, timedelta

class QuadraticVoting:
    def __init__(self):
        self.votes: Dict[str, Dict] = {}
        self.proposals: Dict[str, Dict] = {}
        
    def create_proposal(self, proposal_id: str, title: str, description: str, 
                        voting_period_days: int) -> bool:
        if proposal_id in self.proposals:
            return False
            
        self.proposals[proposal_id] = {
            'title': title,
            'description': description,
            'created_at': datetime.now(),
            'ends_at': datetime.now() + timedelta(days=voting_period_days),
            'votes_for': Decimal('0'),
            'votes_against': Decimal('0')
        }
        return True

    def cast_vote(self, voter_id: str, proposal_id: str, 
                  token_amount: Decimal, conviction_time_days: int, 
                  vote_direction: bool) -> bool:
        if proposal_id not in self.proposals:
            return False
            
        if datetime.now() > self.proposals[proposal_id]['ends_at']:
            return False

        # Calculate quadratic voting power
        voting_power = Decimal(token_amount).sqrt()
        
        # Apply conviction scaling (more conviction time = more voting power)
        conviction_multiplier = Decimal(1 + (conviction_time_days / 365))
        final_voting_power = voting_power * conviction_multiplier

        # Record the vote
        if voter_id not in self.votes:
            self.votes[voter_id] = {}
            
        self.votes[voter_id][proposal_id] = {
            'amount': token_amount,
            'power': final_voting_power,
            'conviction_time': conviction_time_days,
            'vote_direction': vote_direction,
            'timestamp': datetime.now()
        }

        # Update proposal vote tallies
        if vote_direction:
            self.proposals[proposal_id]['votes_for'] += final_voting_power
        else:
            self.proposals[proposal_id]['votes_against'] += final_voting_power

        return True

    def get_proposal_result(self, proposal_id: str) -> Dict:
        if proposal_id not in self.proposals:
            raise ValueError('Proposal not found')
            
        proposal = self.proposals[proposal_id]
        total_votes = proposal['votes_for'] + proposal['votes_against']
        
        if total_votes == Decimal('0'):
            approval_percentage = Decimal('0')
        else:
            approval_percentage = (proposal['votes_for'] / total_votes) * 100

        return {
            'proposal_id': proposal_id,
            'total_votes': total_votes,
            'votes_for': proposal['votes_for'],
            'votes_against': proposal['votes_against'],
            'approval_percentage': approval_percentage,
            'ended': datetime.now() > proposal['ends_at']
        }

    def get_voter_power(self, voter_id: str) -> Dict[str, Decimal]:
        if voter_id not in self.votes:
            return {}
            
        return {prop_id: vote['power'] 
                for prop_id, vote in self.votes[voter_id].items()}
