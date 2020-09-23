import pytest
from hdv_redfish import read_yaml, parse_config

def pytest_addoption(parser):
    parser.addoption(
        "--cases", action="store", default="./conf/cases.yaml", help="case yaml file"
    )
    parser.addoption(
        "--config", action="store", default="./conf/pdf2.0.json", help="given global config.yaml file"
    )


def pytest_generate_tests(metafunc):
    if "config_list" in metafunc.fixturenames:
        config_file = metafunc.config.getoption("--config")
        metafunc.parametrize("config_list", parse_config(config_file), indirect=True, scope='session')

    if "case" in metafunc.fixturenames:
        cases_file = metafunc.config.getoption("--cases")
        metafunc.parametrize("case", read_yaml(cases_file))