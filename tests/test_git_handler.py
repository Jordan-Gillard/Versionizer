import os
from uuid import uuid4

import pytest
from git import Repo

from versionizer.git_handler import GitHandler


@pytest.fixture
def dummy_file_name():
    repo = Repo(search_parent_directories=True)
    dummy_file_name = str(uuid4())
    open(dummy_file_name, 'w').close()
    path_to_dummy_file = os.path.abspath(dummy_file_name)
    repo.index.add(path_to_dummy_file)
    yield dummy_file_name
    if os.path.exists(dummy_file_name):
        os.remove(dummy_file_name)
    repo.index.remove(path_to_dummy_file)


def test_dummy_file_is_destroyed_when_going_to_previous_commit(dummy_file_name):
    git_handler = GitHandler('HEAD~3')
    git_handler.stash_changes_if_necessary()
    git_handler.checkout_first_commit()
    exists = os.path.exists(dummy_file_name)
    git_handler.return_to_head()
    git_handler.pop_stash_if_needed()
    assert not exists


def test_git_handler_doesnt_delete_non_committed_changes_when_returning(dummy_file_name):
    # Return to a known previous commit
    git_handler = GitHandler('HEAD~5')
    git_handler.stash_changes_if_necessary()
    git_handler.checkout_first_commit()
    # Come back and assert that those dummy file is still there
    git_handler.return_to_head()
    git_handler.pop_stash_if_needed()
    assert os.path.exists(dummy_file_name)
