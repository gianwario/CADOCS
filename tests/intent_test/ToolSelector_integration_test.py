import pytest
import requests
from intent_handling import tools
from intent_handling import tool_selector


class TestToolSelectorIT:

    # The tests focus on the ability to set the correct strategy
    # and being able change it as well as to run the strategy like in unit test

    # Here is tested the setter of the class
    def test_setter(self):
        tool_selector_test = tool_selector.ToolSelector(
            tools.CsDetectorTool())
        # another instance of CsDetectorTool is created and assigned to the tool_selector using its setter
        new_strategy_implementation = tools.CsDetectorTool
        tool_selector_test.strategy = new_strategy_implementation
        # Assertion
        assert tool_selector_test.strategy == new_strategy_implementation

    # Here is tested the ability of the class to return the same output of the set strategy implementation
    def test_run(self, mocker):
        tool_selector_test = tool_selector.ToolSelector(
            tools.CsDetectorTool())

        data_test = ["data1", "data2"]

        # Mock the csDetector response
        response = {
            "files": [],
            "result": [
                "test",
                "response"
            ]
        }

        # Mock of the dotenv module
        mocker.patch('intent_handling.tools.os.environ.get',
                     return_value="CSDETECTOR_URL_GETSMELLS")

        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response
        mocker.patch("intent_handling.tools.requests.get", return_value=mock_response)

        response = tool_selector_test.run(data_test)

        # Assertion
        assert ["response"] == response
