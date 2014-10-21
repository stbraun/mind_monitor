Tutorial
========


Logging
-------

The mind_monitor package supports logging based on the standard logging package.

Loggers are named 'mind_monitor'.

Example for a simple configuration in YAML format: ::

    version: 1
    formatters:
      simple:
        format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple
        stream: ext://sys.stdout
    loggers:
      mind_monitor:
        level: DEBUG
        handlers: [console]
        propagate: yes
    root:
      level: DEBUG
      handlers: [console]

Important is the logger 'mind_monitor' and it's propagate property.


Connecting to Mindwave device
-----------------------------

ThinkGear Connector is used for communication with the device. This is a socket server
providing easy data transfer via Json. It is part of NeuroSky's SDK which can be downloaded from their website.

The mindwave_interface package is used to connect to ThinkGear Connector. It provides functions for configuration
and reading data. The data will be returned as dictionary for easy use with Python.

*Example code:* ::

    import json
    from mindwave_interface connect_to_eeg_server, cleanup_raw_data

    sock = connect_to_eeg_server()
    buffer = sock.receive(1024)
    records = cleanup_raw_data(buffer)  # split in records
    for record in records:
        jres = json.loads(record)       # create dictionary for each record
        jres['time'] = time.time()      # and add a timestamp
        print(repr(jres))
    # ...
    sock.close()

----------

A simple test without chevrons:

.. testcode::

   print("lo")

.. testoutput::

   lo

And now a simple doc test:

>>> print("Hi")
Hi

