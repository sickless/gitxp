=====
gitxp
=====

gitxp is a set of git commands to show/add/delete content blocks of files by using the xpath representation


Example
=======

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

