import json
import yaml
import pytest
import hdv.redfish.log_utils
from hdv.redfish.http_handler import UrllibHttpHandler
from hdv.redfish.hdv_redfish import create_real_url

sample_case = {}

with open('test/sample_test_cases.yml', 'r') as sample_test_file:
    sample_case = yaml.load(sample_test_file.read(), Loader=yaml.FullLoader)

@pytest.fixture(autouse=True)
def mock_response(monkeypatch):

    with open('test/mock_server.json', 'r') as mock_server_file:
        mock_server = json.load(mock_server_file)

    def mock_get(*args, **kwargs):
        return mock_server[args[0]]

    monkeypatch.setattr(hdv.redfish.hdv_redfish, "execute_get_url", mock_get)


@pytest.mark.parametrize("sampleCase, expected_list", [
    (sample_case[0], ["/redfish/v1/Systems/437XR1138R2"]),
    (sample_case[1], ["/redfish/v1/Chassis/1U"]),
    (sample_case[2], ["/redfish/v1/Systems/437XR1138R2/Processors"]),
    (sample_case[3], ['/redfish/v1/Systems/437XR1138R2/Processors/CPU1',
                      '/redfish/v1/Systems/437XR1138R2/Processors/CPU2',
                      '/redfish/v1/Systems/437XR1138R2/Processors/FPGA1'])
])
def test_create_real_url(sampleCase, expected_list):

    url, key_flag_dict = sampleCase['url'], sampleCase['key_flag_dict']
    bmc_ip = ""
    depends_id = {}
    http_handler = UrllibHttpHandler()
    url_list = create_real_url(url, depends_id, None, key_flag_dict, http_handler, bmc_ip)
    #checking if url_list and expected_list have same elements, regarless of order
    assert expected_list == url_list