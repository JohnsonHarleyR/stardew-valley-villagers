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

count = 1
for table in tables:
    if count < 5:
        print("Table", count)
        # print(table)
        # print("")
        attributes = table.attrs
        print("Attributes: ", attributes)
        if ("id" in attributes):
            print("Table has id!")
        print("")
    # tag = BeautifulSoup(table, 'html.parser').table
    # tag['id']
    #print("Table", count)
    count = count + 1
    # print(table)
    # if table['id'] == 'infoboxtable':
    #     print(table)

#print (req.text)
# trs = soup.find_all('tr')
# comment = trs[-1].find_next(string=lambda text: isinstance(text, Comment))
# table_soup = BeautifulSoup(comment, "html.parser")

# for tr in table_soup.find_all('tr'):
#     print([td.text for td in tr.find_all('td')])