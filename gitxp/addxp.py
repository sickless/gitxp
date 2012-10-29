#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import difflib

def split_xpath(xpath):
    """ Returns (filename, xpath_to_add)

    """
    index = xpath.find('/')
    return (xpath[:index], xpath[index:])

def get_HEAD_file_content(filename):
    """ Returns string

        Get the content of filename at HEAD revision
    """
    p = subprocess.Popen(['git', 'show', 'HEAD:%s' % filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (child_out, child_err) = (p.stdout, p.stderr)
    return child_out.read()

def get_modified_file_content(filename):
    """ Returns string

        Get the current content of the modified filename
    """
    return open(filename).read()

def indent_count(s):
    """ Returns int

        Counts the first space and tab characters contained
        at the beginning of the given string.
    """
    cnt = 0
    for c in s:
        if c in ('\t', ' '):
            cnt += 1
            continue
        break
    return cnt

def get_blocksequence_of_xpath(content, xpath):
    """ Returns (int, string)

        Get the block sequence of the xpath from the content.

        The returned tuple contains
        * the index line of the beginning of the block sequence
        * the block  sequence itself
    """
    lines_content = content.splitlines()
    index_line = 0
    for path in xpath.split('/')[1:]:
        while True:
            if index_line >= len(lines_content):
                # Xpath not in this revision
                return (None, '')
            if 'class %s' % path in lines_content[index_line]:
                break
            if 'def %s' % path in lines_content[index_line]:
                break
            index_line += 1

    last_index_line = index_line+1
    indent = indent_count(lines_content[index_line])
    while True:
        if last_index_line >= len(lines_content):
            return (index_line, '\n'.join(lines_content[index_line:]))
        # Ignore empty lines
        if lines_content[index_line].strip() == '':
            last_index_line += 1
            continue
        # Indent is the same as the current block? That means to be the end!
        if indent_count(lines_content[last_index_line]) <= indent:
            break
        last_index_line += 1

    return (index_line, '\n'.join(lines_content[index_line:last_index_line]))

def get_patch(filename, xpath):
    """ Returns string

        Returns the diff string from the xpath block of the filename
    """
    HEAD_content = get_HEAD_file_content(filename)
    curr_content = get_modified_file_content(filename)
    HEAD_index_line, HEAD_block_content = get_blocksequence_of_xpath(HEAD_content, xpath)
    curr_index_line, curr_block_content = get_blocksequence_of_xpath(curr_content, xpath)
    # The block already exists or not?
    index_line = HEAD_index_line or curr_index_line
    diff_block = list(difflib.unified_diff(HEAD_block_content.splitlines(), curr_block_content.splitlines(), lineterm=''))
    # Re-writing the indexes
    diff_block[2] = diff_block[2].replace('-1', '-%i'%(index_line+1)).replace('+1', '+%i'%(index_line+1))
    # Adding the filename to patch
    intro_patch = "diff --git a/%s b/%s\n" % (filename, filename)
    return intro_patch + "\n".join(diff_block)


def apply_patch(patch):
    p = subprocess.Popen("""git apply --cached - << PATCH 
%s
PATCH""" % patch, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    filename, xpath = split_xpath(sys.argv[-1])
    patch = get_patch(filename, xpath)
    apply_patch(patch)

