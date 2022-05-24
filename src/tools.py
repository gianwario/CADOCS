from typing import List
from tool_strategy import Tool

# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):    
    def execute_tool(self, data:List):
        #TODO: execute csDetector
        # if we have 2 entities (repo and date), we execute the tool with date parameter
        return ["CS1", "CS2", "CS3"]