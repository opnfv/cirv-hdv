import json
import yaml
import pytest
import hdv.redfish.log_utils
from hdv.redfish.http_handler import UrllibHttpHandler
from hdv.redfish.hdv_redfish import create_real_url, execute_final_url, parse_test_result, parse_data

sample_case = {}
mock_server = {}
with open("test/sample_test_cases.yml", "r") as sample_test_file:
    sample_case = yaml.load(sample_test_file.read(), Loader=yaml.FullLoader)

with open("test/mock_server.json", "r") as mock_server_file:
    mock_server = json.load(mock_server_file)
    

@pytest.fixture(autouse=True)
def mock_response(monkeypatch):

    def mock_get(*args, **kwargs):
        return mock_server[args[0]]

    monkeypatch.setattr(hdv.redfish.hdv_redfish, "execute_get_url", mock_get)


@pytest.mark.parametrize("sampleCase, expected_list", [
    (sample_case[0], ["/redfish/v1/Systems/437XR1138R2"]),
    (sample_case[1], ["/redfish/v1/Chassis/1U"]),
    (sample_case[2], ["/redfish/v1/Systems/437XR1138R2/Processors"]),
    (sample_case[3], ["/redfish/v1/Systems/437XR1138R2/Processors/CPU1",
                      "/redfish/v1/Systems/437XR1138R2/Processors/CPU2",
                      "/redfish/v1/Systems/437XR1138R2/Processors/FPGA1"])
])
def test_create_real_url(sampleCase, expected_list):
    url, key_flag_dict = sampleCase["url"], sampleCase["key_flag_dict"]
    bmc_ip = ""
    depends_id = {}
    http_handler = UrllibHttpHandler()
    url_list = create_real_url(
        url, depends_id, None, key_flag_dict, http_handler, bmc_ip)
    assert expected_list == url_list


@pytest.mark.parametrize("sampleCase", sample_case)
def test_execute_final_url(sampleCase):
    method, url, req_body, key_flag_dict \
        = sampleCase["method"], sampleCase["url"], sampleCase["request_body"], sampleCase["key_flag_dict"]
    bmc_ip = ""
    depends_id = {}
    http_handler = UrllibHttpHandler()
    config_file = {}
    rsp_list = execute_final_url(config_file, depends_id,
                                 http_handler, method, url, req_body, key_flag_dict, bmc_ip)
    assert mock_server[url] == rsp_list


@pytest.mark.parametrize("sampleCase, expected_return_value_list", [
                        (sample_case[0], [{'return_code': 'Success', 'AssetTag': 'Success'}]),
                        (sample_case[1], [{'return_code': 'Success', "Oem": {"Mainboard":{"BoardName": "Success"}}}]),
                        (sample_case[2], [{'return_code': 'Success', "Members@odata.count": "Success" }]),
                        (sample_case[3], [{'return_code': 'Success', 'Manufacturer': 'Success', "MaxSpeedMHz": "Failure, expect value: 2300, return value: 3700", "ProcessorArchitecture": "Success"},
                                          {'return_code': 'Success', 'Manufacturer': "Failure, expect value: Intel(R) Corporation, return value: Can't find key Manufacturer in return value", "MaxSpeedMHz": "Failure, expect value: 2300, return value: Can't find key MaxSpeedMHz in return value", "ProcessorArchitecture": "Failure, expect value: ['x86', 'IA-64', 'ARM', 'MIPS', 'OEM'], return value: Can't find key ProcessorArchitecture in return value"},
                                          {'return_code': 'Success', 'Manufacturer': 'Success', "MaxSpeedMHz": "Failure, expect value: 2300, return value: Can't find key MaxSpeedMHz in return value", "ProcessorArchitecture": "Success"}])
])
def test_parse_result(sampleCase, expected_return_value_list):
    final_rst={}
    method, url, req_body, expected_code, expected_value, tc_name, key_flag_dict \
        = sampleCase["method"], sampleCase["url"], sampleCase["request_body"], \
        sampleCase["expected_code"], sampleCase["expected_result"], sampleCase["case_name"], sampleCase["key_flag_dict"]
    bmc_ip = ""
    depends_id = {}
    http_handler = UrllibHttpHandler()
    config_file = {}
    rsp_list = execute_final_url(config_file, depends_id,
                                 http_handler, method, url, req_body, key_flag_dict, bmc_ip)

    return_value_list, return_code_list, final_rst, flag = \
        parse_test_result(expected_value, expected_code, rsp_list, final_rst)

    assert return_code_list == [200] * len(return_code_list)

    assert return_value_list == expected_return_value_list


@pytest.mark.parametrize("sampleCase, expected_act_pairs_list", [
                        (sample_case[0], [{'AssetTag': ("CM_cc@1234", "CM_cc@1234")}]),
                        (sample_case[1], [{'Oem': {'Mainboard': {'BoardName': ('RS33M2C9S', 'RS33M2C9S')}}}]),
                        (sample_case[2], [{'Members@odata.count': (3, 3)}]),
                        (sample_case[3], [{'Manufacturer': ('Intel(R) Corporation', 'Intel(R) Corporation'), 'MaxSpeedMHz': (2300, 3700), 'ProcessorArchitecture': (['x86', 'IA-64', 'ARM', 'MIPS', 'OEM'], 'x86')},
                                          {'Manufacturer': ('Intel(R) Corporation', "Can't find key Manufacturer in return value"), 'MaxSpeedMHz': (2300, "Can't find key MaxSpeedMHz in return value"), 'ProcessorArchitecture': (['x86', 'IA-64', 'ARM', 'MIPS', 'OEM'], "Can't find key ProcessorArchitecture in return value")},
                                          {'Manufacturer': ('Intel(R) Corporation', 'Intel(R) Corporation'), 'MaxSpeedMHz': (2300, "Can't find key MaxSpeedMHz in return value"), 'ProcessorArchitecture': (['x86', 'IA-64', 'ARM', 'MIPS', 'OEM'], 'OEM')}])
])
def test_parse_data(sampleCase, expected_act_pairs_list):
    method, url, req_body, expected_code, expected_value, tc_name, key_flag_dict \
        = sampleCase["method"], sampleCase["url"], sampleCase["request_body"], \
        sampleCase["expected_code"], sampleCase["expected_result"], sampleCase["case_name"], sampleCase["key_flag_dict"]
    bmc_ip = ""
    depends_id = {}
    http_handler = UrllibHttpHandler()
    config_file = {}
    rsp_list = execute_final_url(config_file, depends_id,
                                 http_handler, method, url, req_body, key_flag_dict, bmc_ip)

    for i in range (0,len(rsp_list)):
        rsp = rsp_list[i]
        return_value = rsp["return_value"]
        expected_act_pairs = expected_act_pairs_list[i]
        exp_act_pairs = {}
        for key, value in expected_value.items():
            if key in return_value:
                exp_act_pairs[key] = parse_data(value, return_value[key])
            elif key == 'count':
                pass
            else:
                exp_act_pairs[key] = \
                    (value, "Can't find key {} in return value".format(key))
        assert exp_act_pairs == expected_act_pairs