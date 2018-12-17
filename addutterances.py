import os
import httplib2
import json
result = True
headers = {"Ocp-Apim-Subscription-Key": "3f88533f3ac04af787adaeb946f26956", "Content-Type": "application/json"}
appid='573a1ae6-4fbb-40ad-b353-6a085112755c'
dir=os.getcwd()
def addUtterances():
    configEntites = []
    result = True
    for file in os.listdir(dir):
        if result and file.endswith(".txt"):
                utterances = []
                intent = os.path.splitext(file)[0]
                print("Adding utterances for " + intent)
                with open(file, "r") as intentFile:
                    for example in intentFile:
                        entityLabels = []

                        # Check if example has entities
                        exampleSplit = example.strip().split("<=>")
                        exampleText = exampleSplit[0].strip()
                        #print(exampleSplit)
                        if len(exampleSplit)==1:
                            exampleEntities = exampleSplit[0:]
                            #print(exampleEntities)
                            # check if entities mentioned in text exist in config
                            """for exampleEntity in exampleEntities:
                                if not exampleEntity.strip() in configEntites:
                                    print("The entity " + exampleEntity + " used in " + exampleText + " is not present in config")
                                    return None"""

                            # Check if parantheses match
                            openParanCount = exampleText.count("(")
                            closeParanCount = exampleText.count(")")

                            """if openParanCount != closeParanCount:
                                print("Paranthesis don't match for " + exampleText)
                                return None"""

                            # Check if paranthesis and provide entities match
                            """if openParanCount != len(exampleEntities):
                                print("The entities provided and the words marked in paranthesis don't match for " + exampleText)
                                return None

                            startPos = 0
                            entitiesCount = 0
                            noOfEntities = len(exampleEntities)"""

                            """while entitiesCount < noOfEntities:
                                startPos = exampleText.find("(", startPos, len(exampleText)) + 1
                                endPos = exampleText.find(")", startPos, len(exampleText)) - 1
                                entityLabel = {"EntityType": exampleEntities[entitiesCount].strip(),
                                               "StartToken": startPos - ((entitiesCount * 2) + 1),
                                               "EndToken": endPos - ((entitiesCount * 2) + 1)}
                                entitiesCount += 1
                                entityLabels.append(entityLabel)"""

                            utterances.append({"text": exampleText.replace("(", "").replace(")", ""),
                                               "intentName": intent, "entityLabels": entityLabels})

                if len(utterances) > 0:
                    try:
                        print(utterances)
                        conn = httplib2.HTTPSConnectionWithTimeout("westus.api.cognitive.microsoft.com")
                        conn.request("POST", "/luis/api/v2.0/apps/{0}/versions/0.1/examples".format(appid), json.dumps(utterances),headers)
                        response = conn.getresponse()
                        conn.close()
                        print(response.status)
                        result = response.status == 201
                    except Exception as e:
                        print(e)
                        result = False
    return result

addUtterances()