import os
import pytest
# from kivy.clock import Clock
# Clock._maxfps = 0

KIVY_EVENTLOOP = os.environ['KIVY_EVENTLOOP']


try:
    from kivy.tests.fixtures import kivy_app
except SyntaxError:
    # async app tests would be skipped due to async_run forcing it to skip so
    # it's ok to fail here as it won't be used anyway
    pass


if KIVY_EVENTLOOP == 'async':
    import pytest_asyncio
    @pytest.fixture()
    def nursery():
        pass
    @pytest.fixture()
    def autojump_clock():
        return True
elif KIVY_EVENTLOOP == 'trio':
    import pytest_trio


@pytest.fixture(scope='session')
def delta():
    # TODO: make this able to configure from the command line option
    return 20


@pytest.fixture(autouse=True)
def set_maxfps_to_zero():
    from kivy.clock import Clock
    old_value = Clock._max_fps
    Clock._max_fps = 0
    yield
    Clock._max_fps = old_value
