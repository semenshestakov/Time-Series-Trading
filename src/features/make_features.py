import pandas as pd


def RSI(df, l=14):
    up, down = df.open.rolling(l).mean(), df.close.rolling(l).mean()
    rsi = 100 - up / (up + down)
    return rsi


def SMA(df, l=10):
    up, down = df.open.rolling(l).sum(), df.close.rolling(l).sum()
    avg = (up + down) / 2
    return avg / l


def z_score(df):
    return (df.mean() - df) / df.std()


def percent_bar(df):
    r = df.open / df.close
    return (r - r.mean()) / r.std()


def get_macd(price, slow, fast, smooth):
    """
    50, 10, 10
    40, 10, 10

    """
    exp1 = price.ewm(span=fast, adjust=False).mean()
    exp2 = price.ewm(span=slow, adjust=False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns={'close': 'macd'})
    signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean()).rename(columns={'macd': 'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns={0: 'hist'})
    frames = [macd, signal, hist]
    df = pd.concat(frames, join='inner', axis=1)
    return df
