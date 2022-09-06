from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv


list_name = []
list_abbrev = []
list_place = []
list_id = []
list_code = []
list_dpt = []
list_auth = []
list_scoreYr = []
list_scoreOv = []

tab = range(1,533)
title = [ 
    'name','place','id','code','departement','authors','scoreYr','scoreOv'
 ]
for i in tab:
  link = 'https://sinta.kemdikbud.go.id/affiliations?page='+str(i)
  html = urlopen(link).read()
  besoup = BeautifulSoup(html,'lxml')
  item = besoup.find_all('div','list-item row mb-4')
  for i in item:
    #! name
    name = i.find('div','affil-name').get_text()
    name = name.replace('\n' ,'').rstrip()
    list_name.append(name)
    #! abbrev
    abbrev = i.find('div','affil-abbrev').get_text()
    abbrev = abbrev.replace('\n' ,'').rstrip()
    abbrev = abbrev.replace(' ' ,'')
    list_abbrev.append(abbrev)
    #! place
    place = i.find('div','affil-loc mt-2').get_text()
    place =place .replace('\n' ,'').rstrip()
    list_place.append(place)
    #! id
    id = i.find('div','profile-id').get_text()
    id = id.split(' ')
    id = int(id[3])
    list_id.append(id)
    #! code
    code = i.find('div','profile-id').get_text()
    code = code.split(' ')
    code = code[-1]
    list_code.append(code)
    #! dpt
    dpt = i.find('span',' num-stat').get_text()
    dpt = dpt.replace('Department','').rstrip()
    list_dpt.append(int(dpt))
    #! auth
    auth = i.find('span',' num-stat ml-3').get_text()
    auth = auth.replace('Authors','').replace(',','')
    list_auth.append(int(auth))
    #score
    score = i.find('div','pr-bottom row').get_text()
    score = score.split('\n')
    # print(score)
    #scoreYr
    scoreYr =score[2].replace('.','',2)
    list_scoreYr.append(int(scoreYr))
    #scoreOV
    scoreOv = score[-4].replace('.','',2)
    list_scoreOv.append(int(scoreOv))

# print('name')
# print(list_name)
# print('abbrev')
# print(list_abbrev)
# print('place')
# print(list_place)
# print('id')
# print(list_id)
# print('code')
# print(list_code)
# print('departement')
# print(list_dpt)
# print('authors')
# print(list_auth)
# print('scoreYr')
# print(list_scoreYr)
# print('scoreOv')
# print(list_scoreOv)

# print('Crawling Success')

create_dict = { 'Name':list_name , 'Abbrev':list_abbrev , 'Place':list_place , 'Id':list_id , 'Code':list_code, 'Department':list_dpt,
               'Authors':list_auth,'Score 3 Yr':list_scoreYr,'Score Overall':list_scoreOv}
data_frame = pd.DataFrame(create_dict)
# data_frame

data_frame.to_csv('sinta_kemdikbud.csv',sep=',',index=False)
data_frame.to_excel('sinta_kemdikbud',index=False)