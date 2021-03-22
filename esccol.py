from click import echo, style, termui
import csv
from typing import List
from dataclasses import dataclass

echo(style('コンソール画面の背景は白くすること'))
NAMES = [
    'black', 'white',
    'red', 'green', 'yellow', 'blue', 'magenta', 'cyan',
    'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan',
]
name2text = {name: style('■', fg=name) for name in NAMES}
number2text = {number: name2text[NAMES[number]] for number in range(len(NAMES))}


def ansi_block_esccode(color_name: str) -> str:
    return style('■', fg=color_name)


ESCCODES = [
    ansi_block_esccode('black'),
    ansi_block_esccode('white'),
    '　',
    ansi_block_esccode('red'),
    ansi_block_esccode('green'),
    ansi_block_esccode('yellow'),
    ansi_block_esccode('blue'),
    ansi_block_esccode('magenta'),
    ansi_block_esccode('cyan'),
    ansi_block_esccode('bright_red'),
    ansi_block_esccode('bright_green'),
    ansi_block_esccode('bright_yellow'),
    ansi_block_esccode('bright_blue'),
    ansi_block_esccode('bright_magenta'),
    ansi_block_esccode('bright_cyan'),
]


@dataclass
class EsccolRecord:
    pass


@dataclass
class HSVEsccolRecord(EsccolRecord):
    h: float
    s: float
    v: float
    esccol_number: int


@dataclass
class RGBEsccolRecord(EsccolRecord):
    r: float
    g: float
    b: float
    esccol_number: int


class EsccolDataSet:
    def __init__(self, records: List[EsccolRecord] = []):
        self.records: List[EsccolRecord] = records

    @staticmethod
    def load_hsv(fp):
        db = EsccolDataSet()
        with open(fp, 'r', encoding='utf-8')as file:
            reader = csv.reader(file)
            for h, s, v, esccol_number in reader:
                record = HSVEsccolRecord(h=float(h), s=float(s), v=float(v), esccol_number=esccol_number)
                db.append(record)
        return db

    def save_hsv(self, fp):
        with open(fp, 'w', encoding='utf-8', newline='')as file:
            writer = csv.writer(file)
            for record in self.records:
                writer.writerow([record.h, record.s, record.v, record.esccol_number])

    def append(self, record: EsccolRecord):
        self.records.append(record)
