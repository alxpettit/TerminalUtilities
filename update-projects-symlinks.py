#!/bin/env python3
from os import getenv
from pathlib import Path
from typing import List, TextIO

import click

home = Path(getenv('HOME')).resolve()
projects_symlink_dir = home / 'Projects'
desktop_dir = home / 'Desktop'


@click.command()
@click.option('--create-desktop-link', '-c', is_flag=True,
              help='Create a desktop symlink pointing to the Projects directory')
@click.option('--no-hide-dirs', '-n', is_flag=True,
              help='Skip hiding the various projects directories.')
def build_projects_symlink_dir(create_desktop_link, no_hide_dirs):
    try:
        projects_symlink_dir.mkdir(parents=True)
        print('"Projects" dir created.')
    except FileExistsError:
        print('Projects dir confirmed to exist.')

    subdirectory_names: List[str] = []

    for subdirectory_of_home in home.iterdir():
        if subdirectory_of_home.stem != 'Projects' and 'Projects' in subdirectory_of_home.stem:
            subdirectory_names += [subdirectory_of_home.stem]
            target = projects_symlink_dir / subdirectory_of_home.stem.replace('Projects', '')
            try:
                target.symlink_to(subdirectory_of_home)
                print(f'{target} -> {subdirectory_of_home}')
            except FileExistsError:
                print(f'Symlink "{target}" already exists.')

    if create_desktop_link:
        try:
            (desktop_dir / 'Projects').symlink_to(projects_symlink_dir)
        except FileExistsError:
            print(f'Desktop symlink already exists.')

    if not no_hide_dirs:
        dot_hidden = DotHidden(home / '.hidden')
        for name in subdirectory_names:
            dot_hidden.add(name)


class DotHidden:
    lines: List[str] = []
    f_handle: TextIO

    def __init__(self, path: Path):
        if path.is_file():
            self.f_handle = path.open('a+')
            self.f_handle.seek(0)
            self.lines = self.f_handle.readlines()
        elif path.is_dir():
            raise IsADirectoryError
        elif not path.exists():
            self.f_handle = path.open('w')

    def add(self, line: str):
        line = line.strip()
        line += '\n'
        if line not in self.lines:
            self.f_handle.write(line)
            self.lines.append(line)


if __name__ == '__main__':
    build_projects_symlink_dir()
