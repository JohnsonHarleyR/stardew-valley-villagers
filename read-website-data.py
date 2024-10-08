from bs4 import BeautifulSoup
import requests
import json

bachelors = ["Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane"]
bachelorettes = ["Abigail", "Emily", "Haley", "Leah", "Maru", "Penny"]
townspeople = ["Caroline", "Clint", "Demetrius", "Evelyn", "George", "Gil", "Gunther", "Gus",
                "Jas", "Jodi", "Kent", "Lewis", "Linus", "Marlon", "Marnie", "Morris", "Pam",
                "Pierre", "Robin", "Vincent", "Willy"]
other = ["Birdie", "Bouncer", "Dwarf", "Fizz", "Governor", "Grandpa", "Henchman",
         "Junimos", "Krobus", "Leo", "Mr. Qi" ,"Old Mariner", "Professor Snail",
        "Sandy", "Wizard"]

allCharacterNames = {
    "bachelors": bachelors,
    "bachelorettes": bachelorettes,
    "townspeople": townspeople,
    "other": other
}


def grabCharacterInformation(url):
    #get the page
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    #print(req.text)

    tables = soup.findAll("table")

    wantedTableInfos = [{
        "byAttribute": True,
        "attribute": "id",
        "value": "infoboxtable"
    },
    {
        "byAttribute": False,
        "attribute": "",
        "value": "Universal Loves"
    },
    {
        "byAttribute": False,
        "attribute": "",
        "value": "Universal Likes"
    },
    {
        "byAttribute": False,
        "attribute": "",
        "value": "Universal Neutrals"
    },
    {
        "byAttribute": False,
        "attribute": "",
        "value": "Universal Dislikes"
    },
    {
        "byAttribute": False,
        "attribute": "",
        "value": "Universal Hates"
    }]

    # def addToAttributeList(list, attributeName, attributeValue):
    #     list.append({"attribute": attributeName, "value": attributeValue})

    def addToAttributeDict(dict, attributeName, attributeValue):
        #list.append({"attribute": attributeName, "value": attributeValue})
        dict[attributeName] = attributeValue

    def hasAttributeAs(item, attribute, value):
        if(attribute in item.attrs and item.attrs[attribute] == value):
            return True
        return False

    def doesContainText(item, text):
        if text in item:
            return True
        return False

    def isWantedTable(table):
        for info in wantedTableInfos:
            if info["byAttribute"] and hasAttributeAs(table, info["attribute"], info["value"]):
                return True
            elif not info["byAttribute"] and doesContainText(str(table), info["value"]):
                return True
        return False

    def getWantedTableInfo(table):
        newInfo = {"isWanted": False, "category": ""}
        for info in wantedTableInfos:
            if info["byAttribute"] and hasAttributeAs(table, info["attribute"], info["value"]):
                newInfo["isWanted"] = True
                newInfo["category"] = "Basic"
            elif not info["byAttribute"] and doesContainText(str(table), info["value"]):
                newInfo["isWanted"] = True
                newInfo["category"] = info["value"]
        return newInfo

    wantedTables = []

    count = 1
    for table in tables:
        tableInfo = getWantedTableInfo(table)
        if tableInfo["isWanted"]:
            wantedTables.append({"table": table, "category": tableInfo["category"]})
        count = count + 1

    def isInfoTable(table):
        if hasAttributeAs(table, "id", "infoboxtable"):
            return True
        return False

    def getTableRows(table):
        rows = table.findAll("tr")
        return rows

    print("")

    # characterInfo = []
    characterInfo = {}
    for tableWithCategory in wantedTables:
        table = tableWithCategory["table"]
        category = tableWithCategory["category"]

        rows = getTableRows(table)
        if isInfoTable(table):
            count = 0
            for row in rows:
                cells = row.findAll("td")
                if count == 0:
                    #addToAttributeList(characterInfo, "Name", cells[0].text.strip())
                    addToAttributeDict(characterInfo, "Name", cells[0].text.strip())
                else:
                    valuesToKeep = ["Birthday", "Lives In", "Address", "Marriage"]
                    valueNameInRow = cells[0].text.strip()
                    if valueNameInRow in valuesToKeep:
                        newValue = cells[1].text.strip()
                        #addToAttributeList(characterInfo, valueNameInRow, newValue)
                        addToAttributeDict(characterInfo, valueNameInRow, newValue)
                count = count + 1
        else:
            rowCount = 0
            giftItems = []
            for row in rows:
                if rowCount != 1:
                    cellCount = 0
                    cells = row.findAll("td")
                    for cell in cells:
                        if cellCount == 1:
                            giftItems.append(cell.text.strip())
                            break
                        cellCount = cellCount + 1
                rowCount = rowCount + 1
            #addToAttributeList(characterInfo, category, giftItems)
            addToAttributeDict(characterInfo, category, giftItems)

    return characterInfo

def addCharactersByTypeToDict(characters, type, dict):
    characterInfos = []
    for character in characters:
        characterUrl = "https://stardewvalleywiki.com/" + character
        newCharacterInfo = grabCharacterInformation(characterUrl)
        #addToAttributeList(newCharacterInfo, "type", type)
        #newCharacterInfo["type"] = type
        # return newCharacterInfo
        characterInfos.append(newCharacterInfo)
        # print("Character info: ", newCharacterInfo)
        # print("")
    dict[type] = characterInfos

def createCharacterDict():
    characterTypes = list(allCharacterNames.keys())
    characterDict = {
        "characterTypes": characterTypes
    }
    for type in characterTypes:
        addCharactersByTypeToDict(allCharacterNames[type], type, characterDict)
    return characterDict

def formatString(string):
    return string.lower().strip()

def getInput(textToDisplay):
    return formatString(input(textToDisplay))

def convertToJson(dict):
    return json.dumps(dict, sort_keys=True, indent=4)

answer = getInput("Create dictionary of all Stardew Valley characters?(y/n): ")
filePath = "characters.txt"
if answer == 'y':
    characterDict = createCharacterDict()
    characterJson = convertToJson(characterDict)

    answer = getInput("Successfully created! Would you like to see it?(y/n): ")
    if answer == 'y':
        print(characterJson)

    answer = getInput("Would you like to write the new dictionary to a text file?(y/n): ")
    if answer == "y":
        with open(filePath, 'w') as convert_file: 
            convert_file.write(characterJson)
else:
    answer = getInput("Would you like to read the existing character data? (y/n): ")
    if answer == "y":
        with open(filePath, 'r') as file:
            try:
                data = json.load(file)
                print(convertToJson(data))
            except json.JSONDecodeError:
                print("Invalid JSON format in the file.")
