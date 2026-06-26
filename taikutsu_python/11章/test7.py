#! python3
# test7.py
import bs4
import os
os.chdir(r'E:\GitHub\yamaPythonScripts\11章\11_4')
with open('example.html','r') as example_file:
    example_soup = bs4.BeautifulSoup(example_file)
    p_elems = example_soup.select('p')
    print(f'len(p_elems): {len(p_elems)}')
    print(f'str(p_elems[0]): {str(p_elems[0])}')
    print(f'p_elems[0].getText(): {p_elems[0].getText()}')
    print(f'str(p_elems[1]): {str(p_elems[1])}')
    print(f'p_elems[1].getText(): {p_elems[1].getText()}')
    print(f'str(p_elems[2]): {str(p_elems[2])})')
    print(f'p_elems[2].getText(): {p_elems[2].getText()}')