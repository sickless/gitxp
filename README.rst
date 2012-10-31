=====
gitxp
=====

gitxp is a set of git commands to show/add/delete content blocks of files by using the xpath representation

Code is available on GitHub on the following address: `https://github.com/sickless/gitxp <https://github.com/sickless/gitxp>`_

Examples
========

git addxp
---------

::

    test $ git show HEAD:test.py
    class Foo:
        def __init__(self):
            pass
    
        def bar(self):
            return None
    
        def bar2(self):
            return "bar2"
    
    test $ git di
    diff --git a/test.py b/test.py
    index d3d67fb..1b845d7 100644
    --- a/test.py
    +++ b/test.py
    @@ -6,5 +6,8 @@ class Foo:
             return None
    
         def bar2(self):
    +        """Bla bla"""
             return "bar2"
    
    +    def bar3(self):
    +        return "bar3"
    test $ git addxp test.py/Foo/bar3
    test $ git di --cached
    diff --git a/test.py b/test.py
    index d3d67fb..aa820d8 100644
    --- a/test.py
    +++ b/test.py
    @@ -8,3 +8,5 @@ class Foo:
         def bar2(self):
             return "bar2"
    
    +    def bar3(self):
    +        return "bar3"
    test $ git di
    diff --git a/test.py b/test.py
    index aa820d8..1b845d7 100644
    --- a/test.py
    +++ b/test.py
    @@ -6,6 +6,7 @@ class Foo:
             return None
    
         def bar2(self):
    +        """Bla bla"""
             return "bar2"
    
         def bar3(self):
    test $ git addxp test.py/Foo/bar2
    test $ git di --cached
    diff --git a/test.py b/test.py
    index d3d67fb..1b845d7 100644
    --- a/test.py
    +++ b/test.py
    @@ -6,5 +6,8 @@ class Foo:
             return None
    
         def bar2(self):
    +        """Bla bla"""
             return "bar2"
    
    +    def bar3(self):
    +        return "bar3"
    test $


git delxp
--------

::

    test $ cat test.py
    class Foo:
        def __init__(self):
            pass
    
        def bar(self):
            return None
    
        def bar2(self):
            return "bar2"
    
    test $ git delxp test.py/Foo/bar
    test $ cat test.py
    class Foo:
        def __init__(self):
            pass
    
        def bar2(self):
            return "bar2"
    
    test $ git di --cached
    diff --git a/test.py b/test.py
    index d3d67fb..4f6a66f 100644
    --- a/test.py
    +++ b/test.py
    @@ -2,8 +2,6 @@ class Foo:
         def __init__(self):
             pass
    
    -    def bar(self):
    -        return None
    
         def bar2(self):
             return "bar2"
    test $ git delxp test.py/Foo/bar2
    test $ cat test.py
    class Foo:
        def __init__(self):
            pass
    
    test $ git di --cached
    diff --git a/test.py b/test.py
    index d3d67fb..52105ff 100644
    --- a/test.py
    +++ b/test.py
    @@ -2,9 +2,5 @@ class Foo:
         def __init__(self):
             pass
    
    -    def bar(self):
    -        return None
    
    -    def bar2(self):
    -        return "bar2"
    
    test $

git resetxp & git checkoutxp
----------------------------

::

    test $ git di --cached
    diff --git a/test.py b/test.py
    index d3d67fb..03d02b5 100644
    --- a/test.py
    +++ b/test.py
    @@ -2,9 +2,6 @@ class Foo:
         def __init__(self):
             pass
     
    -    def bar(self):
    -        return None
    -
         def bar2(self):
             return "bar2"
     
    test $ git di
    test $ git resetxp test.py/Foo/bar
    test $ git di --cached
    test $ git di
    diff --git a/test.py b/test.py
    index d3d67fb..03d02b5 100644
    --- a/test.py
    +++ b/test.py
    @@ -2,9 +2,6 @@ class Foo:
         def __init__(self):
             pass
     
    -    def bar(self):
    -        return None
    -
         def bar2(self):
             return "bar2"
     
    test $ git checkoutxp  test.py/Foo/bar
    test $ git di --cached
    test $ git di 
    test $ 
    
