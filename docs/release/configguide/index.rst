.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 

CIRV-HDV Configuration Guide
============================
The HDV tool takes input two files:

PDF2.0 
^^^^^^

.. _link: https://github.com/opnfv/cirv-sdv/tree/master/sdv/pdf/template
PDF2.0 is a standard to describe Pod infrastructure originated from OPNFV. you can find the further information about PDF2.0 here - `link`_.
HDV tool uses this file to get redfish ip and credentials for accessing servers.

cases file
^^^^^^^^^^

The file defines all the test cases which hdv tool takes as input to validate.
Every test case is a set of key-value pairs.

Example:

.. code-block:: console

    ...
    case_name: check CPU info
    case_sn: 12
    enabled: true
    expected_code: 200
    expected_result:
        count: 2
        Manufacturer: Intel(R) Corporation
        MaxSpeedMHz: 2300
        Model: "Intel(R) Xeon(R) Gold 5218N CPU @ 2.30GHz"
        ProcessorArchitecture: ["x86", "IA-64", "ARM", "MIPS", "OEM"]
        Socket: [1, 2]
        Status:
        Health: OK
        State: Enabled
        TotalCores: 16
        TotalThreads: 32
    group: compoment management
    header: null
    method: GET
    request_body: null
    url: /redfish/v1/Systems/{system_id}/Processors/{cpu_id}/
    ...

Create your own test case
^^^^^^^^^^^^^^^^^^^^^^^^^
There are differences between vendors's redfish implementation, or even versions for the same vendor.
So, we made the tool generic enough so that anyone can easily define more test case or update existing case in the cases.yaml by defining following paramters:


1. **case_name** : name of test case.
2. **case_sn** : Every testcase must have unique serial number
3. **enabled** : whether to run this test or skip
4. **expected_code**:  http return code (200,201,400,..)
5. **expected_result**: Tool will compare the response value with value define in ``expected_result`` to decide if the case passed.
6. **header**: header for http request
7. **method**: http method (GET, POST, PUT, DELETE)
8. **request_body**: data to sent in request in case of POST, PUT method else "null"
9. **url**: URI of the resource which needs to be validated
10. **key_flag_dict**:

How to write expected_result:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* It should be in yaml format.
* The hierachy should be exactly the same with actual returned value.
* a simple example:

.. code-block:: console

    expected_result:
      AssetTag: CM_cc@1234

* a complex example:

.. code-block:: console
 
      expected_result:
        count: 2
        Manufacturer: "Intel(R) Corporation"
        MaxSpeedMHz: 2300
        Model: "Intel(R) Xeon(R) Gold 5218N CPU @ 2.30GHz"
        ProcessorArchitecture: ["x86", "IA-64", "ARM", "MIPS", "OEM"]
        Socket: [1, 2]
        Status:
        Health: OK
        State: Enabled
        TotalCores: 16
        TotalThreads: 32
 
* In the above data, a specific "count" attribute defined to check components quantity returned, e.g How many cpus expected.
* Generally expected_result can be a subset attributes definition, comparing with actual return value.
* It can support list of all expected value for list of objects. Example: "Socket:[1,2]", expecting return "Socket:1" and "Socket:2" from returned response.


How to write URL and key_flag_dict:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Redfish uses RESTful interface semantics to access data that is defined in model format to perform out-of-band systems management.
Every test requires a URI of the target resource. The URIs for every Redfish Resource are defined to appear at known, fixed locations (you can find it in official redfis documentation of your server).

In HDV, for validation of more than 1 resource you have the option to replace the ids with variables.

Examples:

* Url for accessing CPU with id 1 of System id 1

.. code-block:: console

    url : /redfish/v1/Systems/1/Processors/1/ 


* Url for accessing all CPUs of System id 1

.. code-block:: console

    url : /redfish/v1/Systems/1/Processors/{cpu_id}/


* Url for accessing all CPUs of all Systems

.. code-block:: console

    url : /redfish/v1/Systems/{system_id}/Processors/{cpu_id}/

When using variables you need to define key_flag_dict, it is used to describe object name which hdv tool will use to replace variable in URL with appropriate resource id.

Example:

.. code-block:: console

    key_flag_dict :
        system_id: Members
        cpu_id: Members