import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)


# This function gets the data for the past 1 year.
def getData(coinId):
    url = f"https://api.coingecko.com/api/v3/coins/{coinId}/market_chart?x_cg_demo_api_key=CG-3mduk6oZarFpg2usTPNURQXD"
    params = {
        "vs_currency": "usd",
        "days": 365
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    else:
        st.error("Error fetching data")


# Main Code Function starts running
def main():
    st.title("Crypto Tracker")

    # This function will get all the available coins to display in the selection
    coinsListUrl = "https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-3mduk6oZarFpg2usTPNURQXD"
    coinsListResponse = requests.get(coinsListUrl)
    coinsList = coinsListResponse.json()
    coinsDict = {coin['id']: coin['name'] for coin in coinsList}

    # User input for coin selection
    coinInput = st.selectbox("Select a crypto", options=list(coinsDict.values()))

    coinId = [coinId for coinId, name in coinsDict.items() if name == coinInput][0]

    # Fetch coin data
    coinData = getData(coinId)

    if coinData is not None:
        # Plot price over the last year
        st.subheader(f"Price graph for {coinInput}")
        plt.figure(figsize=(10, 6))
        plt.plot(coinData['timestamp'], coinData['price'])
        plt.title(f"{coinInput} Price Over Past 1 Year")
        plt.xlabel("Date")
        plt.ylabel("Price in  US$")
        st.pyplot()

        # Print max and min prices
        maxPrice = coinData['price'].max()
        minPrice = coinData['price'].min()
        # print(maxPrice, minPrice)
        st.write(f"Maximum Price: ${maxPrice:.5f}")
        st.write(f"Minimum Price: ${minPrice:.5f}")

        # Print day with highest and lowest prices
        maxPriceDate = coinData.loc[coinData['price'].idxmax(), 'timestamp']
        minPriceDate = coinData.loc[coinData['price'].idxmin(), 'timestamp']
        st.write(f"Highest Price On: {maxPriceDate}")
        st.write(f"Lowest Price On: {minPriceDate}")


if __name__ == "__main__":
    main()
