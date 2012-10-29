#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gitxp

if __name__ == '__main__':
    filename, xpath = gitxp.split_xpath(sys.argv[-1])
    patch = gitxp.get_add_patch(filename, xpath)
    gitxp.apply_patch(patch)
