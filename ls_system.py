#!/usr/bin/env python3
import argparse,sys
import subprocess
from pathlib import Path

def by_date():
    return subprocess.run(['ls', '-Alht'], stdout = subprocess.PIPE, text = True, check = True).stdout.splitlines()[1:]

def by_size():
    r = subprocess.run(['du', '-sh', *Path('.').iterdir()], stdout = subprocess.PIPE, check = True)
    return subprocess.run(['sort', '-h'], input = r.stdout, stdout = subprocess.PIPE, check = True).stdout.decode().splitlines()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices = ['largest','smallest','newest','oldest'] )
    parser.add_argument('-n', '--head', type=int, default = 10)
    args = parser.parse_args()

    match args.mode:
        case 'largest'|'smallest':
            result = by_size()
        case 'newest'|'oldest':
            result = by_date()

    match args.mode:
        case 'largest'|'oldest':
            result = result[-1:-args.head-1:-1]
        case 'smallest'|'newest':
            result = result[:args.head]

    for x in result:
        print(x)


if __name__ == '__main__':
    assert sys.version_info[0] >= 3 and sys.version_info[1] >= 11
    main()
