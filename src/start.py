import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from shutil import copy2
import importlib
import sys
import time
importlib.reload(sys)
time1 = time.time()

import os.path
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
src_dir = 'G:/九江事业单位/时政/2020_07_18/'  # 源文件目录地址
des_dir = 'G:/九江事业单位/时政/test/'
num = 0

if not os.path.exists(des_dir):  # 如果没有目标文件夹,新建一个目标文件夹进行存储
    os.makedirs(des_dir)

if os.path.exists(src_dir):
    dirs = os.listdir(src_dir)  # 获取源文件的目录地址
    for dirc in dirs:  # 对于目录下的每一个文件
        '''解析PDF文本，并保存到TXT文件中'''
        fp = open(src_dir+dirc, 'rb')
        # pdf1 = urlopen('http://www.tencent.com/20160321.pdf')
        # 用文件对象创建一个PDF文档分析器
        parser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器，与文档对象
        parser.set_document(doc)
        doc.set_parser(parser)

        # 提供初始化密码，如果没有密码，就创建一个空的字符串
        doc.initialize()


        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        pages = doc.get_pages()
        for page in pages:
            break_all = False
            try:
                interpreter.process_page(page)
            except KeyError:
                print(str(dirc)+"损坏")
                break
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    print(results)
                    break_all = True
                    break
            if break_all:
                break
        paper_title = results.replace('\n' , '')
        copy2(os.path.join(src_dir, dirc), os.path.join(des_dir, paper_title) + '.pdf')
else:
    print("该路径下不存在所查找的目录!")






