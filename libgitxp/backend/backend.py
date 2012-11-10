#!/usr/bin/python
# -*- coding: utf-8 -*-

class Backend(object):
    """This is the abstract class for backends."""

    def get_blocksequence_of_xpath(self, file_content, xpath):
        """ Returns (int, list of strings)

            Get the block sequence of the xpath from the content.

            The returned tuple contains
            * the index line of the beginning of the block sequence
            * the block sequence itself.

        """
        raise NotImplementedError('Calling the method of the abstract backend class')
