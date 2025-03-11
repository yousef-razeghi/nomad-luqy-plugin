import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    # Check that the magnitude of the quantity is 1.0, since subcell_area is a quantity with units  # noqa: E501
    assert entry_archive.data.settings.subcell_area.magnitude == 1.0
