from bs4 import BeautifulSoup, Comment
import requests

#test reading a page

#get the page
url = "https://stardewvalleywiki.com/Abigail"
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
#print(req.text)

tables = soup.findAll("table")
#tables = BeautifulSoup(req.content, "html.parser").table
#print(tables)

#determines if it should identify the table by an attribute or by containing specific text
wantedTableInfos = [{
    "byAttribute": True,
    "attribute": "id",
    "value": "infoboxtable"
},
{
    "byAttribute": False,
    "attribute": "",
    "value": "Universal Loves"
}]

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
    #print("Table Info", tableInfo)
    if tableInfo["isWanted"]:
        #wantedTables.append(table)
        wantedTables.append({"table": table, "category": tableInfo["category"]})
        print("Table", count, "is wanted!")
        #print(table)
        print("")
    count = count + 1

print("Wanted tables count: ", len(wantedTableInfos), "Found: ", len(wantedTables))

def isInfoTable(table):
    if hasAttributeAs(table, "id", "infoboxtable"):
        print('Found infoboxtable!')
        return True
    return False

def getTableRows(table):
    rows = table.findAll("tr")
    return rows

def addCellToAttributeList(list, attributeName, cellText):
    list.append({"attribute": attributeName, "value": cellText})

print("")

characterInfo = []
for tableWithCategory in wantedTables:
    #print("tableWithCategory", tableWithCategory)
    table = tableWithCategory["table"]
    category = tableWithCategory["category"]

    rows = getTableRows(table)
    tableInfo = {"category": category, "information": []}
    if isInfoTable(table):
        count = 0
        for row in rows:
            cells = row.findAll("td")
            #print("infoboxtable cells for row", count, ":", cells)
            if count == 0:
                #infoTableValues.append({"attribute": "Name", "value": cells[0].text})
                addCellToAttributeList(tableInfo["information"], "Name", cells[0].text.strip())
                print("Name: ",  cells[0].text)
            else:
                valuesToKeep = ["Birthday", "Address", "Marriage"]
                valueNameInRow = cells[0].text.strip()
                if valueNameInRow in valuesToKeep:
                    newValue = cells[1].text.strip()
                    addCellToAttributeList(tableInfo["information"], valueNameInRow, newValue)
                    print("Found attribute", valueNameInRow, ":", newValue)
            count = count + 1
        print("infotable values: ", tableInfo)

    characterInfo.append(tableInfo)
    
        #print("rows for infoboxtable: ", rows)
print("Character info: ", characterInfo)

# count = 1
# for table in tables:
#     if count < 5:
#         print("Table", count)
#         # print(table)
#         # print("")
#         attributes = table.attrs
#         print("Attributes: ", attributes)
#         if ("id" in attributes):
#             print("Table has id: ", attributes["id"])
#             if hasAttributeAs(table, "id", "infoboxtable"):
#                 print("Id is infoboxtable")
#         print("")
#     count = count + 1