from __future__ import annotations
from tool_strategy import Tool
from typing import List

# this is the context for our strategy pattern
class ToolSelector():
    def __init__(self, strategy: Tool) -> None:
        self._strategy = strategy

    # The Context maintains a reference to one of the Strategy objects. 
    # The Context does not know the concrete class of a strategy. 
    # It should work with all strategies via the Strategy interface
    @property
    def strategy(self) -> Strategy:
        return self._strategy
    
    # we could change the strategy, even at runtime
    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    # we run whichever tool has been selected as the strategy
    def run(self, data: List) -> List:
        result = self._strategy.execute_tool(data)
        return result


