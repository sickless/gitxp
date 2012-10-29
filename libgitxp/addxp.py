#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gitxp

def add(filename, xpath):
    patch = gitxp.get_add_patch(filename, xpath)
    gitxp.apply_patch(patch)

if __name__ == '__main__':
    filename, xpath = gitxp.split_xpath(sys.argv[-1])
    add(filename, xpath)
    sys.exit(0)
