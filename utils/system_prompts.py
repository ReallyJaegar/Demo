import json
 
# Open the JSON file
def givesysprompt(i):
    with open('/storage/som/Demo/toolsummary.json', 'r') as file:
        dataall = json.load(file)  # Load the entire JSON file into a list of dictionaries
        data=dataall[i]
        # keys=list(eval(data["tools"]).keys())
        # values=list(eval(data["tools"]).values())
        sys=data["sys"]
    return sys
 
if __name__=="__main__":
    a=givesysprompt(200)
    print(a)
