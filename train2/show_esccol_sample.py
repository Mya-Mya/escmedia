from pathlib import Path
import os, sys

CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
print('current dir:', CURRENT_DIR)
sys.path.append(str(CURRENT_DIR.parent))
import esccol
from click import echo, style


def show_esccol_sample():
    for number, code in enumerate(esccol.ESCCODES):
        echo('{:02d}'.format(number) + code)


if __name__ == '__main__':
    show_esccol_sample()
