# python3
# usecensus2010_sample.py
# census2010.py を使うサンプル
# all_data = {'AK': {'Aleutians East': {'pop': 3141, 'tracts': 1},
#         'Aleutians West': {'pop': 5561, 'tracts': 2},
#         'Anchorage': {'pop': 291826, 'tracts': 55},
# ...
import census2010 as cnss
d = cnss.all_data['AK']['Aleutians East']
print(d['pop'], d['tracts']) # 3141 1
for d in cnss.all_data:
    print(d) # 州
for state, counties in cnss.all_data.items():
    # print(state + '\n---------------')
    for county in counties:
        d = cnss.all_data[state][county]
        print(f"{state}:{county} 人口:{d['pop']:,} 集計地区数:{d['tracts']:,}")
# ...        
# OR:Wallowa 人口:7,008 集計地区数:3
# OR:Wasco 人口:25,213 集計地区数:8
# OR:Washington 人口:529,710 集計地区数:104
# OR:Wheeler 人口:1,441 集計地区数:1
# OR:Yamhill 人口:99,193 集計地区数:17
# PA:Adams 人口:101,407 集計地区数:23
# PA:Allegheny 人口:1,223,348 集計地区数:402
# PA:Armstrong 人口:68,941 集計地区数:19
# PA:Beaver 人口:170,539 集計地区数:51
# ...
