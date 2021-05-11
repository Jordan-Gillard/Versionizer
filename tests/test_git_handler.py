import os
from uuid import uuid4

import pytest

from versionizer.git_handler import GitHandler


@pytest.fixture
def dummy_file():
    dummy_file_name = str(uuid4())
    f = open(dummy_file_name, 'w')
    yield dummy_file_name
    f.close()
    os.remove(dummy_file_name)


@pytest.fixture
def git_handler():
    """
    By using this fixture and yielding the GitHander, we are guaranteed to return
    to the commit we were on even if tests fail. When tests fail, the code after the
    yield block is guaranteed to run. This keeps us from getting the user stuck on
    a previous commit.
    """
    git_handler = GitHandler('HEAD~3')
    git_handler.checkout_first_commit()
    yield git_handler
    git_handler.return_to_head()


def test_dummy_file_is_destroyed_when_going_to_previous_commit():
    dummy_file_name = str(uuid4())
    f = open(dummy_file_name, 'w')
    f.close()
    git_handler = GitHandler('HEAD~3')
    git_handler.checkout_first_commit()
    exists = os.path.exists(dummy_file_name)
    git_handler.return_to_head()
    if exists:
        os.remove(dummy_file_name)
    assert not exists


def test_git_handler_doesnt_delete_non_committed_changes_when_returning(dummy_file):
    # Return to a known previous commit
    git_handler = GitHandler('HEAD~5')
    git_handler.checkout_first_commit()
    # Come back and assert that those dummy file is still there
    git_handler.return_to_head()
    assert os.path.exists(dummy_file)
