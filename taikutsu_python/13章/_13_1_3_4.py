#! python3
# P343
# _13_1_3_4.py
# PDF を暗号化する(パスワードを設定する)
import PyPDF2 # py -m pip install PyPDF2==2.12.1
from typing import Final
from pathlib import Path
OUT_PDF_NAME:Final = 'encryptedminutes.pdf'
def main()->None:
    with open('meetingminutes.pdf', 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        pdf_writer.encrypt('swordfish')
        with open(OUT_PDF_NAME, 'wb') as pdf_out:
            pdf_writer.write(pdf_out)
    print('done')        
if __name__ == '__main__':
    if (Path(__file__).parent / OUT_PDF_NAME).exists():
        print(f'{OUT_PDF_NAME} は、既に存在します。')
    else:
        main()