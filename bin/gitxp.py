#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import optparse
import os
from libgitxp import gitxp, addxp, delxp

if __name__ == '__main__':
    parser = optparse.OptionParser()
    _, args = parser.parse_args()
    if not args:
        sys.exit(1)
    if len(args) != 2:
        sys.exit(2)

    filename, xpath = gitxp.split_xpath(args[1])
    if args[0] == 'add':
        addxp.add(filename, xpath)
    elif args[0] in ('del', 'delete', 'rm', 'remove'):
        delxp.delete(filename, xpath)
    sys.exit(0)
