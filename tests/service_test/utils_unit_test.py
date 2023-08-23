import pytest
from unittest.mock import patch
from intent_handling.cadocs_intents import CadocsIntents
from service.utils import valid_link, valid_date
import datetime


class TestUtils:

    @patch('re.findall')
    def test_valid_link_with_valid_url(self, mock_findall):
        # Mock the return value of re.findall
        mock_findall.return_value = [
            ("https://github.com/tensorflow/ranking",)]
        
        # Mock the valid_link method
        result = valid_link("https://github.com/tensorflow/ranking")

        #Assertion
        assert result == True

    @patch('re.findall')
    def test_valid_link_with_invalid_url(self, mock_findall):
        # Mock the return value of re.findall
        mock_findall.return_value = []

        # Mock the valid_link method
        result = valid_link("invalid_url")

        #Assertion
        assert result == False

    # Mocking the re.findall function and the datetime.datetime class
    @patch('re.findall')
    @patch('datetime.datetime')
    def test_valid_date_with_valid_date(self, mock_datetime, mock_findall):
        # Mock the return value of re.findall
        mock_findall.return_value = ["2022/01/01"]

        mock_datetime.return_value = datetime.datetime(2022, 1, 1)
        # Mock the valid_date method
        result = valid_date("01/01/2022")

        #Assertion
        assert result == True

    @patch('re.findall')
    @patch('datetime.datetime')
    def test_valid_date_with_valid_date_exception(self, mock_datetime, mock_findall):
        with patch('datetime.datetime') as mock_datetime:
            # Mock of datatime construction
            mock_datetime.side_effect = ValueError("Invalid date")
            result = valid_date("07/31/2023")

        #Assertion
        assert result == False

    # Mocking the re.findall function and the datetime.datetime class
    @patch('re.findall')
    @patch('datetime.datetime')
    def test_valid_date_with_invalid_date(self, mock_datetime, mock_findall):
        # Mock the return value of re.findall
        mock_findall.return_value = []
        result = valid_date("invalid_date")

        #Assertion
        assert result == False

    def test_enum_values(self):
        assert CadocsIntents.GetSmells.value == "get_smells"
        assert CadocsIntents.GetSmellsDate.value == "get_smells_date"
        assert CadocsIntents.Report.value == "report"
        assert CadocsIntents.Info.value == "info"