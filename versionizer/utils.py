import contextlib
import io
import sys

from asciistuff import Banner, Lolcat
from colorama import Fore, Style


@contextlib.contextmanager
def no_stdout():
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout


def print_banner():
    print(Lolcat(Banner("Versionizer", font='bubble'), spread=0.5))


def print_bright_blue(message):
    print(Style.BRIGHT + Fore.BLUE + message)
    print(Style.RESET_ALL)
