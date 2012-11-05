#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gitxp

def checkout(filename, xpath):
    patch = gitxp.get_checkout_patch(filename, xpath)
    gitxp.apply_patch(patch, in_stage=False)

if __name__ == '__main__':
    filename, xpath = gitxp.split_xpath(sys.argv[-1])
    checkout(filename, xpath)
    sys.exit(0)
