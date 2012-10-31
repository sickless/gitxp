#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import difflib


ADDING_MODE=1
REMOVING_MODE=2

FROM_STAGE=1
FROM_HEAD=2

def split_xpath(xpath):
    """ Returns (filename, xpath_to_add)

    """
    index = xpath.find('/')
    return (xpath[:index], xpath[index:])

def get_file_content_from(filename, from_type):
    """ Returns list of strings

        Get the content of filename according from the given from_type.
    """
    if from_type == FROM_STAGE:
        before_colon = ''
    elif from_type == FROM_HEAD:
        before_colon = 'HEAD'
    p = subprocess.Popen(['git', 'show', '%s:%s' % (before_colon, filename)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (child_out, child_err) = (p.stdout, p.stderr)
    return child_out.read().splitlines()


def get_file_content_from_HEAD(filename):
    """ Returns list of strings

        Get the content of filename from the stage (index)
    """
    return get_file_content_from(filename, FROM_HEAD)

def get_file_content_from_stage(filename):
    """ Returns list of strings

        Get the content of filename from the stage (index)
    """
    return get_file_content_from(filename, FROM_STAGE)

def get_modified_file_content(filename):
    """ Returns list of strings

        Get the current content of the modified filename
    """
    return open(filename).read().splitlines()

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

def get_blocksequence_of_xpath(content_list, xpath):
    """ Returns (int, list of strings)

        Get the block sequence of the xpath from the content.

        The returned tuple contains
        * the index line of the beginning of the block sequence
        * the block sequence itself
    """
    idx = 0
    for path in xpath.split('/')[1:]:
        while True:
            if idx >= len(content_list):
                # Xpath not in this revision
                return (None, [])
            if 'class %s' % path in content_list[idx]:
                break
            if 'def %s' % path in content_list[idx]:
                break
            idx += 1

    last_idx = idx+1
    indent = indent_count(content_list[idx])
    while True:
        # Until the end of the file
        if last_idx >= len(content_list):
            return (idx, content_list[idx:])
        # Ignore empty lines
        if content_list[last_idx].strip() == '':
            last_idx += 1
            continue
        # Indent is the same as the current block? That means to be the end!
        if indent_count(content_list[last_idx]) <= indent:
            break
        last_idx += 1

    return (idx, content_list[idx:last_idx])

def get_patch(staged_content, new_content, index, mode, filename):
    """ Returns diff string

        staged_content (str): the current content in the stage
        new_content (str): the new wanted content
        index (int): index position of the staged_content
        mode (int): ADDING_MODE/REMOVING_MODE, used to set correctly the diff indexes
        filename (str): the filename to patch
    """
    diff_block = list(difflib.unified_diff(staged_content, new_content, lineterm=''))
    # Re-writing the indexes: 3rd line contains the index lines used to apply the patch
    if mode == ADDING_MODE:
        start, end = 1, 1
    elif mode == REMOVING_MODE:
        start, end = 1, 0
    diff_block[2] = diff_block[2].replace('-1', '-%i'%(index+start)).replace('+1', '+%i'%(index+end))
    # Adding the filename to the patch
    intro_patch = "diff --git a/%s b/%s\n" % (filename, filename)
    return intro_patch + "\n".join(diff_block)


def get_add_patch(filename, xpath):
    """ Returns string

        Returns the diff string from the xpath block of the filename
    """
    staged_content = get_file_content_from_stage(filename)
    current_content = get_modified_file_content(filename)
    _, staged_block_content = get_blocksequence_of_xpath(staged_content, xpath)
    current_idx, current_block_content = get_blocksequence_of_xpath(current_content, xpath)
    # We only need to know the current_idx to set properly
    # the patch even with changes done above in the file.
    return get_patch(staged_block_content, current_block_content, current_idx, ADDING_MODE, filename)

def get_rm_patch(filename, xpath):
    """ Returns string

        Returns the diff string which deletes the block content defined by the xpath
    """
    staged_content = get_file_content_from_stage(filename)
    idx, rm_block_content = get_blocksequence_of_xpath(staged_content, xpath)
    # Get contexts before and after if possible
    new_context = []
    add_beginning_context = idx
    if add_beginning_context:
        beginning_context = staged_content[idx-1]
        new_context.append(beginning_context)
    ending_idx = idx+len(rm_block_content)
    add_ending_context = ending_idx < len(staged_content)
    if add_ending_context:
        ending_content = staged_content[idx+len(rm_block_content)]
        new_context.append(ending_content)
    # And insert it to make the patch applying properly
    if add_beginning_context:
        rm_block_content.insert(0, beginning_context)
    if add_ending_context:
        rm_block_content.append(ending_content)
    return get_patch(rm_block_content, new_context, idx, REMOVING_MODE, filename)


def get_reset_patch(filename, xpath):
    """ Returns string

        Returns the diff string from the xpath block of the filename
    """
    HEAD_content = get_file_content_from_HEAD(filename)
    idx, HEAD_block_content = get_blocksequence_of_xpath(HEAD_content, xpath)
    # Get contexts before and after if possible
    new_context = []
    add_beginning_context = idx
    if add_beginning_context:
        beginning_context = HEAD_content[idx-1]
        new_context.append(beginning_context)
    ending_idx = idx+len(HEAD_block_content)
    add_ending_context = ending_idx < len(HEAD_content)
    if add_ending_context:
        ending_content = HEAD_content[idx+len(HEAD_block_content)]
        new_context.append(ending_content)
    # And insert it to make the patch applying properly
    if add_beginning_context:
        HEAD_block_content.insert(0, beginning_context)
    if add_ending_context:
        HEAD_block_content.append(ending_content)
    return get_patch(new_context, HEAD_block_content, idx, ADDING_MODE, filename)


def get_checkout_patch(filename, xpath):
    """ Returns string

        Returns the diff string which deletes the block content defined by the xpath
    """
    staged_content = get_file_content_from_stage(filename)
    idx, block_content = get_blocksequence_of_xpath(staged_content, xpath)
    # Get contexts before and after
    new_context = []
    if add_beginning_context:
        beginning_context = staged_content[idx-1]
        new_context.append(beginning_context)
    ending_idx = idx+len(staged_content)
    add_ending_context = ending_idx < len(staged_content)
    if add_ending_context:
        ending_content = staged_content[idx+len(block_content)]
        new_context.append(ending_content)
    # And insert it to make the patch applying properly
    if add_beginning_context:
        block_content.insert(0, beginning_context)
    if add_ending_context:
        block_content.append(ending_content)
    # TODO Refactoring is needed:
    #      The code is the same as get_rm_patch()
    #      excepted the 2 first arguments given to
    #      get_patch() which are reversed!
    return get_patch(new_context, block_content, idx, REMOVING_MODE, filename)


def apply_patch(patch, in_stage=True):
    """ Returns bool

        Returns True if nothing on stderr (which should mean the patch has been applied correctly)
    """
    stage = in_stage and " --cached" or ""
    p = subprocess.Popen("""git apply %s - << PATCH 
%s
PATCH""" % (stage, patch), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if p.stderr.read():
        return False
    return True

