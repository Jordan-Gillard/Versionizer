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


def test_git_handler_doesnt_delete_non_committed_changes_when_returning(dummy_file):
    # Return to a known previous commit
    git_handler = GitHandler('HEAD~1')
    git_handler.checkout_first_commit()
    # Come back and assert that those dummy file is still there
    git_handler.return_to_head()
    assert os.path.exists(dummy_file)
