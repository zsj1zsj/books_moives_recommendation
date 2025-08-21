#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_prompt.py
生成电影推荐系统提示词的 Python 脚本
"""

import json
import logging
import uuid
from pathlib import Path

# ===================== 日志配置 =====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# ===================== 数据抽取 =====================
def extract_recommendation_data(movie_json: dict) -> dict:
    """从电影 JSON 中抽取推荐系统所需的核心字段"""
    print("extract_recommendation_data")
    try:
        data = {
            "movie_title": movie_json.get("title", ""),
            "movie_genres": movie_json.get("genres", []),
            "movie_director": movie_json.get("director", ""),
            "movie_actors": movie_json.get("actors", []),
            "movie_summary": movie_json.get("summary", ""),
            "movie_rating": movie_json.get("rating", {}).get("score", ""),
            "rating_count": movie_json.get("rating", {}).get("count", 0),
            "rating_distribution": {
                f"{item.get('score', '')}分": item.get("proportion", 0.0)
                for item in movie_json.get("rating", {}).get("details", [])
            },
            "user_reviews": movie_json.get("reviews", []),
            "popularity": {
                "wish_count": movie_json.get("popularity", {}).get("wish_count", 0),
                "watched_count": movie_json.get("popularity", {}).get("watched_count", 0),
                "trending_score": movie_json.get("popularity", {}).get("trending_score", 0),
                "news_score": movie_json.get("popularity", {}).get("news_score", 0),
                "video_score": movie_json.get("popularity", {}).get("video_score", 0),
                "box_office": movie_json.get("popularity", {}).get("box_office", 0),
            }
        }
        logging.info("✅ 数据抽取完成")
        return data
    except Exception as e:
        logging.error(f"❌ 数据抽取失败: {e}")
        return {}


# ===================== 提示词生成 =====================
def generate_prompt(extracted_data: dict) -> str:
    """生成填充模板的提示词（Markdown，带 <xaiArtifact> 标签）"""

    artifact_id = str(uuid.uuid4())

    prompt = f"""
<xaiArtifact id="{artifact_id}" contentType="text/markdown">

# 🎬 个性化电影推荐系统 Prompt

## 任务
基于输入的电影 JSON 数据，生成个性化电影推荐列表。推荐逻辑需结合：
- **内容匹配**（类型、导演、演员、剧情摘要）
- **用户反馈**（评分、评论情感分析）
- **热度数据**（想看/观看人数、实时热度、票房等）
- **用户偏好**（如类型、演员偏好，若有）

## 输入参数
- 电影标题: {extracted_data.get("movie_title", "")}
- 类型: {", ".join(extracted_data.get("movie_genres", []))}
- 导演: {extracted_data.get("movie_director", "")}
- 演员: {", ".join(extracted_data.get("movie_actors", []))}
- 剧情摘要: {extracted_data.get("movie_summary", "")}
- 评分: {extracted_data.get("movie_rating", "")}
- 评分人数: {extracted_data.get("rating_count", 0)}
- 评分分布: {json.dumps(extracted_data.get("rating_distribution", {}), ensure_ascii=False)}
- 热度数据: {json.dumps(extracted_data.get("popularity", {}), ensure_ascii=False)}
- 用户评论: {len(extracted_data.get("user_reviews", []))} 条
- 用户偏好: {{user_preferences}}
- 推荐场景: {{recommendation_scenario}}

## 输出要求
- 推荐电影列表（默认 3 部）
- 格式：JSON 或 Markdown 表格
- 每条包含：
  - 标题
  - 类型
  - 评分
  - 推荐理由

## 推荐逻辑
1. 内容匹配：基于类型、导演、演员、剧情相似度
2. 用户反馈：结合评分分布与评论情感分析
3. 热度排序：综合想看人数、实时热度、票房等
4. 用户偏好：匹配用户喜好（若提供）
"""
    logging.info("✅ 提示词生成完成")
    return prompt.strip()


def save_prompt(prompt: str, output_path: Path):
    """保存提示词到 Markdown 文件"""
    try:
        output_path.write_text(prompt, encoding="utf-8")
        logging.info(f"✅ 提示词已保存至 {output_path}")
    except Exception as e:
        logging.error(f"❌ 保存文件失败: {e}")

# TODO: 写个方法获取 json， 从中获取需要的数据
# 示例 JSON 数据（可替换为实际文件读取）
print("main")
sample_json = {
    "title": "罗小黑战记2",
    "genres": ["动画", "奇幻"],
    "director": "MTJJ",
    "actors": ["山新", "郝祥海"],
    "summary": "小黑的奇幻冒险故事继续展开。",
    "rating": {
        "score": 9.3,
        "count": 120000,
        "details": [
            {"score": 5, "proportion": 0.85},
            {"score": 4, "proportion": 0.10},
            {"score": 3, "proportion": 0.03}
        ]
    },
    "reviews": ["很治愈！", "比第一部更精彩"],
    "popularity": {
        "wish_count": 500000,
        "watched_count": 300000,
        "trending_score": 98,
        "news_score": 80,
        "video_score": 85,
        "box_office": 120000000
    }
}
extracted = extract_recommendation_data(sample_json)
prompt_text = generate_prompt(extracted)

output_file = Path("movie_recommendation_prompt.md")
save_prompt(prompt_text, output_file)
