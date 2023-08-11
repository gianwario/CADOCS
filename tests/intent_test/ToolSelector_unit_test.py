import pytest
from unittest.mock import Mock
from src import tool_selector, tools, tool_strategy

class TestToolSelectorUT:

    #Since this class implements a Strategy Design Pattern, the tests focus on 
    # the ability to set the correct strategy and being able change it 
    # as well as to run the strategy
    

    @pytest.fixture
    def mock_strategy_implementation(self):
        return Mock(spec=tool_strategy.Tool)

    def tool_selector_instance(self, mock_strategy_implementation):
        tool_selector_test = tool_selector.ToolSelector(mock_strategy_implementation)
        yield tool_selector_test

    # Here is tested the setter of the class

    def test_setter(self, mock_strategy_implementation):
        tool_selector_test =  tool_selector.ToolSelector(mock_strategy_implementation)

        # another instance of a mocked tool is created and assigned to the tool_selector using its setter

        new_strategy_implementation = Mock(spec=tool_strategy.Tool)
        tool_selector_test.strategy = new_strategy_implementation

        # Assertion

        assert tool_selector_test.strategy == new_strategy_implementation

    # Here is tested the ability of the class to return the same output of the set strategy implementation

    def test_run(self, mock_strategy_implementation):
        tool_selector_test =  tool_selector.ToolSelector(mock_strategy_implementation)
        
        data_test = ["data_test_1", "data_test_2"]
        expected_response = ["processed_data_test_1", "processed_data_test_2"]
        
        # The return value of the mocked strategy implementation is set

        mock_strategy_implementation.execute_tool.return_value = expected_response

        result = tool_selector_test.run(data_test)

        # Assertion

        assert result == expected_response