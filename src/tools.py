from typing import List
from tool_strategy import Tool
import os
import requests

# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):    
    last_repo = ""
    def execute_tool(self, data:List):
        #if we have 2 entities (repo and date), we execute the tool with date parameter
        req = requests.get('http://localhost:5001/getSmells?repo='+data[0]+'&pat='+os.environ.get('GIT_PAT',"")+'&user='+data[data.__len__()-1]+"&graphs=True")
        print(req.json())
        # we retrieve the file names created by csdetector
        file_names = req.json().get("files")
        print(file_names)
        # if there is any file
        if len(file_names) > 0:
            for fn in file_names:
                # we make a request to get it from the csdetector folder
                file_req = requests.get("http://localhost:5001/uploads/"+fn, allow_redirects=True)
                els = str(fn).split("\\")
                # we save it locally
                open('src/attachments/'+els[len(els)-1], 'wb').write(file_req.content)
        results = req.json().get("result")[1:]
        return results

