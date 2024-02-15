import streamlit as st
import pandas as pd 
import numpy as np
import yfinance as yf 
import plotly.express as px

st.title('Welcome to the world of Finance🪙')
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Dow Jones", "38293", "0.055%")
col2.metric("S&P 500", "4973", "-0.09%")
col3.metric("Nasdaq Composite", "15761", "0.6%")
st.divider()

with st.sidebar:
    ticker = st.text_input('💹Stock name')
    start_date = st.date_input('🗓️Start date')
    end_date = st.date_input('🗓️End date')
data = yf.download(ticker,start=start_date,end=end_date)
print(data)
fig = px.line(data,x=data.index, y = data['Adj Close'],title = ticker)
st.plotly_chart(fig)
st.bar_chart(data['Volume'],color='#008000')
pricing_data, fundamental_data,news,tech_indicator = st.tabs(['Pricing data','Fundamental data','Top 5 news','Technical Indicator'])
with pricing_data:
    st.subheader('Price Movements')
    data2 = data
    data2['% change'] = data['Adj Close'] / data['Adj Close'].shift(1) -1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['% change'].mean()*252*100
    st.write('Annual Return is',annual_return,'%')
    st_dev = np.std(data2['% change'])*np.sqrt(252)
    st.write('Standard Deviation is',st_dev*100,'%')

from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    key = 'OPJF0JNRIPA233ZI'
    fd = FundamentalData(key, output_format='pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Cash Flow')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)
    st.bar_chart(cf)
    import streamlit as st
    import yfinance as yf
    import matplotlib.pyplot as plt
# Streamlit app title
    st.subheader('Cash Flow Chart')
# Input field for ticker symbol
    ticker_symbol = st.text_input('Enter Ticker Symbol (e.g., AAPL for Apple):')

# Fetch cash flow data
if ticker_symbol:
    try:
        # Fetch data from Yahoo Finance
        cash_flow = yf.Ticker(ticker_symbol).cashflow

        # Select cash flow variables
        selected_variables = st.multiselect('Select Cash Flow Variables', cash_flow.rows)

        # Plotting cash flow data
        plt.figure(figsize=(10, 6))
        cash_flow[selected_variables].plot(kind='bar', ax=plt.gca())
        plt.title(f'Cash Flow Statement for {ticker_symbol}')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot()
    except Exception as e:
        st.error(f"Error fetching data: {e}")

    
    

from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker,save_news=False)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

import pandas_ta as ta
with tech_indicator:
    st.header('Technical Analysis ')
    df = pd.DataFrame()
    ind_list = df.ta.indicators(as_list=True)
    technical_indicator = st.selectbox('Tech Indicator',options=ind_list)
    method = technical_indicator
    indicator = pd.DataFrame(getattr(ta,method)(low=data['Low'],close=data['Close'],high=data['High'],open=data['Open']))
    indicator['Close'] = data['Close']
    figw_ind_new = px.line(indicator)
    st.plotly_chart(figw_ind_new)
    st.write(indicator)






