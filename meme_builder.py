from typing import Dict, List

class MemeBuilder:
    #meme_components: actual meme components
    #contributions: [user_id, their submission for the round]
    #votes: [voter_id, target_user_id (who they voted for)]
    def __init__(self, meme_components: List[str], contributions: Dict[int, str], votes: Dict[int, int]):
        self.meme_components = meme_components
        self.contributions = contributions
        self.votes = votes

    def submit_component(self, user_id: int, text: str):
        if text == "" or text.isspace():
            raise ValueError("Text cannot be empty")
        if len(text) < 3 or len(text) > 200:
            raise ValueError("Text must be between 3 and 200 characters")
        
        self.contributions[user_id] = text

    def cast_vote(self, voter_id: int, target_user_id: int):
        if voter_id == target_user_id:
            raise ValueError("You cannot vote for yourself")
        if voter_id in self.votes:
            raise ValueError("You have already voted")
        if target_user_id not in self.contributions.keys():
            raise ValueError("The user you are voting for does not exist")
        
        self.votes[voter_id] = target_user_id

    def get_current_contributions(self):
        return self.contributions

    #Get the number of votes for a specific user's contribution.
    def count_votes_for(self, contribution_user_id: int):
        return len([vote for vote in self.votes.values() if vote == contribution_user_id])

    def get_winning_component(self):
        contributors_votes: Dict[int, int] = {} #key: contribution_user_id, value: number of votes for that contribution
        for contribution_user_id in self.contributions.keys():
            contributors_votes[contribution_user_id] = self.count_votes_for(contribution_user_id)

        max_votes = max(contributors_votes.values())
        if max_votes == 0 and len(contributors_votes) != 1:
            return None
        user_ids_with_max_votes = [key for key in contributors_votes if contributors_votes[key] == max_votes]
        
        if len(user_ids_with_max_votes) != 1:
            return None

        return self.contributions.get(user_ids_with_max_votes[0])

    def finalize_round(self):
        pass

    def get_meme(self):
        pass

    def is_meme_complete(self):
        pass