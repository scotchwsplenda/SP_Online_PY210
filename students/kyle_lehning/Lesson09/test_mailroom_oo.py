#!/usr/bin/env python3
"""
test code for donor_models.py and cli_main.py
"""

from donor_models import *
from cli_main import *
import pytest


def test_donor_init():
    """
    Tests that a donor can be initiated
    """
    e = Donor("Frank Dolittle")
    assert e.name == "Frank Dolittle"
    assert e.total_donation == 0
    assert e.donation_num == 0
    assert e.most_recent_donation == 0


def test_donor_str():
    """
    Tests a donors str magic function
    """
    e = Donor("Frank Dolittle")
    assert str(e) == "Donor with a name of Frank Dolittle"


def test_new_donation():
    """
    Tests that a new donation can be added to a donor
    """
    e = Donor("Frank Dolittle")
    e.new_donation(400.50)
    assert e.total_donation == 400.50
    assert e.donation_num == 1
    assert e.most_recent_donation == 400.50
    e.new_donation(201.50)
    assert e.total_donation == 602
    assert e.donation_num == 2
    assert e.most_recent_donation == 201.50


def test_avg_donation():
    """
    Tests that average donation property is calculated correctly
    """
    e = Donor("Frank Dolittle")
    assert e.avg_donation == 0
    e.new_donation(400.50)
    assert e.avg_donation == 400.50
    e.new_donation(201.50)
    assert e.avg_donation == 301
    e.new_donation(0.02)
    assert e.avg_donation == 200.67


def test_from_existing():
    """
    Tests that average an existing donor can be created
    """
    e = Donor.from_existing("Mark Zuckerberg", 16396.10, 3)
    assert e.name == "Mark Zuckerberg"
    assert e.total_donation == 16396.10
    assert e.donation_num == 3
    assert e.avg_donation == 5465.37
    assert e.most_recent_donation == 0


def test_generate_thanks():
    """
    Tests that a Donor can generate it's thank you text
    """
    e = Donor("Mark Zuckerberg")
    e.new_donation(547.20)
    thanks_text = e.generate_recent_thanks()
    thanks_text_test = ("Dear Mark Zuckerberg,"
                        "\n\nThank you for your kind donation of $547.20."
                        "\nIt will be put to very good use."
                        "\n\nSincerely,"
                        "\n-The Team")
    assert thanks_text == thanks_text_test
    e.new_donation(120.80)
    thanks_text2 = e.generate_total_thanks()
    thanks_text_test2 = ("Dear Mark Zuckerberg,"
                         "\n\nThank you for your kind donations totalling $668.00."
                         "\nIt will be put to very good use."
                         "\n\nSincerely,"
                         "\n-The Team")
    assert thanks_text2 == thanks_text_test2


def test_donor_collection_init():
    """
    Tests that a DonorCollection can be initiated
    """
    e = DonorCollection()
    assert len(e.donor_list) == 0


def test_add_new_donor():
    """
    Tests that a new donor can be added to DonorCollection's donor_list
    """
    e = DonorCollection()
    e.add_new_donor("Jack Sparrow")
    assert len(e.donor_list) == 1
    assert any(x.name == "Jack Sparrow" for x in e.donor_list)
    assert e.donor_list[0].name == "Jack Sparrow"
    assert e.donor_list[0].total_donation == 0
    assert e.donor_list[0].donation_num == 0
    assert e.donor_list[0].avg_donation == 0


def test_donor_collection_str():
    """
    Tests that DonorCollection object returns correct str
    """
    e = DonorCollection()
    e.add_new_donor("Jack Sparrow")
    assert str(e) == "DonorCollection with 1 donors"
    e.add_new_donor("New Person")
    assert str(e) == "DonorCollection with 2 donors"


def test_add_existing_donor():
    """
    Tests that an existing donor can be added to DonorCollection's donor_list
    """
    e = DonorCollection()
    e.add_existing_donor("Steve Jobs", 1002.40, 2)
    assert len(e.donor_list) == 1
    assert e.donor_list[0].name == "Steve Jobs"
    assert e.donor_list[0].total_donation == 1002.40
    assert e.donor_list[0].donation_num == 2
    assert e.donor_list[0].avg_donation == 501.20


def test_list_donor_names():
    """
    Tests that a list of donor names can be returned
    """
    e = DonorCollection()
    e.add_new_donor("Jack Sparrow")
    e.add_new_donor("Russell Wilson")
    e.add_new_donor("Ron Burgundy")
    all_donors = e.list_donor_names()
    assert len(e.donor_list) == 3
    assert all_donors == ["Jack Sparrow", "Russell Wilson", "Ron Burgundy"]


def test_generate_report():
    """
    Tests that a report is generated correctly
    """
    compare_string = """
Donor Name      | Total Given | Num Gifts | Average Gift
--------------------------------------------------------
Bill Gates       $  653784.49           2  $   326892.24
Mark Zuckerberg  $    16396.1           3  $     5465.37
Steve Jobs       $     1002.4           2  $       501.2
Jeff Bezos       $     877.33           1  $      877.33
Paul Allen       $     708.42           3  $      236.14
"""
    e = DonorCollection()
    e.add_existing_donor("Jeff Bezos", 877.33, 1)
    e.add_existing_donor("Paul Allen", 708.42, 3)
    e.add_existing_donor("Steve Jobs", 1002.40, 2)
    e.add_existing_donor("Mark Zuckerberg", 16396.1, 3)
    e.add_existing_donor("Bill Gates", 653784.49, 2)
    test_string = e.generate_report()
    assert test_string == compare_string
