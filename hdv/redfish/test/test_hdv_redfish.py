import unittest
import hdv_redfish
import http_handler
import logging

class TestHdvRedfish(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.bmc_ip = "http://localhost:8000"
        self.http_handler = http_handler.UrllibHttpHandler()
        self.sampleCase = {"case_name" : "check CPU amount",
                           "case_sn": "11",
                           "expected_code": "200",
                           "expected_result": '{"Members@odata.count": 2}',
                           "group": "compoment management",
                           "header": "null",
                           "method": "GET",
                           "request_body": "null",
                           "url": "/redfish/v1/Systems/{system_id}/Processors",
                           "key_flag_dict": {"system_id": 'Members'}
                            }

        self.method, self.url, self.req_body, self.expected_code, self.expected_value, self.tc_name, self.key_flag_dict \
            = self.sampleCase['method'], self.sampleCase['url'], self.sampleCase['request_body'], \
            self.sampleCase['expected_code'], self.sampleCase['expected_result'], self.sampleCase['case_name'], self.sampleCase['key_flag_dict']
    

    def test_create_real_url(self):
        depends_id = {}
        url_list = hdv_redfish.create_real_url(self.url, depends_id, None, self.key_flag_dict, self.http_handler, self.bmc_ip)
        expected_list = ["/redfish/v1/Systems/437XR1138R2/Processors"]
        #checking if url_list and expected_list have same elements, regarless of order
        self.assertCountEqual(expected_list,url_list)

if __name__ == '__main__':
    unittest.main()