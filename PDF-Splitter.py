############################################
# 작성자 : 윤정도
# 작성일 : 21-11-04
# 사용목적 : PDF 파일을 페이지마다 분리하여 이미지로 저장한다.
# 사용한 라이브러리 : https://github.com/Belval/pdf2image
############################################

import argparse
import os;
from PIL import Image 
from os import path;
from pathlib import Path
import ntpath
from pdf2image import convert_from_path


from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdfFilePath", help="<PDF 파일 경로>")
    parser.add_argument("threadCount", help="<이미지 분할에 사용할 쓰레드 수>", type=int)
    args = parser.parse_args()
except:
    print('사용방법 : {0} <PDF 파일 경로> <이미지 분할에 사용할 쓰레드 수>'.format(path.basename(__file__)))
    exit(-2)

filePath = args.pdfFilePath;
threadCount = args.threadCount;
popplerPath = 'poppler/Library/bin'

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or '';

# 파일명에서 확장자명을 제외하고 이름 얻기
# @ https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python?rq=1
fileNameWithoutExtensionPath = path.splitext(filePath)[0]
fileNameWithoutExtensionOnlyName = path_leaf(fileNameWithoutExtensionPath);

# 경로가 존재하지 않으면 생성하도록 
# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python

# python 3.5 >=
# Path(fileNameWithoutExtension).mkdir(parents=True, exist_ok=True)
# 그 이하 버전에서
try:
    if not path.exists(fileNameWithoutExtensionOnlyName):
        os.makedirs(fileNameWithoutExtensionOnlyName);

    images = convert_from_path(pdf_path=filePath, 
                            thread_count=threadCount, 
                            poppler_path=popplerPath,
                            fmt='jpeg');

    totalCount = len(images);
    count = 0
    for img in images:
        count += 1
        img.save(fileNameWithoutExtensionOnlyName + '/{0:04d}.jpeg'.format(count))
        
    print('작업완료 {}/{}', count, totalCount)
    exit(0)
except Exception as e:
    # 파이썬 예외 캐치 방법
    # https://stackoverflow.com/questions/4690600/python-exception-message-capturing
    print(str(e))
    exit(-1)
