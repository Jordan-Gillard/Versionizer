# TODO: You will need to use GitPython to create new commits and functions
#  between these temporary commits. They _must_ be removed to not dirty the
#  users Git history.
import os

from versionizer.versionizer import Versionizer


def test_versionizer_run_on_file():
    v = Versionizer(
        project_path="assets",
        module="file1.py",
        first_commit="ee20881e206f6976e5482bdf97772e5598e545a8"
    )
    initial_len = len(os.listdir("assets/"))
    v.run()
    after_len = len(os.listdir("assets/"))
    assert after_len - initial_len == 2


def test_versionizer_run_on_directory():
    pass
