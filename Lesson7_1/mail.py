import nest_asyncio
nest_asyncio.apply()
import streamlit as st
import asyncio
import time
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import pandas as pd

SCHEMA = {
    "name": "匯率資訊",
    "baseSelector": "table[title='牌告匯率'] tr",
    "fields": [
        {
            "name": "幣別",
            "selector": "td[data-table='幣別'] div.print_show",
            "type": "text"
        },
        {
            "name": "本行買入",
            "selector": "td[data-table='本行現金買入']",
            "type": "text"
        }
    ]
}

URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

async def fetch_rate():
    strategy = JsonCssExtractionStrategy(SCHEMA)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=URL, config=run_config)
        return result

def get_rate_data():
    return asyncio.run(fetch_rate())

def main():
    st.set_page_config(layout="wide")
    st.title("台幣匯率轉換")
    last_update = st.empty()
    col1, col2 = st.columns(2)
    refresh = st.button("手動更新")
    if 'rate_data' not in st.session_state or refresh or (time.time() - st.session_state.get('last_fetch', 0) > 60):
        st.session_state['rate_data'] = get_rate_data()
        st.session_state['last_fetch'] = time.time()
    data = st.session_state['rate_data']
    df = pd.DataFrame(data)
    df['本行買入'] = df['本行買入'].replace('', '暫停交易')
    df = df[df['本行買入'] != '暫停交易']
    with col1:
        st.header("台幣轉換為其它貨幣")
        currency = st.selectbox("選擇幣別", df['幣別'])
        amount = st.number_input("請輸入台幣金額", min_value=0.0, value=1000.0)
        rate = df[df['幣別'] == currency]['本行買入'].values[0]
        try:
            rate = float(rate)
            result = amount / rate
            st.success(f"{amount} 台幣 ≈ {result:.2f} {currency}")
        except:
            st.warning("暫停交易或資料異常")
    with col2:
        st.header("匯率資料表")
        st.dataframe(df[['幣別', '本行買入']].reset_index(drop=True))
    last_update.info(f"最後更新時間：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state['last_fetch']))}")

if __name__ == "__main__":
    main()