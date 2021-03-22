from click import echo, style
from time import time
import esccol
from typing import List
import random
import sys


class EsccolMapRenderer:
    def __init__(self):
        self._buffer = None

    def prepare(self, esccol_number_map: List[List[int]]):
        esccodes_map = []
        for row in esccol_number_map:
            esccodes_in_row = ''.join([esccol.ESCCODES[number] for number in row])
            esccodes_map.append(esccodes_in_row)
        self._buffer = '\n'.join(esccodes_map)

    def render(self):
        if self._buffer is None:
            raise ValueError('バッファがまだ作られていない')
        echo(self._buffer)


def main(esccol_number_map=None):
    esccol_number_map = esccol_number_map or [random.choices(range(14), k=50) for _ in range(50)]
    renderer = EsccolMapRenderer()
    renderer.prepare(esccol_number_map)
    renderer.render()


if __name__ == '__main__':
    main()
