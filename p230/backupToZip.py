#! python3
# フォルダ全体を連番付きZIPファイルにコピーする

import zipfile, os
from pathlib import Path
 
def backup_to_zip(folderpath: str)-> None:
    # フォルダ全体をZIPファイルにバックアップする

    folder = Path(folderpath) # pathオブジェクト

    # 既存のファイル名からファイル名の連番を決める
    number = 1
    while True:
        zip_filename = folder.stem + '_' + str(number) + '.zip'
        if not os.path.exists(zip_filename):
            break
        number += 1
    # TODO: ZIPファイルを作成する
    print('Creating {}...'.format(zip_filename))
    backup_zip = zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED)
    
    # TODO: フォルダのツリーを私歩いてその中のファイルを圧縮する
    for foldername, subfolders, filenames in os.walk(folderpath):
        print('Adding files in {}...'.format(foldername))        
        # 現在のフォルダをZIPファイルに追加する
        backup_zip.write(foldername)
        # 現在のフォルダの中野全ファイルをZIPファイルに追加する
        for filename in filenames:
            new_base = folder.stem + '_'
            # バックアップ用ZIPファイルはバックアップしない
            if filename.startswith(new_base) and filename.endswith('.zip'):
                continue
            print('Adding {}'.format(filename))
            backup_zip.write(os.path.join(foldername, filename))
    backup_zip.close()
    print('Done')
