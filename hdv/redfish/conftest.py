import pytest
from hdv_redfish import read_yaml

def pytest_addoption(parser):
    parser.addoption(
        "--cases", action="store", default="./conf/cases.yaml", help="case yaml file"
    )
    parser.addoption(
        "--config", action="store", default="./conf/config.yaml", help="given global config.yaml file"
    )

@pytest.fixture(scope = 'session')
def conf_file(request):
    return request.config.getoption("--config")

def pytest_generate_tests(metafunc):
    if "case" in metafunc.fixturenames:
        cases_file = metafunc.config.getoption("--cases")
        metafunc.parametrize("case", read_yaml(cases_file))