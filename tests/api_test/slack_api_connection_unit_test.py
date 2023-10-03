from src.api import slack_api_connection
from src.service import utils
from src.intent_handling.cadocs_intents import CadocsIntents
from flask import Flask, make_response
from src.api.slack_api_connection import app, CadocsSlack
from src.chatbot import cadocs_utils
import json
import pytest
import requests
from unittest.mock import Mock, patch, PropertyMock


class TestSlackAPIConnectionUT:

    @pytest.fixture
    def client(self):
        # Create a test client for the Flask app
        with app.test_client() as client:
            with app.app_context():
                yield client

    def mock_handle_request(self):
        return "test_value"

    def mock_post_attachments(self):
        return "test_value"

    def mock_update_waiting_message(self):
        return "test_value_update"

    def test_answer(self, mocker, client):
        # Mock the start method of Thread class
        mocker.patch.object(slack_api_connection.threading.Thread,
                            'start', return_value=self.mock_handle_request)

        # Create the response for assertion
        expected_response = make_response("", 200)
        expected_response.headers['X-Slack-No-Retry'] = 1

        response = slack_api_connection.answer({})

        # Assertion
        assert expected_response.status_code == response.status_code
        assert expected_response.headers['X-Slack-No-Retry'] == response.headers['X-Slack-No-Retry']

    @pytest.mark.parametrize("intent, entities", [(CadocsIntents.GetSmells, ["repo_link"]),
                                                  (CadocsIntents.GetSmellsDate, [
                                                      "repo_link", "12/12/2022"]),
                                                  (CadocsIntents.Info, []),
                                                  (CadocsIntents.Report, [])])
    def test_handle_request(self, intent, entities, mocker):
        event = {
            "client_msg_id": "msg_test",
            "user": "user_test",
            "text": "text_test",
            "bot_id": None,
            "channel": "channel_test"
        }
        payload = {"event": event}

        # Mock the auth_test function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "auth_test", return_value=True)
        # Mock the users_info function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient, "users_info",
                            return_value={"user": {"id": "id_test"}})
        # Mock the post_waiting_message function
        mock_post_waiting_message = Mock()
        mock_post_waiting_message.do_run = True
        mocker.patch('src.api.slack_api_connection.post_waiting_message',
                     return_value=mock_post_waiting_message)
        # Mock the new_message function of CadocsSlack class
        mocker.patch.object(slack_api_connection.CadocsSlack, "new_message", return_value=(
            {"response": "ok"}, "result ok", entities, intent))
        # Mock the chat_postMessage function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "chat_postMessage", return_value="")
        # Mock the save_execution function of cadocs_utils file
        mocker.patch("src.chatbot.cadocs_utils.save_execution", return_value="")
        # Mock the start method of Thread class
        mocker.patch.object(slack_api_connection.threading.Thread,
                            'start', return_value=self.mock_post_attachments)

        expected_response = {"message": "true"}
        response = slack_api_connection.handle_request(payload)

        # Assertion
        assert expected_response == response

    def test_handle_request_exception(self, mocker):
        event = {
            "client_msg_id": "msg_test",
            "user": "user_test",
            "text": "text_test",
            "bot_id": None,
            "channel": "channel_test"
        }
        payload = {"event": event}

        # Mock the auth_test function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "auth_test", return_value=True)
        # Mock the user_info function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient, "users_info",
                            return_value={"user": {"id": "id_test"}})
        # Mock the post_waiting_message function
        mock_progress_message = Mock()
        mock_progress_message.do_run = True
        mocker.patch('src.api.slack_api_connection.post_waiting_message',
                     return_value=mock_progress_message)
        # Mock the new_message function of CadocsSlack class to make it throw an exception
        mock_new_message = Mock(side_effect=Exception("test exception"))
        mocker.patch.object(slack_api_connection.CadocsSlack,
                            "new_message", mock_new_message)
        expected_response = {"message": "false"}
        # Assertions
        with pytest.raises(Exception):
            slack_api_connection.handle_request(payload)

    @pytest.mark.parametrize("args, expected_url", [("?repo=repo_link&pat=pat&user=user_id&graphs=True&date=12/12/2022", "http://127.0.0.1:5001/getSmells?repo=repo_link&pat=pat&user=user_id&graphs=True&date=12/12/2022"),
                                                    ("?repo=repo_link&pat=pat&graphs=True&date=12/12/2022",
                                                     "http://127.0.0.1:5001/getSmells?repo=repo_link&pat=pat&user=default&graphs=True&date=12/12/2022"),
                                                    ("?repo=repo_link&pat=pat&date=12/12/2022",
                                                     "http://127.0.0.1:5001/getSmells?repo=repo_link&pat=pat&user=default&graphs=False&date=12/12/2022"),
                                                    ("?repo=repo_link&pat=pat&user=user_id&graphs=True",
                                                     "http://127.0.0.1:5001/getSmells?repo=repo_link&pat=pat&user=user_id&graphs=True"),
                                                    ("?repo=repo_link&pat=pat&graphs=True",
                                                     "http://127.0.0.1:5001/getSmells?repo=repo_link&pat=pat&user=default&graphs=True"),
                                                    ("?repo=repo_link&pat=pat", "http://127.0.0.1:5001/getSmells?repo=repo_link&pat=pat&user=default&graphs=False")])
    def test_get_smells_wrepo_wpat(self, mocker, client, args, expected_url):
        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mocker.patch("src.api.slack_api_connection.requests.get",
                     return_value=mock_response)

        client.get(f"/csDetector/getSmells{args}")

        # Assertion for verify the url called
        requests.get.assert_called_once_with(expected_url)

        # Reset the mock for the next test
        requests.get.reset_mock()

    @pytest.mark.parametrize("expected_response, args", [("Error: No repo field provided. Please specify a repo.", ""),
                                                         ("Error: No pat field provided. Please specify a pat.", "?repo=repo_link")])
    def test_get_smells_no_repo_no_pat(self, mocker, client, expected_response, args):
        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mocker.patch("src.api.slack_api_connection.requests.get",
                     return_value=mock_response)

        response = client.get(f"/csDetector/getSmells{args}")

        # Assertions
        assert response.status_code == 400
        # Assertion for verify the text of response
        assert response.get_data(as_text=True) == expected_response

        # Reset the mock for the next test
        requests.get.reset_mock()

    def test_download_file(self, client, mocker):
        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mock_response.content = "test_content"
        mocker.patch("src.api.slack_api_connection.requests.get",
                     return_value=mock_response)

        response = client.get(
            "/csDetector/uploads/test_file.txt")

        # Assertions
        assert response.status_code == 200
        # Assertion for verify the text of response
        assert response.get_data(as_text=True) == "test_content"

    def test_predict(self, mocker, client):
        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mocker.patch("src.api.slack_api_connection.requests.get",
                     return_value=mock_response)

        client.get("/cadocsNLU/predict?message=hello i'm tester")

        expected_url = "http://127.0.0.1:5000/predict?message=hello i'm tester"

        # Assertion for verify the url called
        requests.get.assert_called_once_with(expected_url)

    def test_predict_no_message(self, mocker, client):
        # Mock of the Response object
        mock_response = mocker.Mock(spec=requests.Response)
        mocker.patch("src.api.slack_api_connection.requests.get",
                     return_value=mock_response)

        response = client.get("/cadocsNLU/predict")

        # Assertion for verify the text of response
        assert response.get_data(
            as_text=True) == "Error: No message to provide to the model. Please insert a valid message."