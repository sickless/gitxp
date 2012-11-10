#!/usr/bin/python
# -*- coding: utf-8 -*-

import backend

class PyBackend(backend.Backend):
    """This is the backend class to deal with python files."""

    def get_blocksequence_of_xpath(self, file_content_list, xpath):
        """ Returns (int, list of strings)

            Get the block sequence of the xpath from the content.

            The returned tuple contains
            * the index line of the beginning of the block sequence
            * the block sequence itself.

        """
        idx = 0
        for path in xpath.split('/')[1:]:
            while True:
                if idx >= len(file_content_list):
                    # Xpath not in this revision
                    return (None, [])
                if 'class %s' % path in file_content_list[idx]:
                    break
                if 'def %s' % path in file_content_list[idx]:
                    break
                idx += 1

        last_idx = idx+1
        indent = self.indent_count(file_content_list[idx])
        while True:
            # Until the end of the file
            if last_idx >= len(file_content_list):
                return (idx, file_content_list[idx:])
            # Ignore empty lines
            if file_content_list[last_idx].strip() == '':
                last_idx += 1
                continue
            # Indent is the same as the current block? That means to be the end!
            if self.indent_count(file_content_list[last_idx]) <= indent:
                break
            last_idx += 1

        return (idx, file_content_list[idx:last_idx])



    def indent_count(self, s):
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

