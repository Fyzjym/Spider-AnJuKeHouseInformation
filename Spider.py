# -*- coding: utf-8 -*-
# author:           GitHub：Fyzjym
# pc_type           Msi
# create_time:      2020/2/17
# file_name:        spider.py
# qq邮箱            2261013403@qq.com

from lxml import etree
from xlutils.copy import copy
import requests
import time
import random
import xlrd
import xlwt

fakerHeaders = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}


def run(url):
    """

    @param url: 总url，既包含房屋信息的url
    @return:
    """
    resp = requests.get(url, headers = fakerHeaders, timeout = 10)
    time.sleep(random.randint(5,10))
    print(resp.status_code)
    if(resp.status_code == 200):
        print("get this.", url)
        xpathGetHouseInfo(resp.text)
    else:
        print("wrong in :", url)

def xpathGetHouseInfo(text):
    """

    @param text: 解析总url返回的文本，利用xpath降噪弄出单个二手房信息url
    @return:
    """
    html = etree.HTML(text)
    resultHouseLinkList = html.xpath('//ul[@id="houselist-mod-new"]//a//@href')

    for iurl in resultHouseLinkList:
        try:
            getInf_And_xpathNoiseReduction(iurl)
        except:
            print("wrong in here.", iurl)
            getInf_And_xpathNoiseReduction(iurl)



    #print(resultHouseLinkList)
    #return resultHouseLinkList


def getInf_And_xpathNoiseReduction(url):
    """

    @param url: 根据单个二手房信息url  请求并解析出此url下的房屋信息
    @return:
    """

    resp = requests.get(url, headers = fakerHeaders, timeout = 10)
    time.sleep(random.randint(6,7))
    #print(resp.status_code)
    if(resp.status_code == 200):
        text = resp.text

        html = etree.HTML(text)

        # 标题 处理
        resultTitle1 = html.xpath('//h3//text()')[0]
        resultTitle2 = str(resultTitle1).replace(" ", "")
        resultTitle = str(resultTitle2).replace("\n", "")

        # 小区 处理
        resultVillage = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[1]//text()')[4]
        # print(resultVillage)

        # 位置 处理
        resultPosition1 = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[4]//text()')[4]
        resultPosition2 = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[4]//text()')[6]
        resultPosition3 = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[4]//text()')[7]
        resultPosition3 = str(resultPosition3).replace(" ", "")
        resultPosition3 = str(resultPosition3).replace("－\n", "")
        resultPosition = resultPosition1 + resultPosition2 + resultPosition3

        # 楼层处理
        resultFloor = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[11]//text()')[3]

        # 建造年份
        resultConstructionAge1 = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[7]//text()')[3]
        resultConstructionAge2 = str(resultConstructionAge1).replace("\n", '')
        resultConstructionAge = str(resultConstructionAge2).replace("	", '')

        # 面积
        resultArea = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[5]//text()')[3]

        # 朝向
        resultDirection = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[8]//text()')[3]

        # 户型
        resultLayout1 = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[2]//text()')[3]
        resultLayout2 = str(resultLayout1).replace("\n", '')
        resultLayout = str(resultLayout2).replace("	", '')

        # 总价
        resultTotalPrice = html.xpath('//span/em//text()')[0]

        # 单价
        resultUnitPrice1 = html.xpath('//ul[@class="houseInfo-detail-list clearfix"]/li[3]//text()')[3]
        resultUnitPrice = str(resultUnitPrice1).replace(" ", '')
        bigList = []

        infoList = []
        infoList.append(resultTitle)
        infoList.append(resultVillage)
        infoList.append(resultPosition)
        infoList.append(resultFloor)
        infoList.append(resultConstructionAge)
        infoList.append(resultArea)
        infoList.append(resultDirection)
        infoList.append(resultLayout)
        infoList.append(resultTotalPrice)
        infoList.append(resultUnitPrice)
        print(infoList)
        bigList.append(infoList)

        writeExcelXlsAppend(nameXls,bigList)
        #print(resultTitle, resultVillage, resultPosition, resultFloor, resultConstructionAge, resultArea, resultDirection, resultLayout, resultTotalPrice, resultUnitPrice)
        #return resultTitle, resultVillage, resultPosition, resultFloor, resultConstructionAge, resultArea, resultDirection, resultLayout, resultTotalPrice, resultUnitPrice
        return True
    else:
        print("wrong here",resp.url)

def writeExcelXls(path, sheetName, value):
    """
    :param path: 表格路径
    :param sheetName: 表名
    :param value: 页内表头数据
    :return:
    """
    index = len(value)  # 获取需要写入数据的行数
    workBook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workBook.add_sheet(sheetName)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workBook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")



def writeExcelXlsAppend(path, value):
    """
    :param path: 表路径
    :param value: 页内list行数据
    :return:
    """
    index = len(value)  # 获取需要写入数据的行数
    workBook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workBook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workBook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workBook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")



if __name__ == '__main__':

    # ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊ Excel表操作 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
    # 路径
    nameXls = 'AnJuKeInfoFinal.xls'
    # 表名
    sheetNameXls = 'AnJuKe'
    # 表头定义
    valueTitle = [["Title", "Village", "Position", "Floor", "ConstructionAge", "Area", "Direction", "Layout", "TotalPrice", "UnitPrice"]]
    # 写表－格式－表头
    writeExcelXls(nameXls, sheetNameXls, valueTitle)



    # 终止页面数， 安居客网站限制max为 50 。
    pageNumber = 50

    # 起始爬取页面数
    startNumber = 1

    for ipageNumber in range(startNumber, pageNumber+1):

        try:
            url = "https://nc.anjuke.com/sale/p"+str(ipageNumber)+"/#filtersort"
            run(url)
        except:
            print("wrong here. ", url)
            run(url)



