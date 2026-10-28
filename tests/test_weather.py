"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)
import pytest


def test_parse_time_regular_time():
    assert parse_time("14:21") == 861
    assert parse_time("00:00") == 0, "0 erwartet"
    assert parse_time("000014:21") == 861, "861 ertwartet"
    assert parse_time("23:59") == 1439, "1439 erwartet"
    assert parse_time("23:00000") == 1380, "1439 erwartet"

def test_time_wrong_format():
    with pytest.raises(ValueError):
        # parse_time(14.21) failed: Attribute error
        # parse_time(861) failed: Attribute error 
        parse_time("14:21:10")
        parse_time("14")
        parse_time("14,21")

def test_time_worng_type():
    with pytest.raises(AttributeError):
        parse_time(14.21)
        parse_time(861)


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)
    assert parse_measurement("   Köln;   14:21;    21.7") == ("Köln", 861, 21.7)
    assert parse_measurement("Köln    ;14:21    ;21.7    ") == ("Köln", 861, 21.7)
    assert parse_measurement("    Köln   ;   14:21  ;     21.7   ") == ("Köln", 861, 21.7)

def test_parse_measurement_wrong_format():
    with pytest.raises(ValueError):
        parse_measurement(("Köln",14.21,21.7)) == ("Köln", 861, 21.7)
        parse_measurement("Köln;14:21;21.7;0") == ("Köln", 861, 21.7)
        parse_measurement(" ;14:21;21.7") == ("Köln", 861, 21.7)


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

    with pytest.raises(ValueError):
        filter_by_temperature(measurements, 20.0, 15.0) # lower > upper
        filter_by_temperature(None) # nichts drinne
        filter_by_temperature(measurements, 15.0, 20.0) # doppelt
        filter_by_temperature(measurements, -15.0, -20.0) # negative values
    

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_average_temperature_case_sensivte():
    with pytest.raises(TypeError):
            hottest_measurement("düsseldorf", 720, 25.0) == ("Düsseldorf", 720, 25.0)

def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)
    with pytest.raises(TypeError):
            hottest_measurement("düsseldorf", 720, 25.0) == ("Düsseldorf", 720, 25.0)

def test_hottest_measurement_same_value():
    measurements = [
            ("Köln", 900, 25.0),
            ("Düsseldorf", 720, 25.0),
            ("Bonn", 900, 20.0),
        ]
    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)
    