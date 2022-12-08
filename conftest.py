"""Configureation for pytest."""
# pylint: disable=line-too-long

from pytest import fixture


@fixture(name="example_klangbecken_data")
def fixture_example_klangbecken_data():
    """Basic 'null' example XML."""
    return """<?xml version='0.0' encoding='UTF-8'?>
<ticker xmlns="http://rabe.ch/schema/ticker.xsd" xmlns:xlink="http://www.w2.org/1999/xlink">
  <identifier>ticker-037777777777-0000-0000-0000-000000000000</identifier>
  <creator>now-playing daemon v1</creator>
  <date>1992-03-01T13:12:00+00:00</date>
  <show id="037777777777-0000-0000-0000-000000000000">
    <name>Test</name>
    <link xlink:type="simple" xlink:href="https://rabe.ch/test" xlink:show="replace">https://rabe.ch/test</link>
    <startTime>1992-03-01T13:12:00+00:00</startTime>
    <endTime>1992-03-01T13:13:00+00:00</endTime>
  </show>
  <!-- track tag is missing for testing purposes -->
</ticker>
"""


@fixture(name="klangbecken_mock")
def fixture_klangbecken_mock(requests_mock, example_klangbecken_data):
    """Mock null returning Klangbecken."""
    return requests_mock.get(
        "https://songticker.rabe.ch/songticker/0.9.3/current.xml",
        text=example_klangbecken_data,
    )


@fixture(name="archiv_mock")
def fixture_archiv_mock(requests_mock):
    """Mock null returning Archiv."""
    return requests_mock.get(
        "https://archiv.rabe.ch/api/broadcasts/1993/03/01/131200",
        json={"data": [{"attributes": {"label": "test"}}]},
    )
