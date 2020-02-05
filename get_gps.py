#!/usr/bin/python3
# coding = "utf-8"
import io
import sys
import requests
import json
from math import radians, cos, sin, asin, sqrt

# GPS LiST
location_info_list = []


# 计算两点间距离-米
def getdistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2-lng1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis = 2*asin(sqrt(a))*6371*1000
    return dis


# lng 经度 lat 纬度
def get_gps_distance(gps_info):
    try:
        lng1 = float(gps_info.strip().split("\t")[1])
        lat1 = float(gps_info.strip().split("\t")[2])
        lng2 = float(gps_info.strip().split("\t")[3])
        lat2 = float(gps_info.strip().split("\t")[4])
        return getdistance(lng1, lat1, lng2, lat2)
    except IndexError:
        return "file format error!"


# 使用百度API
def getcodebaidu(address):
    base = "http://api.map.baidu.com/geocoding/v3/?address=" + address + \
           "&city=周口&output=json&ak=tmE5wn0pD9TIfULXYyuooR6uxquLuBqT"
    try:
        response = requests.get(base)

        answer = response.json()
        return answer['result']['location']['lng'], answer['result']['location']['lat']
    except json.JSONDecodeError:
        return "baidu API", " output error!"

# command line input 
def read_txt():
    # Python 3的sys.stdin 并不默认为ASCII,当读取字符串中有汉字时必须设置编码格式与输入文件格式一致，否则输出乱码
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    read_char = input_stream.readline()

    try:
        while read_char.strip():
            location_info_list.append(read_char.strip())
            read_char = input_stream.readline()
            # print(read_char)
    except EOFError:
        pass

# Write Output_gps.txt, find
def print_gps_result(count=10000):
    # 显示文件信息内容
    # print("\nstd.in.encoding: ", input_stream.encoding)
    # print("std.out.encoding: ", sys.stdout.encoding, "\n")
    # print(location_info_list)
    n = 0
    with open("output_gps.txt", "w", encoding="utf-8") as outfile:
        for v in location_info_list:
            if n >= count:
                break
            # Baidu GPS Search
            re = getcodebaidu(str(v))
            lng = "{:.6f}".format(re[0])
            lat = "{:.6f}".format(re[1])
            print(v, " ",lng , lat)
            out_str = v + " " + str(lng) + " " + str(lat) + "\n"
            outfile.write(out_str)
            n += 1


def print_distance_result(count=10000):
    # find n index reset 0
    n = 0
    with open("output_dis.txt", "w", encoding="utf-8") as outfile:
        for v in location_info_list:
            if n >= count:
                break
            dist = "{:.2f}".format(get_gps_distance(str(v)))
            print(v, " ", dist)
            out_str = v + "\t " + str(dist) + "\n"
            outfile.write(out_str)
            n += 1


# 开始程序
# 获取传入参数，确定随机数生成范围
parameter = []
index = 0  # -n 参数的位置
try:
    parameter = sys.argv
    # for i, v in enumerate(parameter):
    #     print(i, v)
except IndexError:
    pass

# 读出文件内容
read_txt()

if "-n" in parameter[1:]:
    # 确定-n参数的位置
    index = parameter.index("-n")

# 输入参数-g 或 默认 查询GPS信息
if "-g" in parameter[1:] or len(parameter) == 1:
    if index != 0:
        print_gps_result(int(parameter[index + 1]))
    else:
        print_gps_result()

# 输入参数 -d 查询两个经纬度的长度为米
if "-d" in parameter[1:]:
    if index != 0:
        print_distance_result(int(parameter[index + 1]))
    else:
        print_distance_result()

