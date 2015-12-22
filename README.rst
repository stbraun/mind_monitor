======
README
======

* Version: 0.0.1dev

This README would normally document whatever steps are necessary to get this application up and running. Currently the app is under development.

-------------
Quick summary
-------------

Module to access NeuroSKY Mindwave devices from Python code.

MindWave is a device allowing to capture raw and also pre-processed EEG data. It is quite limited because there is only one sensor, but it's fine for some experiments.

The device connects via Bluetooth to the computer. There is a low-level COM and a nice socket based protocol.
Data can be read as Json string and therefore easily processed using Python.

Currently *SQLite* is used for persistence. A graphs of the captured data based on *matplotlib* are provided.

--------------------
How do I get set up?
--------------------


There is no regular setup yet, just a view hints.

The device needs to be installed. *ThinkGearConnector* is used for communication, so it must be started before running mind monitor.
See the constants at top of ```mindwave_interface``` for configuration.

------------
Dependencies
------------

  * Python 3.5
  * matplotlib
  * Sphinx (for doc generation only)
  * nose (for tests only)
  * behave (for tests only)
  * sqlite3
  * tkinter
  * genutils
  
----------------------
Database configuration
----------------------

The database will be created on demand.
See ```monitor_sqlite.py```.


----------------
How to run tests
----------------

There are tests written for *behave* and others using *pyunit* that may be run with *nose*. 

-----------------------
Deployment instructions
-----------------------


    python3 setup.py install



--------------------------
How to tun the application
--------------------------

```mind_monitor.monitor_app.py``` will pop up a simple UI. 

Currently features available via UI:
  * Control recording of EEG data.
  * Plot recorded session data. (all eegPower records)

-----------------------
Contribution guidelines
-----------------------

#### Writing tests

Behavioral tests shall be written using *behave*. Those tests are blackbox tests; they are expected to respect the API of the unit under test. This helps to refactor the implementation without breaking the tests.

Sometimes it is useful to peek into a class for more detailed tests. These are called whitebox tests and shall be written using *pyunit*. 

Obviously white box tests may break during refactoring. Therefore the use of blackbox tests is the preferred way to go.

----------------
Other guidelines
----------------

* PEP 8 codestyle
* Pylint 

-------------------
Copyright & License
-------------------

  * Copyright 2014, 2015, Stefan Braun
  * License: MIT

