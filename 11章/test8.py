# test8.py
# P277 11.4.3
import bs4
import os
os.chdir(r'E:\GitHub\yamaPythonScripts\11章\11_4')
with open('example.html', 'r') as example_file:
    soup = bs4.BeautifulSoup(example_file)
    span_elem = soup.select('span')[0]
    print(f'str(span_elem): {str(span_elem)}')
    print(f'span_elem.get("id"): {span_elem.get('id')}')
    print(
        f'span_elem.get("hoge")==None:'
        f'{span_elem.get("hoge")==None}'
        )
    print(f'span_elem.attrs: {span_elem.attrs}')
    
