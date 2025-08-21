import requests

BASE_URL = "https://apis.netstart.cn/maoyan"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/128.0.0.0 Safari/537.36"
}

def get_city_info(lat, lng):
    """根据经纬度获取城市信息（cityId）"""
    url = f"{BASE_URL}/city/latlng?lat={lat}&lng={lng}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_cinemas(movie_id, date, city_id, lat, lng, limit=20, offset=0):
    """获取指定电影在指定日期的影院列表"""
    url = f"{BASE_URL}/movie/select/cinemas"
    params = {
        "limit": limit,
        "offset": offset,
        "client": "iphone",
        "channelId": 4,
        "showDate": date,
        "movieId": movie_id,
        "sort": "distance",
        "cityId": city_id,
        "lat": lat,
        "lng": lng,
        "districtId": -1,
        "lineId": -1,
        "areaId": -1,
        "stationId": -1,
        "brandIds": "[-1]",
        "serviceIds": "[-1]",
        "hallTypeIds": '["all"]',
        "languageIds": '["all"]',
        "dimIds": '["all"]'
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    # 示例：用户输入
    movie_id = 1413641
    show_date = "2025-08-20"
    # TODO: 这里最好用地理编码 API 获取坐标
    lat, lng = 31.0506, 121.5871  # 周浦镇的经纬度（示例）

    city_info = get_city_info(lat, lng)
    city_id = city_info.get("id") or city_info.get("cityId")  # 看接口返回结构

    print("城市信息：", city_info)

    cinemas = get_cinemas(movie_id, show_date, city_id, lat, lng)
    print("影院:"+str(cinemas))
    for c in cinemas.get("cinemas", []):
        print(f"{c['nm']} - {c['addr']} - {c['sellPrice']}元起")
