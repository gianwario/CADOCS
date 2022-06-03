from typing import List
from tool_strategy import Tool
import os
import requests

# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):    
    last_repo = ""
    def execute_tool(self, data:List):
        #TODO: execute csDetector
        #if we have 2 entities (repo and date), we execute the tool with date parameter
        print(data)
        x = requests.get('http://localhost:5001/getSmells?repo='+data[0]+'&pat='+os.environ.get('GIT_PAT',"")+'&user='+data[data.__len__()-1])
        #print(x.json())
        return x.json()[1:]
        #return ["BCE"]
