.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c)

CIRV-HDV User Guide
===================

Requirements
^^^^^^^^^^^^
* Python3
* pip
* git

Installation
^^^^^^^^^^^^^

Clone repo as follows:

.. code-block:: bash

      $ git clone "https://gerrit.opnfv.org/gerrit/cirv-hdv"


then install required python packages:

.. code-block:: bash

      $ pip install -r cirv-hdv/requirements.txt

The command will install following packages

* PyYAML
* urllib3
* requests
* netaddr
* openpyxl
* pytest
* allure-pytest

Run
^^^^

move to the ``/hdv/redfish`` directory and run Validation
 
.. code-block:: bash

      $ cd /hdv/redfish
      $ pytest --allure-dir=<output_directory> --config=<pdf_file> --cases=<cases_file> hdv_redfish.py
      $ allure serve <output_directory>

* allure-dir: Path to name of the folder which will be used later to create graphical reports using python-allure.

* config: Path to pdf2.0 file. It is needed to access servers.

* cases: Path to case file, yaml file which store all the cases to validate.