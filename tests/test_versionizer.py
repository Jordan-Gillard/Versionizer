# TODO: You will need to use GitPython to create new commits and functions
#  between these temporary commits. They _must_ be removed to not dirty the
#  users Git history.
from versionizer.versionizer import Versionizer


def test_versionizer_run_on_file():
    # TODO make some temp commits and test this shit
    v = Versionizer(
        project_path="assets",
        module="file1.py",
        first_commit="71a8c2089e01ddcf334a662898f07c56b7a12255"
    )
    v.run()


def test_versionizer_run_on_directory():
    pass
