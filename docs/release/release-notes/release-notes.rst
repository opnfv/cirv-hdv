.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c)

OPNFV Jerma Release
====================

Introduction:
^^^^^^^^^^^^^
 
This is a sub project of CIRV about the hardware delivery validation tool implementation,
short as HDV. The HDV implementation is based on redfish interface. It can be used to validate or configurate server hardware,
especially if a very large scale of resource pool to build in NFV where all the servers are expected with same configuration required.
It's possible for user to have a slightly different of redfish interface across the server model from vendors, users are encouraged to edit
and prepare their specific validation case file for the specific server.  Then it is capable to promote operator to examine hardware efficiently. 


Features:
^^^^^^^^^

* open framework to support multi-vendor redfish
* support of CNTT-RI PDF2.0 format definition
* develop default HP test case yml file supported
* documentation of user guide, developer guide

Known issue:
^^^^^^^^^^^

N/A listing the known issue if any
