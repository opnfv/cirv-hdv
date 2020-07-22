import pytest

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

@pytest.fixture(scope = 'session')
def case_file(request):
    return request.config.getoption("--cases")