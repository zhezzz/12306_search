import urllib3
import json
import time

http = urllib3.PoolManager()

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie':
    '_uab_collina=161950018733183389546025; JSESSIONID=B1616DC91F8063A85E95617D7172B5E3; BIGipServerpool_passport=48497162.50215.0000; RAIL_EXPIRATION=1619797029807; RAIL_DEVICEID=qjLKRUPA4TDUugDY43e0t1qxLKxRc9X5Q6-bLQmMmP1D3uVySEuT7MbWpQMEf4rXa1cVH1v86SAzZfFQei86t5fFuLWgxm18IagYMpnoenmGbUwdhdjrM8Jc6cmZD0RQH6HgZuccurlI3fFJazAbucCjfltKThI0; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_toStation=%u8386%u7530%2CPTS; _jc_save_toDate=2021-04-27; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2021-05-01; current_captcha_type=C; BIGipServerotn=116392458.50210.0000; _jc_save_fromStation=%u4E0A%u6D77%u8679%u6865%2CAOH',
    'DNT': '1',
    'Host': 'kyfw.12306.cn',
    'If-Modified-Since': '0',
    'Pragma': 'no-cache',
    'Referer':
    'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E4%B8%8A%E6%B5%B7,SHH&ts=%E6%BD%AE%E6%B1%95,CBQ&date=2021-04-29&flag=N,N,Y',
    'sec-ch-ua':
    '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


# 处理获得的字符串，返回字典类型
def zip_dic():
    # 由于火车站使用三字码，所以我们需要先获取站点对应的三字码
    response = http.request(
        'GET',
        'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js')
    code_data = response.data.decode('utf-8')
    code_data = code_data[20:]
    list_code = code_data.split("|")
    a = 1
    b = 2
    t1 = []
    t2 = []
    while (a < (len(list_code))):
        t1.append(list_code[a])
        t2.append(list_code[b])
        a = a + 5
        b = b + 5
    dic = dict(zip(t1, t2))
    return dic


code_dic = zip_dic()

## 参数定义
fromStationName = '上海虹桥'
toStationName = '潮汕'
fromStationTeleCode = code_dic[fromStationName]
toStationTeleCode = code_dic[toStationName]
dptDate = '2021-05-02'
trainNoList = []
trainInfoList = []
role = 'ADULT'
## 高铁动车
GorD = 'G'
## 座位 ZE=二等座
seatType = 'ZE'
## 指定的车次
disTrainNoList = ['D2281']


## 查询列车经停站信息
def queryByTrainNo(train_no, fromStationTeleCode, toStationTeleCode, dptDate):
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={}&from_station_telecode={}&to_station_telecode={}&depart_date={}'.format(
        train_no, fromStationTeleCode, toStationTeleCode, dptDate)
    response = http.request('GET', url, headers=headers)
    info = json.loads(response.data.decode('utf-8'))['data']['data']
    return info


## 查询单天所有列车
def query(fromStationTeleCode, toStationTeleCode, dptDate, role, disTrainNo):
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(
        dptDate, fromStationTeleCode, toStationTeleCode, role)
    response = http.request('GET', url, headers=headers)
    resp = response.data.decode('utf-8')
    # print(resp)
    if '网络' in resp:
        print('网络错误')
        return []
    data = json.loads(resp)['data']
    time.sleep(3)
    endAllStationMap = data['map']
    trainList = data['result']
    resultList = []
    for train in trainList:
        infoList = train.split('|')
        result = {}
        result['train_no'] = infoList[2]
        result['station_train_code'] = infoList[3]
        result['start_station_telecode'] = infoList[4]
        result['end_station_telecode'] = infoList[5]
        result['from_station_telecode'] = infoList[6]
        result['to_station_telecode'] = infoList[7]
        result['start_time'] = infoList[8]
        result['arrive_time'] = infoList[9]
        result['lishi'] = infoList[10]
        result['canWebBuy'] = infoList[11]
        result['yp_info'] = infoList[12]
        result['start_train_date'] = infoList[13]
        result['train_seat_feature'] = infoList[14]
        result['location_code'] = infoList[15]
        result['from_station_no'] = infoList[16]
        result['to_station_no'] = infoList[17]
        result['is_support_card'] = infoList[18]
        result['controlled_train_flag'] = infoList[19]
        result['gg_num'] = infoList[20] if infoList[20] != '' else '无'
        result['gr_num'] = infoList[21] if infoList[21] != '' else '无'
        result['qt_num'] = infoList[22] if infoList[22] != '' else '无'
        result['rw_num'] = infoList[23] if infoList[23] != '' else '无'
        result['rz_num'] = infoList[24] if infoList[24] != '' else '无'
        result['tz_num'] = infoList[25] if infoList[25] != '' else '无'
        result['wz_num'] = infoList[26] if infoList[26] != '' else '无'
        result['yb_num'] = infoList[27] if infoList[27] != '' else '无'
        result['yw_num'] = infoList[28] if infoList[28] != '' else '无'
        result['yz_num'] = infoList[29] if infoList[29] != '' else '无'
        result['ze_num'] = infoList[30] if infoList[30] != '' else '无'
        result['zy_num'] = infoList[31] if infoList[31] != '' else '无'
        result['swz_num'] = infoList[32] if infoList[32] != '' else '无'
        result['srrb_num'] = infoList[33] if infoList[33] != '' else '无'
        result['sold_out'] = False
        if result['gg_num'] == '无' and result['gr_num'] == '无' and result[
                'qt_num'] == '无' and result['rw_num'] == '无' and result[
                    'rz_num'] == '无' and result['tz_num'] == '无' and result[
                        'wz_num'] == '无' and result['yb_num'] == '无' and result[
                            'yw_num'] == '无' and result[
                                'yz_num'] == '无' and result[
                                    'ze_num'] == '无' and result[
                                        'zy_num'] == '无' and result[
                                            'swz_num'] == '无' and result[
                                                'srrb_num'] == '无':
            result['sold_out'] = True
        result['yp_ex'] = infoList[34]
        result['seat_types'] = infoList[35]
        result['exchange_train_flag'] = infoList[36]
        result['houbu_train_flag'] = infoList[37]
        result['houbu_seat_limit'] = infoList[38]
        if disTrainNo == result['station_train_code']:
            resultList.append(result)
            break
        elif disTrainNo == None:
            resultList.append(result)
    return resultList


def queryTicketPrice(train_no, fromStationNo, toStationNo, dptDate, seatTypes):
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}}&from_station_no={}&to_station_no={}&seat_types=MOO&train_date={}'.format(
        train_no, fromStationNo, toStationNo, seatTypes, dptDate)
    response = http.request('GET', url, headers=headers)
    info = json.loads(response.data.decode('utf-8'))['data']['data']
    return info


##查询指定车次前后站点是否有余票

for disTrainNo in disTrainNoList:
    trainInfo = query(fromStationTeleCode, toStationTeleCode, dptDate, role,
                      disTrainNo)[0]
    trainPassStopList = queryByTrainNo(trainInfo['train_no'],
                                       fromStationTeleCode, toStationTeleCode,
                                       dptDate)
    fromNo = 1
    toNo = 1
    for i in range(0, len(trainPassStopList)):
        tps = trainPassStopList[i]
        if tps['station_name'] == fromStationName:
            fromNo = i
        if tps['station_name'] == toStationName:
            toNo = i

    # print(trainPassStopList)
    for i in range(0, fromNo + 1):
        iStation = trainPassStopList[i]
        iStationTeleCode = code_dic[iStation['station_name']]
        for j in range(toNo, len(trainPassStopList)):
            jStation = trainPassStopList[j]
            jStationTeleCode = code_dic[jStation['station_name']]
            ## 查询是否有票
            info = query(iStationTeleCode, jStationTeleCode, dptDate, role,
                         disTrainNo)
            if len(info) == 0 or info[0]['sold_out']:
                continue
            print(iStation['station_name'] + ' 到：' + jStation['station_name'] +
                  ' 有票')

# print(queryByTrainNo('5l000D3145B0', fromStationTeleCode, toStationTeleCode, dptDate))
# print(query(fromStationTeleCode, toStationTeleCode, dptDate, role, None))
