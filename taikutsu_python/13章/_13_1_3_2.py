#! python3
# _13_1_3_2.py
# ページを回転する
# カレントディレクトリに 'meetingminutes.pdf' を置いて実行
# 時計回りに90度回転して1ページ目で rotatedPage.pdf が作成される
import PyPDF2 # py -m pip install PyPDF2==2.12.1

def main()->None:
    with open('meetingminutes.pdf', 'rb') as minutes_file:
        pdf_reader = PyPDF2.PdfFileReader(minutes_file)
        page = pdf_reader.pages[0]
        page.rotate_clockwise(90) # 時計回り
        
        # 新規PDF
        pdf_writer = PyPDF2.PdfFileWriter() 
        pdf_writer.addPage(page)

        with open('rotatedPage.pdf', 'wb') as outfile:
            pdf_writer.write(outfile)
        
        print('done')
if __name__ == '__main__':
    main()
