import pandas as pd
from xtquant import xtdata

def download_data(code, period, start_time, end_time):
    xtdata.download_history_data(
        code,
        period=period,
        start_time=start_time,
        end_time=end_time,
        incrementally=True
    )

def filter_trading_time(df):
    df = df.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        df['datetime'] = pd.to_datetime(df.index.astype(str), format='%Y%m%d%H%M%S')
        df = df.set_index('datetime')
    morning = df.between_time('09:30', '11:30')
    afternoon = df.between_time('13:00', '15:00')
    return pd.concat([morning, afternoon]).sort_index()

def resample_custom_kline(df, code, intervals):
    result = []
    for date, group in df.groupby(df.index.date):
        for start, end in intervals:
            start_dt = pd.Timestamp(f"{date} {start}")
            end_dt = pd.Timestamp(f"{date} {end}")
            mask = (group.index >= start_dt) & (group.index < end_dt)
            seg = group.loc[mask]
            if seg.empty:
                continue
            k = {
                'datetime': end_dt.strftime('%Y%m%d%H%M%S'),
                'code': code,
                'open': round(seg['open'].iloc[0], 3),
                'high': round(seg['high'].max(), 3),
                'low': round(seg['low'].min(), 3),
                'close': round(seg['close'].iloc[-1], 3),
                'preClose': round(seg['preClose'].iloc[0], 3),
                'volume': seg['volume'].sum(),
                'amount': seg['amount'].sum()
            }
            result.append(k)
    return pd.DataFrame(result)

def get_historical_data(symbol: str, start_date: str, end_date: str, period: str = '1m'):
    # 支持的周期
    valid_periods = ['1m', '5m', '30m', '60m', '1d']
    if period not in valid_periods:
        return {"code": 1, "message": "仅支持周期: 1m, 5m, 30m, 60m, 1d", "data": []}

    # 1d用日线，30m/60m用5m聚合，其余直接取
    if period == '1d':
        actual_period = '1d'
    elif period in ['30m', '60m']:
        actual_period = '5m'
    else:
        actual_period = period

    start = start_date.replace('-', '')
    end = end_date.replace('-', '')

    download_data(symbol, actual_period, start, end)
    data_dict = xtdata.get_market_data_ex([], [symbol], period=actual_period, start_time=start, end_time=end)

    if symbol not in data_dict or data_dict[symbol].empty:
        return {"code": 1, "message": "未获取到数据或数据为空", "data": []}
    df = data_dict[symbol]

    # 日线
    if period == '1d':
        df['datetime'] = pd.to_datetime(df.index.astype(str), format='%Y%m%d')
        df = df.set_index('datetime')
        df['datetime'] = df.index.strftime('%Y%m%d')
        df['code'] = symbol
        for col in ['open', 'high', 'low', 'close', 'preClose']:
            df[col] = df[col].round(3)
        result = df[['datetime', 'code', 'open', 'high', 'low', 'close', 'preClose', 'volume', 'amount']].reset_index(drop=True)
    # 60m/30m聚合
    elif period in ['30m', '60m']:
        df['datetime'] = pd.to_datetime(df.index.astype(str), format='%Y%m%d%H%M%S')
        df = df.set_index('datetime')
        df = filter_trading_time(df)
        if period == '60m':
            intervals = [
                ('09:30', '10:30'),
                ('10:30', '11:30'),
                ('13:00', '14:00'),
                ('14:00', '15:00')
            ]
        else:  # 30m
            intervals = [
                ('09:30', '10:00'),
                ('10:00', '10:30'),
                ('10:30', '11:00'),
                ('11:00', '11:30'),
                ('13:00', '13:30'),
                ('13:30', '14:00'),
                ('14:00', '14:30'),
                ('14:30', '15:00')
            ]
        result = resample_custom_kline(df, symbol, intervals)
    # 1m/5m
    else:
        df['datetime'] = pd.to_datetime(df.index.astype(str), format='%Y%m%d%H%M%S')
        df = df.set_index('datetime')
        df = filter_trading_time(df)
        df = df.reset_index()
        df['datetime'] = df['datetime'].dt.strftime('%Y%m%d%H%M%S')
        df['code'] = symbol
        for col in ['open', 'high', 'low', 'close', 'preClose']:
            df[col] = df[col].round(3)
        result = df[['datetime', 'code', 'open', 'high', 'low', 'close', 'preClose', 'volume', 'amount']]

    return {"code": 0, "message": "Success", "data": result.to_dict(orient='records')}