#! python3
# test5.py
import bs4
import os
os.chdir(r'E:\GitHub\yamaPythonScripts\11章\11_4')
with open('example.html','r') as example_file:
    example_soup = bs4.BeautifulSoup(example_file)
    elems = example_soup.select('#author')
    print(f'type(elems):{type(elems)}')
    print(f'len(elems):{len(elems)}')
    print(f'type(elems[0]):{type(elems[0])}')
    print(f'elems[0].getText():{elems[0].getText()}')
    print(f'str(elems[0]):{str(elems[0])}')
    print(f'elems[0].attrs:{elems[0].attrs}')
    