from git import repo


class GitHandler:
    def __init__(self, first_commit, second_commit, file):
        self.first_commit = first_commit
        self.second_commit = second_commit
        self.file = file

    def checkout_first_commit(self):
        pass
        # past_branch = repo.create_head('commit_1', 'HEAD~10')

    def get_ast_for_first_commit(self):
        pass

    def get_ast_for_second_commit(self):
        pass

    def return_to_head(self):
        pass