import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

SCHEMA = {
    "name": "匯率資訊",
    "baseSelector": "table[title='牌告匯率'] tr",
    "fields": [
        {"name": "幣別", "selector": "td[data-table='幣別'] div.print_show", "type": "text"},
        {"name": "本行買入", "selector": "td[data-table='本行現金買入']", "type": "text"}
    ]
}
URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

async def fetch_rate():
    strategy = JsonCssExtractionStrategy(SCHEMA)
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, extraction_strategy=strategy)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=URL, config=run_config)
        with open("rate.json", "w", encoding="utf-8") as f:
            f.write(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(fetch_rate())