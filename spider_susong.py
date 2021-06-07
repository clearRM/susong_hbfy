# -*- coding: utf-8 -*-
import requests
import configparser
import datetime
import csv
import random
from lxml import etree
import time


config = configparser.ConfigParser()
cr = config.read("config.ini")
input_time = config.get("date","from")
config_pageNums = config.get("pageNums","Nums")
if input_time:
	now_time = datetime.datetime.now()
	input_time = datetime.datetime(int(input_time[1:5]),int(input_time[6:8]),int(input_time[9:11]))
	days = (now_time - input_time).days + 1
pageNums = days*70 if input_time else int(config_pageNums)
print('欢迎使用社会公众案件查询程序!')
print('共需下载 %s 页, 预计耗时 %s 分钟。' % (str(pageNums),str(int(pageNums*10/60)+1)))

url = "http://susong.hbfy.gov.cn/gfcms/templetPro.do?templetPath=caze/CaseOpenList.html"
User_Agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
				   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
				   "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
				   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
				   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
				   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
				   "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
				   "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
				   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
				   "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
				   "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
				   "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
				   "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
				   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
				   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
				   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
				   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
				   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
				   "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
				   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
				   "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"]
Cookie_list = ["JSESSIONID=49141CF14E30E32F934DA635C5CCCD2E; JSESSIONID=00F1A42EA2C35DE79F8530C74B27EFE9",
			   "JSESSIONID=A2226BBCC356171EACA8FDC5A37B343F; JSESSIONID=1542DC98F699389B3EDC0E48964B7DB0",
			   "JSESSIONID=250408ECDE0089BFB556ABA95B029014; JSESSIONID=EDADD8C988A45C783D2EE65DB044C9B1",
			   "JSESSIONID=0E4BBB997B7ED4DC4FB655644516771D",
			   "JSESSIONID=DA8F1F77AF14EE8E0E01B3A0D052A76F; JSESSIONID=C8CAC1D9DBE1B423CAE4506FC1C8DA3F"]

headers = {
	"User-Agent": random.choice(User_Agent_list),
	"Content-Type": "application/x-www-form-urlencoded",
	"Referer": "http://susong.hbfy.gov.cn/gfcms/templetPro.do?templetPath=caze/CaseOpenList.html",
	"Host": "susong.hbfy.gov.cn",
	# "Connection": "keep-alive",
	"Cache-Control": "max-age=0",
	"Accept-Language": "zh-CN,zh;q=0.9",
	"Accept-Encoding": "gzip, deflate",
	"Cookie": random.choice(Cookie_list)}
csv_headers = ['案件','原告','被告','立案日期','结案日期','状态']
csv_rows = []


def spider(pages=False):
	error_pages = []
	if pages:
		for page in pages:
			print('正在下载第 %s 页' % page)
			formdata = {
				"page": page,
				"currChannelid": "f4df0408-34cb-4799-8b03-705e17b815f1",
				"siteid": "ce0b9496-6b88-4f66-8da7-ede1a989fd6e",
				"pageNum": page - 1
			}
			try:
				response = requests.post(url, data=formdata, headers=headers)
				content = etree.HTML(response.text)
				for info in content.xpath('//table[@class="zebra"]')[0].xpath('tr'):
					info_list = str(info.xpath('string(.)')).replace('\n\t\t\t\t\t\t', 'x').replace('\n\t\t\t\t\t',
																									'x').split('x')
					anjian = "".join(info_list[1].split())
					yuangao = "".join(info_list[2].split())
					beogao = "".join(info_list[3].split())
					lianriqi = "".join(info_list[4].split())
					jieanriqi = "".join(info_list[5].split())
					zhuangtai = "".join(info_list[6].split())
					list_val = [anjian, yuangao, beogao, lianriqi, jieanriqi, zhuangtai]
					csv_rows.append(list_val)
				print('第 %s 页下载成功' % page)
			except:
				pass
	else:
		for page in range(1,pageNums):
			print('正在下载第 %s 页' % page)
			formdata = {
				"page": page,
				"currChannelid":"f4df0408-34cb-4799-8b03-705e17b815f1",
				"siteid":"ce0b9496-6b88-4f66-8da7-ede1a989fd6e",
				"pageNum": page - 1
			}
			try:
				response = requests.post(url, data = formdata, headers = headers)
				content = etree.HTML(response.text)
				for info in content.xpath('//table[@class="zebra"]')[0].xpath('tr'):
					info_list = str(info.xpath('string(.)')).replace('\n\t\t\t\t\t\t','x').replace('\n\t\t\t\t\t','x').split('x')
					anjian = "".join(info_list[1].split())
					yuangao = "".join(info_list[2].split())
					beogao = "".join(info_list[3].split())
					lianriqi = "".join(info_list[4].split())
					jieanriqi = "".join(info_list[5].split())
					zhuangtai = "".join(info_list[6].split())
					list_val = [anjian,yuangao,beogao,lianriqi,jieanriqi,zhuangtai]
					csv_rows.append(list_val)
				response.close()
				# 必要的时间限制 否则会被屏蔽
				# time.sleep(3)
				print('第 %s 页下载成功!' % page)
			except:
				print('第 %s 页下载失败,过后自动重新下载。' % page)
				error_pages.append(page)
	return error_pages

if __name__ == '__main__':
	error_pages = spider()
	if error_pages:
		print('因失败重新下载的页面有 %s' % str(error_pages))
		spider(error_pages)
	if csv_rows:
		if input_time:
			with open('社会公众案件 %s.csv' % (str(input_time)[0:10] + '~' + str(now_time)[0:10]), 'w', newline='')as f:
				print('感谢使用社会公众案件查询程序!已生成/刷新文件 社会公众案件 %s.csv 即将终止程序!' % (str(input_time)[0:10] + '~' + str(now_time)[0:10]))
				f_csv = csv.writer(f)
				f_csv.writerow(csv_headers)
				f_csv.writerows(csv_rows)
				time.sleep(10)
		else:
			with open('社会公众案件 1~%s页.csv' % (str(pageNums)), 'w', newline='')as f:
				print('感谢使用社会公众案件查询程序!已生成/刷新文件 社会公众案件 1~%s页.csv 即将终止程序!' % (str(pageNums)))
				f_csv = csv.writer(f)
				f_csv.writerow(csv_headers)
				f_csv.writerows(csv_rows)
				time.sleep(10)




