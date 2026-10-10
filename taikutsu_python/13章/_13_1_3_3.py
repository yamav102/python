#! python3
# P342
# _13_1_3_3.py
# ページを重ね合わせる
# カレントディレクトリに 
# meetingminutes.pdf, watermark.pdf を置いて実行
# 表紙ページに透かし画像を入れた watermarkedCover.pdf を出力する。
import PyPDF2 # py -m pip install PyPDF2==2.12.1
def main()->None:
    with open('meetingminutes.pdf', 'rb') as minutes_file:
        pdf_reader = PyPDF2.PdfFileReader(minutes_file)
        # 加工するページ
        minutesfirst_page = pdf_reader.pages[0]
        with open('watermark.pdf', 'rb') as watermark_file:
            pdf_watermark_reader = PyPDF2.PdfFileReader(watermark_file)
            # 透かし画像のページ
            watermark_page = pdf_watermark_reader.pages[0]
            # ページのマージ
            minutesfirst_page.merge_page(watermark_page)
            # 新規PDF
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.add_page(minutesfirst_page)
            for page_num in range(1, len(pdf_reader.pages)): # pdf_reader.numPages):← 非推奨
                page_obj = pdf_reader.pages[page_num]
                pdf_writer.add_page(page_obj)

                with open('watermarkedCover.pdf', 'wb') as pdf_out:
                    pdf_writer.write(pdf_out)
    print('done')

if __name__ == '__main__':
    main()