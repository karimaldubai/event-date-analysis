
from datetime import datetime
from datetime import timedelta
import functions as func
import pandas as pd
tickers = [
    "XOM",
    "BP",
    "SHEL",
    "CVX",
    "TTE",
    "E",
    "COP",
    "REP.MC",
    "APA",
    "DVN",
    "BHP",
    "EXE",
    "CNQ"
]


date = "2024-10-15"

def analisys(date):
    
    while isinstance(date, datetime) != True:
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            date = input("Please use the given date yyyy-mm-dd: ")
    
    start_event = date - timedelta(days = 20)
    end_event = date + timedelta(days = 20)
    start_estimation = date - timedelta(days = 150)
    end_estimation = date + timedelta(days = 150)
    

    market = func.get_finance_data("^GSPC", start_estimation, end_estimation)
    market = func.check_data(market)
    market = func.calculate_returns(market)
    

    ticker_dict_event = {}
    for i in tickers:
        ticker_dict_event[i] = func.get_finance_data(i, start_event, end_event)


    ticker_dict_estimate = {}
    for i in tickers:
        ticker_dict_estimate[i] = func.get_finance_data(i,start_estimation, end_estimation)


    for i in list(ticker_dict_event):
        check_data_event = func.check_data(ticker_dict_event[i], False)
        
        if check_data_event is None:
            del ticker_dict_event[i]
        else:
            ticker_dict_event[i] = check_data_event

    for i in list(ticker_dict_estimate):
        check_data_estimate = func.check_data(ticker_dict_estimate[i], True)
        if check_data_estimate is None:
            del ticker_dict_estimate[i]
        else:
            ticker_dict_estimate[i] = check_data_estimate

    for i in list(ticker_dict_event):
        if i not in ticker_dict_estimate:
            del ticker_dict_event[i]
    for i in list(ticker_dict_estimate):
        if i not in ticker_dict_event:
            del ticker_dict_estimate[i]

    if len(ticker_dict_event) == 0:
        return {"error": "Ticker Data not availble"}
    
    if market is None:
        return {"error": "Market Data is not available"}

    for i in ticker_dict_event:
        ticker_dict_event[i] = func.calculate_returns(ticker_dict_event[i])


    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.calculate_returns(ticker_dict_estimate[i])


    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.calculate_alpha_beta(ticker_dict_estimate[i], market)
    print(ticker_dict_estimate)

    for i in ticker_dict_event:
        ticker_dict_event[i] = func.calculate_ER_AR_CAR(ticker_dict_estimate[i], ticker_dict_event[i], market)

    combined_stocks = func.combine_stocks(*ticker_dict_event.values())

    t_tests_values = func.t_test(combined_stocks, date)
    w_tests_values = func.wilcoxon_test(combined_stocks, date)
    
    residual_standard_deviation_df = pd.DataFrame(index = (["residual variance", "degrees of freedom"]))
    for i in range(len(ticker_dict_estimate)):
        ticker = list(ticker_dict_estimate.keys())[i]
        residual_standard_deviation_df.loc["residual variance", ticker] = list(ticker_dict_estimate.values())[i]["residual variance"].iloc[0]
        residual_standard_deviation_df.loc["degrees of freedom", ticker] = list(ticker_dict_estimate.values())[i]["degrees of freedom"].iloc[0]

    print(residual_standard_deviation_df)
    single_test = func.single_comp_CAR_test(combined_stocks, residual_standard_deviation_df, date)
    print(single_test)

    data_ARs = combined_stocks.iloc[:, 0 : : 2]
    data_ARs.columns = data_ARs.columns.droplevel(1)
    event_date_index = data_ARs.index.get_loc(date)
    start_position = event_date_index -5
    end_position = event_date_index + 6
    data_ARs = data_ARs.iloc[start_position:end_position, :]
    event_CARs = pd.DataFrame(index = ["CAR"])
    for i in range(len(data_ARs.columns)):
        col_ARs = data_ARs.columns[i]
        event_CARs.loc["CAR", col_ARs] = data_ARs.iloc[:,i].sum()

    return combined_stocks, t_tests_values, w_tests_values, event_CARs, single_test

analisys(date)
