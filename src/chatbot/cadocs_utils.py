from os import path
import json


# this method saves execution results to file system
# in order to retrieve it when needed
# we chose the json due to the format of the input
# and basing on the following study
# http://matthewrocklin.com/blog/work/2015/03/16/Fast-Serialization
def save_execution(results, exec_type, date, repo, user):
    filename = f'src/executions/executions_{user}.json'
    list_obj = []
    # Check if file exists
    if path.isfile(filename) is False:
        with open(filename, 'w'):
            pass

    with open(filename) as fp:
        try:
            list_obj = json.load(fp)
        except:
            pass
        list_obj.append(
            {
                "user": user,
                "exec_type": exec_type,
                "date": date,
                "repo": repo,
                "results": results
            }
        )
    with open(filename, 'w') as json_file:
        json.dump(list_obj, json_file,
                    indent=4,
                    separators=(',', ': '))
    # Read JSON file

# this method will retrieve the last execution of the current user in order to display it
def get_last_execution(user):
    filename = f'src/executions/executions_{user}.json'
    list_obj = []
    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")

    # Read JSON file
    with open(filename) as fp:
        list_obj = json.load(fp)
    return list_obj[list_obj.__len__()-1]    
