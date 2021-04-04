#!/bin/env python3

from pathlib import Path
import os

import click


def update_file(src: Path, dst: Path):
    error_code = os.system(f'sudo cp {src} {dst}') >> 8
    return error_code


@click.command()
@click.option('--force', '-f', is_flag=True, help="Overwrite existing files")
def install(force):
    for path in Path('.').glob('*.py'):
        src = path.resolve()
        dst = Path('/usr/local/bin') / path.stem
        if dst.exists():
            if dst.is_file():
                print(f'Warning! Target "{dst}" already exists... comparing.')
                error_code = os.system(f'diff {src} {dst}') >> 8
                if error_code == 0:
                    print('Identical. File is already installed!')
                else:
                    if force:
                        print(f'Force overwrite target: {dst}')
                        update_file(src, dst)
                    else:
                        print('Differing -- possibly out of date. Pass -f to overwrite.')
            else:
                print(f'Warning! Non-file in target destination. Skipping install of {path}')
        else:
            update_file(src, dst)


if __name__ == '__main__':
    install()