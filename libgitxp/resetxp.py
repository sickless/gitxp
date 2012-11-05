#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gitxp

def reset(filename, xpath):
    patch = gitxp.get_reset_patch(filename, xpath)
    gitxp.apply_patch(patch, revert=True)

if __name__ == '__main__':
    filename, xpath = gitxp.split_xpath(sys.argv[-1])
    reset(filename, xpath)
    sys.exit(0)
