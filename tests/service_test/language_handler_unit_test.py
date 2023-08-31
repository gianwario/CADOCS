import pytest
from src.service.language_handler import LanguageHandler

class TestLanguageHandlerUT:

    # This class implements a Singleton Design Pattern whose metaclass is SingletonMeta,
    # the tests focus on the class LanguageHandler, and in particular on its ability to have only one instance.
    
    @pytest.fixture
    def language_handler(self):
        return LanguageHandler()

    # This method tests the ability of the class to return the same instance.
    def test_return_same_instance(self):
        instance1 = LanguageHandler()
        instance2 = LanguageHandler()

        # Assertion
        assert instance1 == instance2

    # This method tests the detect_language method
    def test_detect_language(self, language_handler, mocker):
        # The language detector tool is mocked to detect the language of the message as italian
        mocker.patch('src.service.language_handler.detect', return_value="it")

        # Assertions
        assert language_handler.detect_language("Questo è un testo in lingua italiana") == "it"

    # This method tests the correct assignment of a new language to the _current_language variable
    def test_get_current_language(self, language_handler, mocker):
        # The language detector tool is mocked to detect the language of the message as italian
        mocker.patch('src.service.language_handler.detect', return_value="it")
        language_handler.detect_language("Questo è un testo in lingua italiana") == "it"

        # Assertions
        assert language_handler.get_current_language() == "it"
