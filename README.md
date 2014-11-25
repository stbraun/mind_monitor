# README #

* Version: 0.0.1dev

This README would normally document whatever steps are necessary to get this application up and running. Currently the app is under development.

### Quick summary

Module to access NeuroSKY Mindwave devices from Python code.

MindWave is a device allowing to capture raw and also pre-processed EEG data. It is quite limited because there is only one sensor, but it's fine for some experiments.

The device connects via Bluetooth to the computer. There is a low-level COM and a nice socket based protocol.
Data can be read as Json string and therefore easily processed using Python.

Currently *MongoDB* is used for persistence. A simple graph of the captured data based on *matplotlib* is provided.


### How do I get set up? ###

#### Summary of set up ####

There is no regular setup yet, just a view hints.

#### Configuration ####

The device needs to be installed. *ThinkGearConnector* is used for communication, so it must be started before running mind monitor.

#### Dependencies ####
  * Python 3.4
  * matplotlib
  * pymongo
  * Sphinx (for doc generation only)
  * nose (for tests only)
  * MongoDB
  
#### Database configuration ####

The database instance must be provided. Collections will be created on demand.
See ```monitor_db.py```.

#### How to run tests ####

There are tests written for *behave* and others using *pyunit* and may be run with *nose*. 

#### Deployment instructions ####

```
python3 setup.py install
```

### Contribution guidelines ###

#### Writing tests

Behavioral tests shall be written using *behave*. Those tests are blackbox tests; they are expected to respect the API of the unit under test. This helps to refactor the implementation without breaking the tests.

Sometimes it is useful to peek into a class for more detailed tests. These are called whitebox tests and shall be written using *pyunit*. 

Obviously white box tests may break during refactoring. Therefore the use of blackbox tests is the preferred way to go.

#### Other guidelines
* PEP 8 codestyle
* Pylint 

### Copyright & License ###

  * Copyright 2014, Stefan Braun
  * License: MIT

