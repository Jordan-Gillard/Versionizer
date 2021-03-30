import contextlib
import io
import sys

from asciistuff import Banner, Lolcat


@contextlib.contextmanager
def no_stdout():
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout


def print_banner():
    print(Lolcat(Banner("Versionizer")))
