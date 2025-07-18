import json
 
# Open the JSON file
def givetool(i):
    with open('/storage/som/Demo/toolsummary.json', 'r') as file:
        dataall = json.load(file)  # Load the entire JSON file into a list of dictionaries
        data=dataall[i]
        keys=list(eval(data["tools"]).keys())
        values=list(eval(data["tools"]).values())
    return keys,values
 
def get_tools_for_domain(index,domain=None):
 
    # tools = TOOL_DESCRIPTIONS.get(domain, [])
    keys,values=givetool(index)
    return "\n".join(f"{i}: {j}" for i,j in zip(keys,values))
