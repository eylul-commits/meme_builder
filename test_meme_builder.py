import pytest

from meme_builder import MemeBuilder

# i will use this order: assert actual == expected
class TestMemeBuilder:
    def setup_method(self):
        self.builder = MemeBuilder([], {}, {})

    def test_submit_valid_component(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        assert self.builder.contributions[1] == "AI generated memes be like:"

    def test_submit_valid_component_with_different_users(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")

        assert self.builder.contributions[1] == "AI generated memes be like:"
        assert self.builder.contributions[2] == "Human generated memes be like:"

    def test_submit_component_at_minimum_length(self):
        self.builder.submit_component(1, "e!!")
        assert self.builder.contributions[1] == "e!!"

    def test_submit_component_at_maximum_length(self):
        self.builder.submit_component(1, "When you open the project just to fix one little thing and suddenly you're refactoring half the codebase wondering how life brought you here and why future you will hate you for this exact moment!!!!!")
        assert self.builder.contributions[1] == "When you open the project just to fix one little thing and suddenly you're refactoring half the codebase wondering how life brought you here and why future you will hate you for this exact moment!!!!!"

    def test_submit_component_with_all_caps(self):
        self.builder.submit_component(1, "WHEN YOU FINALLY FIX THE BUG")
        assert self.builder.contributions[1] == "WHEN YOU FINALLY FIX THE BUG"

    def test_submit_empty_component_rejected(self):
        with pytest.raises(ValueError) as err:
            self.builder.submit_component(1, "")

        assert str(err.value) == "Text cannot be empty"

    def test_submit_component_with_only_whitespace_rejected(self):
        with pytest.raises(ValueError) as err:
            self.builder.submit_component(1, " ")

        assert str(err.value) == "Text cannot be empty"

    def test_submit_component_too_short(self):
        with pytest.raises(ValueError) as err:
            self.builder.submit_component(1, "e!")
        
        assert str(err.value) == "Text must be between 3 and 200 characters"

    def test_submit_component_replaces_previous(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(1, "AI generated memes be like: (updated)")
        assert self.builder.contributions[1] == "AI generated memes be like: (updated)"

    def test_vote_for_existing_contribution(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        assert self.builder.votes[1] == 2

    def test_vote_for_own_submission_rejected(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        with pytest.raises(ValueError) as err:
            self.builder.cast_vote(1, 1)
        assert str(err.value) == "You cannot vote for yourself"

    def test_vote_twice_rejected(self):
        self.builder.submit_component(2, "Intern said 'it worked locally' before nuking prod")
        self.builder.submit_component(3, "My code works but I have no idea why")
        self.builder.cast_vote(1, 2)

        with pytest.raises(ValueError) as err:
            self.builder.cast_vote(1, 3)

        assert str(err.value) == "You have already voted"

    def test_vote_for_nonexistent_user(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        with pytest.raises(ValueError) as err:
            self.builder.cast_vote(1, 2)
        assert str(err.value) == "The user you are voting for does not exist"

    def test_get_current_contributions(self):
        #not sure if i should test this since it's just a getter method
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        assert self.builder.get_current_contributions() == {1: "AI generated memes be like:", 2: "Human generated memes be like:"}

    def test_count_votes_for(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(3, 2)
        assert self.builder.count_votes_for(2) == 2

    def test_count_votes_for_nonexistent_user(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        assert self.builder.count_votes_for(3) == 0
    
    def test_get_winner_clear_majority(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(3, 2)
        assert self.builder.get_winning_component() == "Human generated memes be like:"

    def test_get_winner_returns_none_on_tie(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(2, 1)
        assert self.builder.get_winning_component() is None

    def test_get_winner_three_way_tie(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.submit_component(3, "Cat generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(2, 1)
        self.builder.cast_vote(4, 3)
        assert self.builder.get_winning_component() is None
    
    def test_get_winner_no_votes(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        assert self.builder.get_winning_component() is None

    def test_single_contribution_can_win(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        assert self.builder.get_winning_component() == "AI generated memes be like:"

    def test_finalize_adds_winner_to_meme(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(3, 2)
        assert self.builder.finalize_round() is True
        assert self.builder.meme_components == ["Human generated memes be like:"]

    def test_finalize_with_tie_returns_false(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(2, 1)
        assert self.builder.finalize_round() is False

    def test_finalize_clears_round_state(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(3, 2)
        self.builder.finalize_round()
        assert self.builder.contributions == {}
        assert self.builder.votes == {}

    def test_finalize_preserves_meme_history(self):
        #No need for casting votes since if we have one contribution, it will win by default. i already tested this in test_single_contribution_can_win
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(2, "Cat generated memes be like:")
        self.builder.finalize_round()
        assert self.builder.meme_components == ["AI generated memes be like:", "Cat generated memes be like:"]
    
    def test_finalize_tie_does_not_add_to_meme(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.cast_vote(1, 2)
        self.builder.cast_vote(2, 1)

        result = self.builder.finalize_round()

        assert result is False
        assert self.builder.meme_components == []
        assert len(self.builder.contributions) != 0
        assert len(self.builder.votes) != 0
    
    def test_is_meme_complete_with_three_components(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(3, "Cat generated memes be like:")
        self.builder.finalize_round()
        assert self.builder.is_meme_complete() is True
        assert self.builder.meme_components == ["AI generated memes be like:", "Human generated memes be like:", "Cat generated memes be like:"]

    def test_is_meme_complete_with_two_components(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.finalize_round()
        assert self.builder.is_meme_complete() is False

    def test_is_meme_complete_with_four_components(self):
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(3, "Cat generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(4, "Dog generated memes be like:")
        self.builder.finalize_round()
        assert self.builder.is_meme_complete() is False

    def test_get_meme(self):
        #not sure if i should test this since it's just a getter method
        self.builder.submit_component(1, "AI generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(2, "Human generated memes be like:")
        self.builder.finalize_round()
        self.builder.submit_component(3, "Cat generated memes be like:")
        self.builder.finalize_round()
        assert self.builder.get_meme() == ["AI generated memes be like:", "Human generated memes be like:", "Cat generated memes be like:"]