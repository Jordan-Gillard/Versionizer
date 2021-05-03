from typing import Optional

from git import Commit, Repo


class GitHandler:
    def __init__(self, file: str, first_commit: str, second_commit: Optional[str] = None):
        self.repo = Repo(search_parent_directories=True)
        self.master: Commit = self.repo.head.reference
        self.first_commit: Commit = self.repo.commit(first_commit)
        if second_commit:
            self.second_commit: Commit = self.repo.commit(second_commit)
        else:
            self.second_commit = self.master
        self.file = file

    def _checkout_commit(self, commit: Commit):
        self.repo.head.reference = commit
        self.repo.head.reset(index=True, working_tree=True)

    def checkout_first_commit(self):
        self._checkout_commit(self.first_commit)

    def checkout_second_commit(self):
        self._checkout_commit(self.second_commit)

    def get_ast_for_first_commit(self):
        pass

    def get_ast_for_second_commit(self):
        pass

    def return_to_head(self):
        self.repo.head.reference = self.master
        self.repo.head.reset(index=True, working_tree=True)
