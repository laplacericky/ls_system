#!/usr/bin/env python3
import argparse,sys
import subprocess
from pathlib import Path
import re

def search_keyword(keyword, search_space):
    r = re.compile(rf"(?i).*{keyword}.*")
    return filter(r.match, search_space)

def print_limited_lines(lines, start, end, step):
    limited_lines = lines[start: end: step]
    for x in limited_lines:
        print(x)
    if len(limited_lines) < len(lines):
        print(f'--More--({len(limited_lines):d}/{len(lines):d})')
    else:
        print('(END)')

def all_files_and_dirs(d):
    result = []
    for x in d.iterdir():
        result.append(x)
        if not x.is_symlink() and x.is_dir():
            result += all_files_and_dirs(x)
    return result


def search_name(keyword):
    search_space = {x.name: x for x in all_files_and_dirs(Path('.'))}
    return [str(search_space[k]) for k in search_keyword(keyword, search_space)]

def by_date():
    return subprocess.run(['ls', '-Alht'], stdout = subprocess.PIPE, text = True, check = True).stdout.splitlines()[1:]

def by_size():
    r = subprocess.run(['du', '-sh', *Path('.').iterdir()], stdout = subprocess.PIPE, check = True)
    return subprocess.run(['sort', '-h'], input = r.stdout, stdout = subprocess.PIPE, check = True).stdout.decode().splitlines()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices = ['largest','smallest','newest','oldest','search'] )
    parser.add_argument('target', nargs='?')
    parser.add_argument('-n', '--head', type=int, default = 10)
    args = parser.parse_args()

    match args.mode:
        case 'largest'|'smallest'|'newest'|'oldest':
            assert args.target is None
        case 'search':
            assert args.target is not None

    match args.mode:
        case 'largest'|'smallest':
            result = by_size()
        case 'newest'|'oldest':
            result = by_date()
        case 'search':
            result = search_name(args.target)

    match args.mode:
        case 'largest'|'oldest':
            start = -1
            end = -args.head-1
            step = -1
        case 'smallest'|'newest':
            start = 0
            end = args.head
            step = 1
        case 'search':
            start = 0
            end = len(result)
            step = 1

    print_limited_lines(result, start, end, step)


if __name__ == '__main__':
    assert sys.version_info[0] >= 3 and sys.version_info[1] >= 11
    main()
