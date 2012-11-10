#!/usr/bin/python
# -*- coding: utf-8 -*-

import mimetypes

# backends:
import pybackend


def get_backend(filename):
    """{Returns backend class}

        Returns the backend class according to the filename
    """
    mime_type, encoding = mimetypes.guess_type(filename)
    if mime_type in ('text/x-python',):
        return pybackend.PyBackend()
    else:
        raise AssertionError('No backend found for %s' % filename)
