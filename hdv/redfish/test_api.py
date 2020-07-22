from datetime import datetime as dt
import requests

OPNFV_URL = "http://testresults.opnfv.org/test/api/v1"
POD_NAME = 'intel-pod10'
INSTALLER = 'none'
BUILD_TAG = "none"
PKG_LIST = 'package-list.mk'
START_TIME = dt.now().strftime('%Y-%m-%d %H:%M:%S')
STOP_TIME = dt.now().strftime('%Y-%m-%d %H:%M:%S')
TC_NAME = 'HDV_Redfish_Basic'
VERSION = '1.0'
CRITERIA = 'PASS'

class PushResults():
    """ Push results to opnfv test api """
    def __init__(self, results, logger):
        """ constructor """
	    # store external values
        self.results = results
        self.logger = logger
        # initialize internal values
        self.push_vals = dict()
        # call functions
        self.generate_response()
        self.push_results()

    def generate_response(self):
        """ generate json output to be pushed """
        # Build body
        body = {
            "project_name": "cirv",
            "scenario": "none",
            "start_date": START_TIME,
            "stop_date": STOP_TIME,
            "case_name": TC_NAME,
            "pod_name": POD_NAME,
            "installer": INSTALLER,
            "version": VERSION,
            "build_tag": BUILD_TAG,
            "criteria": CRITERIA,
            "details": self.results
	        }

        self.logger.debug("The generated json response to be pushed:%s", body)
        # store this value in the class variable
        self.push_vals = body
	
    def push_results(self):
        """ push results to testapi """
        url = OPNFV_URL + "/results"
        print(self.push_vals)
        try:
            response = requests.post(url, json=self.push_vals)
            self.logger.info("testapi push response:%s", response)
        except ConnectionError:
	            self.logger.exception("error while pushing results to testapi")
	            self.logger.error("failed to push results")
