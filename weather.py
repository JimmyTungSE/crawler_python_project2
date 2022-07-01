import requests, datetime
import json
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['exam_1_try']

num_=["001","005","009","013","017","021","025","029","033","037","041","045","049","053","057","061","065","069","073","077","081","085","089"]
for i in num_:
    # data_of_mongo = 'mongo_weather{}'.format(page_numb)
    data_of_mongo = 'mongo_weather{}'.format(i)
    collection = db[data_of_mongo]

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-{}?Authorization=CWB-81D57CFF-EDB0-4E82-85C7-7B3529752C7B".format(i)
    data = requests.get(url)   # 取得 JSON 檔案的內容為文字
    data_json = data.json()
    dataset = json.loads(data.text)
    data_dict = {}
    #縣市
    location = dataset["records"]["locations"][0]["locationsName"]
    print("縣市:", location)
    data_dict["縣市"] = location
    data_dict["各地區天氣資訊"] = []
    #鄉鎮
    for township in dataset["records"]["locations"][0]["location"]:
        township_dict = {}
        township_name = township["locationName"]
        print("鄉鎮:",township_name)
        town_weatherElement = township["weatherElement"]
        print("天氣資訊:",town_weatherElement) 
        township_dict[township_name] = town_weatherElement
        data_dict["各地區天氣資訊"].append(township_dict)

    collection.insert_one(data_dict)

    # with open("example1/weather_Try.json", "w", encoding='utf-8') as f:
    #     f.write(json.dumps(data_dict, ensure_ascii=False, indent=2))



