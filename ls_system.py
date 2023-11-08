#!/usr/bin/env python3
import argparse,sys
import subprocess
from pathlib import Path
from lib_output import limited_lines

def search_name(pattern):
    matched = Path('.').rglob(pattern)
    return [str(x) for x in sorted(matched, key=lambda y: len(y.parents) )]

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
    parser.add_argument('-a','--all',action='store_true')
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
        case 'smallest'|'newest'|'search':
            start = 0
            end = args.head
            step = 1

    if args.all:
        for x in result:
            print(x)
    else:
        print(limited_lines(result, start, end, step, more_info = True))


if __name__ == '__main__':
    assert sys.version_info[0] >= 3 and sys.version_info[1] >= 11
    main()
