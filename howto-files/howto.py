#!/usr/bin/python3

import os
from collections import OrderedDict
from string import Template

MY_PATH = os.path.dirname(os.path.realpath(__file__))
HOWTOS_PATH = os.path.join(MY_PATH, 'howtos')
HOWTO_EXT = '.txt'


def substitute(text, variables, delim='^'):
    class NewTemplate(Template):
        delimiter = delim

    return NewTemplate(text).safe_substitute(variables)


def howtos_get_list():
    for (dirpath, dirnames, filenames) in os.walk(HOWTOS_PATH):
        return sorted([f[:-len(HOWTO_EXT)] for f in filenames if f.endswith(HOWTO_EXT)])


def howto_parse(name, ask):
    variables = OrderedDict()

    with open(os.path.join(HOWTOS_PATH, name + HOWTO_EXT), 'r') as fd:
        for line in fd:
            line = line.strip()
            if line == '---':
                break
            else:
                try:
                    variable, value = line.split('=', 1)
                    variables[variable.strip()] = substitute(value.strip(), variables)
                except ValueError:
                    continue

        return(substitute(fd.read(), variables))


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='An howto system')
    parser.add_argument('-a', '--ask', action='store_true', help='ask for new variable values')
    parser.add_argument('-l', '--list', action='store_true', help='list available howtos')
    parser.add_argument('-p', '--print', dest='howto', metavar='howto', help='print the <howto> to the console')

    args = parser.parse_args()

    try:
        if args.list:
            print('Howtos:\n')
            for howto in howtos_get_list():
                print(howto)
        elif args.howto is not None:
            print(howto_parse(args.howto, args.ask))
        else:
            print(args)
            parser.print_help()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit('{}: {}'.format(e.__class__.__name__, str(e)))
