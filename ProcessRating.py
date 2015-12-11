from bs4 import BeautifulSoup


soup = BeautifulSoup(load_from_file('rating.txt'), 'lxml')
content = soup.body.find("div", {"id": "tn15content"})
for link in soup(["a"]):
    link.replaceWithChildren()
for bold in soup(["b"]):
    bold.replaceWithChildren()
for images in soup(["img"]):
    images.extract()

for table in content(["table"]):
    print(table)
    print("")
    print("new one:")

tables = content(["table"])
print(tables[0])

tabResults = []
for line in tables[0](["tr"]):
    cols = [ele.text.strip() for ele in line(["td"])]
    tabResults.append(cols)

print(tabResults)




