from typing import Dict, List, Optional


class MemeBuilder:
    def __init__(self, meme_components: List[str], contributions: Dict[str, str], votes: Dict[str, str]):
        self.meme_components = meme_components
        self.contributions = contributions
        self.votes = votes

    def submit_component(self, user_id: str, text: str):
        pass

    def cast_vote(self, voter_id: str, target_user_id: str):
        pass

    def get_current_contributions(self):
        pass

    def get_winner(self):
        pass

    def finalize_round(self):
        pass

    def get_meme(self):
        pass

    def is_meme_complete(self):
        pass