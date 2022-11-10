import pytest


@pytest.fixture(scope='session')
def vcr_config():
    return {
        'cassette_library_dir': 'tests/fixtures/cassettes',
        'serializer': 'yaml',
        'filter_headers': [('aftership-api-key', 'YOUR_API_KEY_IS_HERE'),('as-api-key', 'YOUR_AS_API_KEY'), ('as-api-ssecret', 'YOUR_AS_API_SECRET')],
        'record_mode': 'none',
        'match_on': ['uri', 'method', 'query', 'body'],
    }
