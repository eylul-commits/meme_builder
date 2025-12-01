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
