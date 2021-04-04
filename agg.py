#!/bin/env python3
from pathlib import Path
from typing import List, Callable, TextIO

import click


class LineData:
    value: str = ''
    desc: str = ''
    date: str = ''
    line: str = ''

    # token 0 = value
    def token_value(self, buffer: str):
        self.value = buffer

    # token 1 = desc
    def token_desc(self, buffer: str):
        self.desc = buffer

    # token 2 = date (not implemented)
    def token_date(self, buffer: str):
        self.date = buffer

    # syntax we're parsing is token0:[token1[:token2]]...
    token_index_map: List[Callable] = [token_value, token_desc, token_date]

    def __init__(self, line):
        self.line = line
        self.handle_line()

    def handle_token(self, token_id: int, buffer: str):
        self.token_index_map[token_id](self, buffer)
        # new token value
        new_token = token_id
        if new_token < 2:
            new_token += 1
        # buffer is set to blank string
        return new_token, ''

    def handle_line(self):
        self.line = self.line.strip()
        if len(self.line) == 0:
            return None
        if self.line[0] == '#':
            return None

        buffer: str = ''
        is_in_quotes: bool = False
        token_id: int = 0

        for c in self.line:
            if c == '"' or c == '\'':
                is_in_quotes = True
            else:
                if not is_in_quotes:
                    if c == ':':
                        token_id, buffer = self.handle_token(token_id, buffer)
                buffer += c
        return


class AggParser:
    _aggregate = 0

    def __init__(self, f: TextIO):
        self.parse(f)

    def parse(self, f: TextIO):
        for i, line in enumerate(f.readlines()):
            line_data = LineData(line)
            if line_data is not None:
                if line_data.value:
                    try:
                        self._aggregate += float(line_data.value)
                    except ValueError:
                        print(f'Warning: could not parse line #{i}: "{line}"')

    def get_aggregate(self):
        return self._aggregate


@click.command()
@click.argument('file_path')
def agg(file_path):
    path = Path(file_path)
    f: TextIO
    with path.open('r') as f:
        agg_parser = AggParser(f)
        print(f"Aggregate: {agg_parser.get_aggregate()}")


if __name__ == '__main__':
    agg()
