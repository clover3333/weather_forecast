#coding=utf-8
import requests
from imp import reload
import sys
import urllib.request
import json
import chardet
from pypinyin import lazy_pinyin
import pypinyin
import re

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

#中文转化为拼音
def pinyin(string):
	result =lazy_pinyin(string,style=pypinyin.NORMAL)
	cityName = ''
	for item in result:
		# print(item)
		cityName = cityName + (str(item))
	return cityName

#判断字符串是否为中文字符
def isHans(contents):
	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	#一个小应用，判断一段文本中是否包含简体中：
	match = zhPattern.search(contents)
	if match:
		# print(u'有中文：%s' % (match.group(0),))
		return True
	else:
		# print(u'没有包含中文')
		return False

#获取城市名
def getCityName():
	city = ''
	print(u"请输入要查询的城市:")
	city = input()
	if isHans(city):
		city = pinyin(city)
	return city

# 百度天气API
def getWeather():
	cityName = getCityName()
	url = 'http://apis.baidu.com/heweather/weather/free?city=' + cityName
	# print(url)
	req = urllib.request.Request(url)
	req.add_header("apikey", "******")	#填入自己的APIkey就行了
	resp = urllib.request.urlopen(req)
	content = resp.read()

	# 查看获取的代码的编码格式
	# print(type(content))
	# print(chardet.detect(content))

	if content:
		print(content.decode('utf-8'))
		with open('weather.json', 'w', encoding='utf-8') as f:
			f.write(content.decode('utf-8'))
	else:
		print(u'保存天气json文件的时候出错啦~~~')

#处理数据
def handleData():
	#读取json数据
	with open('weather.json', 'r', encoding='utf-8') as f:
		weather_data = json.load(f)
		if weather_data:
			data_dict = weather_data["HeWeather data service 3.0"][0]
			# print(data_dict)
			detail_data = {}
			detail_data[u"国家"] = data_dict["basic"]["cnty"]
			detail_data[u"城市"] = data_dict["basic"]["city"]
			detail_data[u'时间'] = data_dict["daily_forecast"][0]["date"]
			detail_data[u"天气"] = data_dict["daily_forecast"][0]["cond"]["txt_d"]\
			                     + ',' + data_dict["daily_forecast"][0]["cond"]["txt_n"]
			detail_data[u'温度'] = data_dict["now"]["tmp"]
			detail_data[u'最高温度'] = data_dict["daily_forecast"][0]["tmp"]["max"]
			detail_data[u'最低温度'] = data_dict["daily_forecast"][0]["tmp"]["min"]
			detail_data[u'体感温度'] = data_dict["now"]["fl"]
			if "aqi" in data_dict:
				detail_data[u'空气质量'] = data_dict["aqi"]["city"]["qlty"]

			with open('weather_forecast.txt', 'w', encoding='utf-8') as f:
				for item in detail_data:
					f.writelines(item.encode('utf-8').decode('utf-8') + \
					':' + detail_data[item].encode('utf-8').decode('utf-8') + '\n')
			return detail_data
			# print(detail_data)
		else:
			print(u'处理json数据的时候出错啦~~~')


#展示数据
def showDataByText():
	data = handleData()
	if data:
		print(u"国家：", data["国家"])
		print(u"城市：", data["城市"])
		print(u"时间：", data["时间"])
		print(u"天气：", data["天气"])
		if u"空气质量" in data:	#有的城市没有空气质量这一数据，所以稍作处理
			print(u"空气质量：", data["空气质量"])
		else:
			print(u"空气质量：哎呀！这地儿太小了，空气质量查不了~~~")
		print(u"温度：", data["温度"])
		print(u"体感温度：", data["体感温度"])
		print(u"最高温度：", data["最高温度"])
		print(u"最低温度：", data["最低温度"])
	else:
		print(u'输出天气情况的时候出错啦~~~')

def main():
	if __name__ == "__main__":
		check = 'y'
		while(check == 'y'):
			getWeather()
			handleData()
			showDataByText()
			check = input("是否继续查询（y/n）:")

main()
