#!/usr/bin/python3

import os
from collections import OrderedDict
from string import Template

MY_PATH = os.path.dirname(os.path.realpath(__file__))
HOWTOS_PATH = os.path.join(MY_PATH, 'howtos')

def substitute(text, variables, delim='^'):
    class NewTemplate(Template):
        delimiter = delim

    return NewTemplate(text).safe_substitute(variables)


def parse_howto(name, ask):
    text = ''
    variables = OrderedDict()

    with open(os.path.join(HOWTOS_PATH, name + '.txt'), 'r') as fd:
        for line in fd:
            line = line.strip()
            if line == '---':
                break
            else:
                try:
                    variable, value = line.split('=', 1)
                    variables[variable.strip()] = substitute(value.strip(), variables)
                except:
                    continue

        return(substitute(fd.read(), variables))


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='An howto system')
    parser.add_argument('name', help='The howto name to print')
    parser.add_argument('-a', '--ask', action='store_true', help='Ask for new variable values')

    args = parser.parse_args()

    try:
        print(parse_howto(args.name, args.ask))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit('error: ' + str(e))
