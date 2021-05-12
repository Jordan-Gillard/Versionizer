from typing import Optional

from git import Commit, Repo


class GitHandler:
    def __init__(self, first_commit: str,
                 second_commit: Optional[str] = None,
                 git_repo: Optional[str] = None):
        if git_repo:
            self.repo: Repo = Repo(git_repo)
        else:
            self.repo: Repo = Repo(search_parent_directories=True)
        self.master: Commit = self.repo.head.reference
        self.first_commit: Commit = self.repo.commit(first_commit)
        if second_commit:
            self.second_commit: Commit = self.repo.commit(second_commit)
        else:
            self.second_commit = self.master
        self.was_dirty = False

    def _checkout_commit(self, commit: Commit):
        # TODO: If there are unsaved changes in the current working tree, we should
        #  stash these changes and then get them back when we eventually return to
        #  the head.
        self.repo.head.reference = commit
        self.revert_all_changes()

    def checkout_first_commit(self):
        self._checkout_commit(self.first_commit)

    def checkout_second_commit(self):
        self._checkout_commit(self.second_commit)

    def return_to_head(self):
        self._checkout_commit(self.master)

    def stash_changes_if_necessary(self):
        if self.repo.is_dirty():
            self.was_dirty = True
            self.repo.git.stash("save")

    def pop_stash_if_needed(self):
        if self.was_dirty:
            self.repo.git.stash("pop")

    def revert_all_changes(self):
        self.repo.head.reset(index=True, working_tree=True)
