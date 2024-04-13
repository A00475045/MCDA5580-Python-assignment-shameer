import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to fetch historical price data for a cryptocurrency over a given period.
def fetchCryptoData(cryptoId, periodDays):
    baseUrl = "https://api.coingecko.com/api/v3/coins/"
    endpoint = f"{cryptoId}/market_chart"
    parameters = {
        "vs_currency": "usd",
        "days": periodDays,
        "x_cg_demo_api_key": "CG-3mduk6oZarFpg2usTPNURQXD"
    }
    response = requests.get(f"{baseUrl}{endpoint}", params=parameters)
    if response.ok:
        priceData = response.json()['prices']
        priceDf = pd.DataFrame(priceData, columns=['timestamp', 'price'])
        priceDf['timestamp'] = pd.to_datetime(priceDf['timestamp'], unit='ms')
        return priceDf
    else:
        st.error(f"Failed to fetch data: {response.text}")
        return None

# Function to fetch data for the past 1 year for a specific cryptocurrency.
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
        return None

# Main function to show comparison of two cryptocurrencies.
def cryptoPriceTracker():
    st.title("Cryptocurrency Price Tracker")

    listUrl = "https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-3mduk6oZarFpg2usTPNURQXD"
    response = requests.get(listUrl)
    if response.ok:
        coins = response.json()
        coinOptions = {coin['id']: coin['name'] for coin in coins}

        crypto1 = st.selectbox("Choose the first cryptocurrency:", options=list(coinOptions.values()))
        cryptoId1 = [key for key, value in coinOptions.items() if value == crypto1][0]

        crypto2 = st.selectbox("Choose the second cryptocurrency:", options=list(coinOptions.values()))
        cryptoId2 = [key for key, value in coinOptions.items() if value == crypto2][0]

        timeOptions = {"1 Week": 7, "1 Month": 30, "1 Year": 365}
        selectedPeriod = st.selectbox("Choose the period:", options=list(timeOptions.keys()))

        data1 = fetchCryptoData(cryptoId1, timeOptions[selectedPeriod])
        data2 = fetchCryptoData(cryptoId2, timeOptions[selectedPeriod])

        if data1 is not None and data2 is not None:
            st.subheader(f"Comparing {crypto1} and {crypto2} over {selectedPeriod}")
            plt.figure(figsize=(10, 6))
            plt.plot(data1['timestamp'], data1['price'], label=crypto1)
            plt.plot(data2['timestamp'], data2['price'], label=crypto2)
            plt.title(f"Price Trend: {selectedPeriod}")
            plt.xlabel("Date")
            plt.ylabel("Price in USD")
            plt.legend()
            st.pyplot()
    else:
        st.error("Could not load cryptocurrency list.")

# Main function to display data and price trends of a single cryptocurrency.
def cryptoTracker():
    st.title("Crypto Tracker")

    coinsListUrl = "https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-3mduk6oZarFpg2usTPNURQXD"
    coinsListResponse = requests.get(coinsListUrl)
    coinsList = coinsListResponse.json()
    coinsDict = {coin['id']: coin['name'] for coin in coinsList}

    coinInput = st.selectbox("Select a crypto", options=list(coinsDict.values()))
    coinId = [coinId for coinId, name in coinsDict.items() if name == coinInput][0]

    coinData = getData(coinId)

    if coinData is not None:
        st.subheader(f"Price graph for {coinInput}")
        plt.figure(figsize=(10, 6))
        plt.plot(coinData['timestamp'], coinData['price'])
        plt.title(f"{coinInput} Price Over Past 1 Year")
        plt.xlabel("Date")
        plt.ylabel("Price in US$")
        st.pyplot()

        maxPrice = coinData['price'].max()
        minPrice = coinData['price'].min()
        st.write(f"Maximum Price: ${maxPrice:.5f}")
        st.write(f"Minimum Price: ${minPrice:.5f}")

        maxPriceDate = coinData.loc[coinData['price'].idxmax(), 'timestamp']
        minPriceDate = coinData.loc[coinData['price'].idxmin(), 'timestamp']
        st.write(f"Highest Price On: {maxPriceDate}")
        st.write(f"Lowest Price On: {minPriceDate}")

# User interface for navigating between two functionalities.
def main():
    st.sidebar.title("Navigation")
    appChoice = st.sidebar.radio("Go to", ("Crypto Tracker", "Crypto Price Tracker"), index=0)

    if appChoice == "Crypto Price Tracker":
        cryptoPriceTracker()
    elif appChoice == "Crypto Tracker":
        cryptoTracker()

if __name__ == "__main__":
    main()
