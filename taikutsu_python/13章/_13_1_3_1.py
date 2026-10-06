#! python3
# P339 13.1.3
# 2つの PDF のページをコピーして、新規PDFにまとめて出力する。
# meetigminutes.pdf と meentingminutes2.pdf をカレントディレクトリに置いて実行
# combinedminutes.pdf が作成される。
# python -m pip install PyPDF2==2.12.1
import PyPDF2
def append_pages(reader: PyPDF2.PdfReader, writer: PyPDF2.PdfWriter)-> None:
    for page in reader.pages: # add_page は末尾に追加のみ
        writer.add_page(page)

def main()->None:
    writer = PyPDF2.PdfWriter()
    with ( 
        open('meetingminutes.pdf', 'rb') as f1, 
        open('meetingminutes2.pdf', 'rb') as f2
    ):        
        append_pages(PyPDF2.PdfReader(f1), writer)
        append_pages(PyPDF2.PdfReader(f2), writer)
        with open('combinedminutes.pdf', 'wb') as pdf_output_file:
            writer.write(pdf_output_file)
    print('done')

if __name__ == '__main__':
    main()
