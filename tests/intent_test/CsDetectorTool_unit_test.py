from src import tools
from tools import CsDetectorTool
import requests
from unittest.mock import mock_open, patch
import pytest
import json


class TestCsDetectorToolUT:

    @pytest.fixture
    def cs_tool_instance(self):
        cs_tool = CsDetectorTool()
        yield cs_tool

    @pytest.mark.parametrize("data, files", [
        (["repo", "data", "date"], ["commitCentrality_0.pdf",
         "Issues_0.pdf", "issuesAndPRsCentrality_0.pdf", "PRs_0.pdf"]),
        (["repo", "data"], ["commitCentrality_0.pdf", "Issues_0.pdf",
         "issuesAndPRsCentrality_0.pdf", "PRs_0.pdf"]),
        (["repo", "data"], [])
    ])
    def test_execute_tool_w_date(self, cs_tool_instance, mocker, data, files):
        response = {
            "files": files,

            "result": [
                "test",
                "response"
            ]
        }

        # Mock of the dotenv module
        mocker.patch('tools.os.environ.get',
                     return_value="CSDETECTOR_URL_GETSMELLS")

        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.json.return_value = response
        mocker.patch("requests.get", return_value=mock_response)

        #  Mock of the open method
        with patch("builtins.open", mock_open()) as mock_file:
            # Execute the tool
            result = cs_tool_instance.execute_tool(data)
            # Assertions
            assert result == ["response"]
