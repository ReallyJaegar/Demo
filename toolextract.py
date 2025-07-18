import json,re
with open("/storage/som/ToolRL/dataset/rlla_4k_raw/rlla_rl.json","r") as f:
    a=json.load(f)
 
# print(a[0]["instruction"])
print(len(a))
 
with open("toolsummary.json", "w") as file:
    file.write('[')
    for i in range(4000):
        prompt=a[i]["instruction"]
        tools = {}
        pattern = r"Name: ([^\n]+)\nDescription: ([^\n]+)"
        matches = re.findall(pattern, prompt)
 
        for match in matches:
            tool_name = match[0].strip()
            tool_description = match[1].strip()
            tools[tool_name] = tool_description
        _new_dict={
            "sys" :prompt,
            "tools":str(tools) ## list of dict [{name:description},{},..]
        }
        json.dump(_new_dict, file)
        if (i!=3999):
            file.write(',')
            file.write('\n')
    file.write(']')
 
# # Displaying the extracted tools
# for tool_name, tool_description in tools.items():
#     print(f"Tool Name: {tool_name}")
#     print(f"Description: {tool_description}")
#     print("-" * 50)