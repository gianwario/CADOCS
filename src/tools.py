from typing import List
from tool_strategy import Tool
import requests

# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):    
    last_repo = ""
    def execute_tool(self, data:List):
        #TODO: execute csDetector
        #if we have 2 entities (repo and date), we execute the tool with date parameter
        #print(data)
        x = requests.get('http://localhost:5001/getSmells?repo='+data[0]+'&pat=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')
        #print(x.json())
        return x.json()[1:]
        #return ["BCE"]
