from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv

"""## CRAWLING DATA Affiliations"""

list_name ,list_abbrev ,list_place ,list_id ,list_code ,list_dpt ,list_auth ,list_scoreYr ,list_scoreOv = [],[],[],[],[],[],[],[],[]
tab = range(1,533)
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

print('Crawling Affiliations Success')

"""## Create and Write CSV Affilations"""

create_dict = { 'Name':list_name , 'Abbrev':list_abbrev , 'Place':list_place , 'Id':list_id , 'Code':list_code, 'Department':list_dpt,
               'Authors':list_auth,'Score 3 Yr':list_scoreYr,'Score Overall':list_scoreOv}
data_frame = pd.DataFrame(create_dict)
data_frame

data_frame.to_csv('sinta_kemdikbud_affiliations.csv',sep=',',index=False)
print('sinta_kemdikbud_affiliations.csv telah dibuat')

"""## CRAWLING DATA DEPARTMENT"""

list_name_affil , list_level_dpt ,list_name_dpt ,list_authors_dpt , list_code_dpt , list_scoreYr_dpt , list_scoreOv_dpt = [],[],[],[],[],[],[]
tab = range(1,500)
runn=0

try:
  for idcode in range(len(list_name)):
    affil = list_name[idcode]
    id = list_id[idcode]
    code = list_code[idcode]
    print('\n')
    print(affil)
    for pages in tab:
      link_dpt = 'https://sinta.kemdikbud.go.id/affiliations/departments/'+str(id)+'/'+str(code)+'?page='+str(pages)
      html = urlopen(link_dpt).read()
      besoup = BeautifulSoup(html,'lxml')
      item = besoup.find_all('div','row d-item mb-4 pb-2 mt-3')
      if item == []:
        break
      for i in item:
        list_name_affil.append(affil)
        #! level_dpt
        level_dpt = i.find('div','col-lg-1 tbl-content-meta mb-2').get_text()
        level_dpt = level_dpt.replace('\n' ,'').rstrip()
        list_level_dpt.append(level_dpt)

        #! name_dpt
        name_dpt = i.find('a',).get_text()
        name_dpt = name_dpt.replace('\n' ,'').rstrip()
        list_name_dpt.append(name_dpt)

        #! authors dpt
        authors = i.find('li','au-more')
        auth = i.find_all('img','img-aut-prev')
        if authors != None:
          authors = authors.get_text()
          authors = authors.split(' ')
          if authors[1] == 'No':
            authors = 0
          else:
            authors = int(authors[1])
        elif authors == None:
          authors = 0
        total_authors = len(auth) + authors
        list_authors_dpt.append(total_authors)
        #! code_dpt
        code_dpt = i.find('div','tbl-content-meta-num').get_text()
        code_dpt = code_dpt.replace(' ' ,'').rstrip()
        list_code_dpt.append(int(code_dpt))
        #score
        score_dpt = i.find('div','profile-hindex').get_text()
        score_dpt = score_dpt.replace(' ' ,'').rstrip()
        score_dpt = score_dpt.split('\n')
        # print(score_dpt)
        #! scoreYr_dpt
        scoreYr_dpt = score_dpt[-1]
        scoreYr_dpt = scoreYr_dpt.replace('SINTAScore3Yr:','')
        list_scoreYr_dpt.append(int(scoreYr_dpt))
        #! scoreOv_dpt
        scoreOv_dpt = score_dpt[2]
        scoreOv_dpt = scoreOv_dpt.replace('SINTAScoreOverall:','')
        list_scoreOv_dpt.append(int(scoreOv_dpt))
        runn+=1
        print(runn,end=" ")

print('Crawling Affiliations Departments Success')

except:
  print('error in crawlling data : ',end='')
  print(affil)
  print(runn)

"""##CREATE CSV DEPARTMENTS"""

create_dict_dpt = { 'Affiliations':list_name_affil , 'Level':list_level_dpt , 
                   'Department':list_name_dpt , 'Authors':list_authors_dpt , 
                   'Code ':list_code_dpt, 'Score 3 Yr':list_scoreYr_dpt,'Score Overall':list_scoreOv_dpt}
data_frame_dpt = pd.DataFrame(create_dict_dpt)
data_frame_dpt

data_frame_dpt.to_csv('sinta_kemdikbud_departments.csv',sep=',',index=False)
print('sinta_kemdikbud_departments.csv telah dibuat')