Lessons Learned
===============

General Notes
-------------

* Make small steps at a time. Call **make html** frequently.
* Have an HTTP server and browser running to continually check the
  changes made to the documents your working on.

Python provides already a nice little HTTP server. Run it in the docs
folder (where the Sphinx Makefile resides) using: ::

      python -m http.server 65432 --bind 127.0.0.1

Document your API
-----------------
* Must use .. automodule:: resp. autoclass, autofunction with
  qualified names to get members extracted.
* Modules need to be imported by __init__ to be visible.


Include Math
------------

It might be useful to include some math in a document:

.. math::

   {a + b \over c} > 1

