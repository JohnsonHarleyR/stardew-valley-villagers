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

wantedTables = []

count = 1
for table in tables:
    if isWantedTable(table):
        wantedTables.append(table)
        print("Table", count, "is wanted!")
        print(table)
        print("")
    count = count + 1

print ("Wanted tables count: ", len(wantedTableInfos), "Found: ", len(wantedTables))
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