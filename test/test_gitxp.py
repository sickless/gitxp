#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import os.path
import tempfile
import shutil
import inspect
import git
import difflib
import sys

from libgitxp import addxp, delxp, resetxp, checkoutxp

def shortDescription(self):
    return ("\npython %s %s.%s" % (sys.argv[0], self.__class__.__name__, self._testMethodName))

if sys.version_info[:2] >= (2, 7):
    from unittest.runner import TextTestResult
    TextTestResult.getDescription = lambda _, self: shortDescription(self)

class TestGitXP(unittest.TestCase):

    path_of_testfile = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


    def setUp(self):
        super(TestGitXP, self).setUp()
        self.repodir = tempfile.mkdtemp()
        os.chdir(self.repodir)
        self.repo = git.Repo.init(self.repodir)
        shutil.copy(os.path.join(self.path_of_testfile, 'python/example.py'), self.repodir)
        self.repo.git.add('example.py')
        self.repo.git.commit(m='first')

    def tearDown(self):
        shutil.rmtree(self.repodir)
        super(TestGitXP, self).tearDown()

    def _assert(self, done, expected):
        if done != expected:
            print "done     :", repr(done)
            print "expected :", repr(expected)
        assert done == expected

    def _get_testfile_content(self, filename):
        content = open(os.path.join(self.path_of_testfile, filename)).read()
        return content[:-1]

    def _get_file_from_workingtree(self, filename):
        content = open(os.path.join(self.repodir, filename)).read()
        return content[:-1]
        

    def test_difflib_unified_diff(self):
        if sys.version_info[:2] <= (2, 6):
            expected = ['--- before.py ', # NOTE: A space character is present after the filename
                        '+++ after.py ',
                        '@@ -1,0 +1,2 @@', # Got -1
                        '+def foo():',
                        '+    return None']
            # Added a new function
            assert expected == list(difflib.unified_diff([], ['def foo():', '    return None'], fromfile='before.py', tofile='after.py', lineterm=''))
        else:
            expected = ['--- before.py',
                        '+++ after.py',
                        '@@ -0,0 +1,2 @@', # Got -0
                        '+def foo():',
                        '+    return None']
            # Added a new function
            assert expected == list(difflib.unified_diff([], ['def foo():', '    return None'], fromfile='before.py', tofile='after.py', lineterm=''))


    def test_addxp(self):
        file_with_changes = os.path.join(self.path_of_testfile, 'python/addxp/example.py_add')
        shutil.copy(file_with_changes, os.path.join(self.repodir, 'example.py'))
        addxp.add('example.py', '/Foo/bar2')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/addxp/example.py_expected1'))
        addxp.add('example.py', '/Foo/bar3')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/addxp/example.py_expected2'))
        addxp.add('example.py', '/Foo/bar')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/addxp/example.py_expected3'))
        addxp.add('example.py', '/Foo/__init__')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/addxp/example.py_expected4'))

    def test_delxp(self):
        delxp.delete('example.py', '/Foo/bar')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/delxp/example.py_expected1'))
        delxp.delete('example.py', '/Foo/bar2')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/delxp/example.py_expected2'))
        delxp.delete('example.py', '/Foo')
        self._assert(self.repo.git.show(':example.py'), '')

    def test_resetxp(self):
        # Do some changes
        file_with_changes = os.path.join(self.path_of_testfile, 'python/addxp/example.py_add')
        shutil.copy(file_with_changes, os.path.join(self.repodir, 'example.py'))
        addxp.add('example.py', '/Foo/bar2')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/addxp/example.py_expected1'))
        addxp.add('example.py', '/Foo/bar3')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/addxp/example.py_expected2'))
        # Reset them
        resetxp.reset('example.py', '/Foo/bar2')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/resetxp/example.py_expected1'))
        resetxp.reset('example.py', '/Foo/bar3')
        self._assert(self.repo.git.show(':example.py'), self._get_testfile_content('python/resetxp/example.py_expected2'))
        
    def test_checkoutxp(self):
        # Do some changes
        file_with_changes = os.path.join(self.path_of_testfile, 'python/addxp/example.py_add')
        shutil.copy(file_with_changes, os.path.join(self.repodir, 'example.py'))
        addxp.add('example.py', '/Foo')
        # Checkout them
        checkoutxp.checkout('example.py', '/Foo/bar2')
        self._assert(self._get_file_from_workingtree('example.py'), self._get_testfile_content('python/checkoutxp/example.py_expected1'))
        checkoutxp.checkout('example.py', '/Foo/bar')
        self._assert(self._get_file_from_workingtree('example.py'), self._get_testfile_content('python/checkoutxp/example.py_expected2'))
        checkoutxp.checkout('example.py', '/Foo/bar3')
        self._assert(self._get_file_from_workingtree('example.py'), self._get_testfile_content('python/checkoutxp/example.py_expected3'))
        checkoutxp.checkout('example.py', '/Foo/__init__')
        self._assert(self._get_file_from_workingtree('example.py'), self._get_testfile_content('python/checkoutxp/example.py_expected4'))
        # Do some changes again
        file_with_changes = os.path.join(self.path_of_testfile, 'python/addxp/example.py_add')
        shutil.copy(file_with_changes, os.path.join(self.repodir, 'example.py'))
        # Checkout all of them
        checkoutxp.checkout('example.py', '/Foo')
        self._assert(self._get_file_from_workingtree('example.py'), self._get_testfile_content('python/checkoutxp/example.py_expected4'))

if __name__ == '__main__':
    unittest.TestCase.shortDescription = shortDescription
    unittest.main()
