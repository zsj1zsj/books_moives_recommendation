import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/128.0.0.0 Safari/537.36"
}

# 最受好评电影列表
hottest_movies_url = "https://apis.netstart.cn/maoyan/index/topRatedMovies"
hottest_movies = requests.get(hottest_movies_url, headers=headers).json()

for movie in hottest_movies["movieList"]:
    print(movie["name"])

# 关键词获取 movieid
keyword_to_id_url = "https://apis.netstart.cn/maoyan/search/movies?keyword=%E6%B5%AA%E6%B5%AA%E5%B1%B1%E5%B0%8F%E5%A6%96%E6%80%AA&ci=1"
keyword_to_id = requests.get(keyword_to_id_url, headers=headers).json()
print(keyword_to_id)


# 通过 movieid 获取电影详情
# movie_detail_url = "https://apis.netstart.cn/maoyan/movie/detail?movieId=1331230"
# movie_detail = requests.get(movie_detail_url, headers=headers).json()
# print(movie_detail)