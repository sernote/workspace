import pytest

from fixture.application import Application

fixture = None


@pytest.fixture(scope='session')
def app(request) -> Application:
    """Test app session. Start new one if its None"""
    global fixture
    if fixture is None:
        fixture = Application()
    return fixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    """Stop test app session"""
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture
