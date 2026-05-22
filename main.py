
from datetime import datetime
from datetime import timedelta
import functions as func
import webbrowser
import os
import pandas as pd
tickers = [
"XOM", "CVX", "SHEL", "BP", "TTE", "PBR", "ONGC.NS", "EQNR", "NWMD.TA"
]


#date = "2012-12-12"

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


    for i in ticker_dict_event:
        ticker_dict_event[i] = func.check_data(ticker_dict_event[i], False)
    #print(ticker_dict_event)

    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.check_data(ticker_dict_estimate[i], True)
    #print(ticker_dict_estimate)


    for i in list(ticker_dict_event):
        if i not in ticker_dict_estimate:
            del ticker_dict_event[i]
    for i in list(ticker_dict_estimate):
        if i not in ticker_dict_event:
            del ticker_dict_estimate[i]


    for i in ticker_dict_event:
        ticker_dict_event[i] = func.calculate_returns(ticker_dict_event[i])
    #print(ticker_dict_event)


    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.calculate_returns(ticker_dict_estimate[i])
    #print(ticker_dict_estimate)


    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.calculate_alpha_beta(ticker_dict_estimate[i], market)
    print(ticker_dict_estimate)

    for i in ticker_dict_event:
        ticker_dict_event[i] = func.calculate_ER_AR_CAR(ticker_dict_estimate[i], ticker_dict_event[i], market)
    #print(ticker_dict_event)

    combined_stocks = func.combine_stocks(*ticker_dict_event.values())
    #print(combined_stocks)

    #func.plot_data(combined_stocks)


    #combined_stocks.to_html("combined_stocks.html")
    #file_path = os.path.abspath("combined_stocks.html")
    #webbrowser.open(file_path)

    #combined_stocks.to_csv("combined_stocks", index = False)


    """
    x = 1
    t_tests_values = []
    w_tests_values = []
    t_tests_results = []
    w_tests_results = []
    while x < len(combined_stocks.columns):
        t_value= func.t_test(combined_stocks.iloc[:, x])[0]
        t_value_p= func.t_test(combined_stocks.iloc[:, x])[1]
        t_tests_results.append(func.t_test(combined_stocks.iloc[:,x])[2])
        t_tests_values.append({"Ticker": combined_stocks.iloc[:, x].name[0], "t-value": t_value, "p-value": t_value_p})

        w_value= func.wilcoxon_test(combined_stocks.iloc[:, x])[0]
        w_value_p= func.wilcoxon_test(combined_stocks.iloc[:, x])[1]
        w_tests_results.append(func.wilcoxon_test(combined_stocks.iloc[:,x])[2])
        w_tests_values.append({"Ticker": combined_stocks.iloc[:, x].name[0], "w-value": w_value, "p-value": w_value_p})
        
        x += 2
    """

    t_tests_values = func.t_test(combined_stocks, date)
    w_tests_values = func.wilcoxon_test(combined_stocks, date)
    
    residual_standard_deviation_df = pd.DataFrame(index = (["residual variance", "degrees of freedom"]))
    for i in range(len(ticker_dict_estimate)):

        """
        residual_standard_deviation.loc[i,"ticker"] = list(ticker_dict_estimate.keys())[i]
        residual_standard_deviation.loc[i,"residual standard deviation"] = list(ticker_dict_estimate.values())[i]["residual standard deviation"].iloc[0]
        """
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

