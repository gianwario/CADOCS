from typing import List
from tool_strategy import Tool

# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):    
    def execute_tool(self, data:List):
        #TODO: execute csDetector
        return ["CS1", "CS2", "CS3"]