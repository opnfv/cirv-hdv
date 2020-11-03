.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 

CIRV-HDV Developer Guide
========================


Intended Audience
^^^^^^^^^^^^^^^^^

This document is intended to aid those who want to modify the hdv code Or 
to extend it to add new features.

Requirements
^^^^^^^^^^^^
* Python3
* pip
* git

Installation
^^^^^^^^^^^^^

Clone repo as follows:

.. code-block:: bash

      $ git clone "git clone "ssh://YourLFID@gerrit.opnfv.org:29418/cirv-hdv""


then install required python packages:

.. code-block:: bash

      $ pip install -r cirv-hdv/requirements.txt


Structure
^^^^^^^^^ 
  
.. code-block:: console

    ./redfish
    ├─conf   # config directory
    ├─logs   # hdv.log would be generated here.


.. code-block:: console

    $ ls redfish/*.py
    redfish/__init__.py  
    redfish/hdv_redfish.py    #The main code implementation by parsing config.yaml and cases.yaml
    redfish/conftest.py       # File automitacally runs before hdv_redfish.py used to take input and add paramters to fixtures.
    redfish/log_utils.py      #log utils
    redfish/errors.py         #error code definition for the tool during parse.
    redfish/http_handler.py   #http_handler
    redfish/yaml_utils.py	  #yaml utils for test.

    $ ls redfish/conf
    pdf2.0  # OPNFV Pod Descriptor File, Used by hdv for accessing servers
    cases.yaml   #test cases yaml file
    report.yaml  #final test report


    $ ls redfish/logs
    hdv.log     # test log file
