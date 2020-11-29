import pandas as pd
from PIL import Image
import requests
from bs4 import BeautifulSoup

#DECLARING VARIABLES
name = []
degree = []
degree_f = []
career = []
career_f= []
membership = []
membership_f = []
skills = []
skills_f = []
goal = []
goal_f = []
certification = []
certification_f = []
image_url = []
img = []


#Scraping links from HOMEPAGE
page1 =requests.get('https://www.myvisajobs.com/CV/Candidates.aspx')
soup1 = BeautifulSoup(page1.content, 'html.parser')
table1 = soup1.find(id='ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent')
items1 = table1.find_all('tr')
main1 = items1[1::2]
main1.remove((items1[1]))
links = []
test_links1 = []
for link in table1.find_all('a'):
    test_links1.append(link.get('href'))

for i in test_links1:
    if i not in links:
        links.append(i)


#DEFINING FUNCTION TO SCRAPE LINKS FROM ALL OTHER PAGES
def f():
  soup1 =BeautifulSoup(page1.content,'html.parser')
  table1=soup1.find(id='ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent')
  items1=table1.find_all('tr')
  main1=items1[1::2]
  main1.remove((items1[1]))
  test_links1 = []

  for link in table1.find_all('a'):
    test_links1.append(link.get('href'))

  for i in test_links1:
    if i not in links:
        links.append(i)

#SCRAPING LINKS
for i in range(2,12 ):
    page1 =requests.get('https://www.myvisajobs.com/CV/Candidates.aspx?P='+str(i))
    f()

#REMOVING OTHER LINKS
links=[x for x in links if not '.aspx' in x]

links.pop(103)
links.pop(102)
links.pop(101)
links.pop(100)

#GATHERING DATA FOR REQUIRED FIELDS BY LOOPING THROUGH THE 100 PAGES
for link in links:
    page = requests.get('https://www.myvisajobs.com'+ link)
    soup = BeautifulSoup(page.content, 'html.parser')
    name.append(soup.find('h3').get_text())
    tables = soup.find_all('table')
    a = []

    #SAVING IMAGES
    image = soup.find_all('img')
    image_url.append(image[1]['src'])

    for i in image_url:
        img.append(Image.open(requests.get('https://www.myvisajobs.com'+i, stream=True).raw))

    for i in img:
        i.save(soup.find('h3').get_text()+'.jpg')

    #GATHERING ALL OTHER FIELDS
    for entry in tables[14]:
        a.append(entry.get_text())


    degree = degree+[x for x in a if 'Degree' in x]
    career = career+[x for x in a if 'Career Level' in x]

    found_mem = False
    for i in a:
      if 'Membership' in i:
         membership.append(i)
         found_mem = True
         break

    if (found_mem== False):
       membership.append("NA")

    found_skills = False
    for i in a:
        if 'Skills' in i:
            skills.append(i)
            found_skills = True
            break

    if (found_skills == False):
        skills.append("NA")

    found_goal = False
    for i in a:
      if 'Goal' in i:
         goal.append(i)
         found_goal = True
         break

    if (found_goal == False):
       goal.append("NA")


    found_cert = False
    for i in a:
      if 'Certification' in i:
         certification.append(i)
         found_cert = True
         break

    if (found_cert == False):
       certification.append("NA")


#EDITING DATA TO CONVERT INTO TABLE FORMAT
for i in degree:
        splitRet = i.split(':',1)
        if (len(splitRet) < 2):
            print ("Igonring>>", i)
            continue

        degree_f.append(splitRet[1])

for i in degree_f:
    if len(i)>30:
        degree_f.remove(i)

for i in career:
    if len(i.split(':',1)[1]) > 5:
      career_f.append(i.split(':',1)[1])
    else:
      career_f.append('NA')

for i in membership:
    if ':' in i:
      membership_f.append(i.split(':',1)[1])
    else:
      membership_f.append(i)

for i in skills:
    if ':' in i:
      skills_f.append(i.split(':',1)[1])
    else:
      skills_f.append(i)

for i in goal:
    if ':' in i:
      goal_f.append(i.split(':',1)[1])
    else:
      goal_f.append(i)

for i in certification:
    if ':' in i:
      certification_f.append(i.split(':',1)[1])
    else:
      certification_f.append(i)

#CONVERTING DATA TO CSV FILE USING PANDAS
CV = pd.DataFrame(
  {
    'Name': name,
    'Degree': degree_f,
    'Career Level': career_f,
    'Membership': membership_f,
    'Skills': skills_f,
    'Goals': goal_f,
    'Certification': certification_f,
  })

print(CV)
CV.to_csv('webscrape.csv')
