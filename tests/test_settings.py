from tests import settings as _settings

TEST_SETTINGS = dict(
    (k, getattr(_settings, k)) for k in dir(_settings) if k == k.upper()
)
