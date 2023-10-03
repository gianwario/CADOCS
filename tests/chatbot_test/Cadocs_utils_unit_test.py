from src.chatbot import cadocs_utils
import pytest


class TestCadocsUtilsUT:
    
    def test_get_last_execution_missing_file(self, mocker):
        user_test = "user"
        # Mock the path.isfile method
        mocker.patch('src.chatbot.cadocs_utils.path.isfile', return_value=False)

        # Assertions
        with pytest.raises(Exception, match="File not found"):
            cadocs_utils.get_last_execution(user_test)
            