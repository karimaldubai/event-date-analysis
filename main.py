
from datetime import datetime
from datetime import timedelta
import functions as func
import pandas as pd

#IOCs
tickers = [
    "XOM",
    "BP",
    "SHEL",
    "CVX",
    "TTE",
    "E",
    "ENI.MI",
    "COP",
    "REP.MC",
    "APA",
    "DVN",
    "CNQ"
]

"""
#NOCs
tickers ={    
    "2222.SR",   # Saudi Aramco
    "PBR",       # Petrobras
    "EQNR",      # Equinor
    "EC",        # Ecopetrol
    "YPF",       # YPF
    "0857.HK",   # PetroChina
    "0386.HK",   # Sinopec
    "0883.HK",   # CNOOC
    "ONGC.NS",   # ONGC
    "OIL.NS",    # Oil India
    "PTTEP.BK",  # PTT Exploration and Production
    "OMV.VI"     # OMV}
}
"""
"""
#Renewable Companies
tickers = {
        "NEE",        # NextEra Energy
    "ORSTED.CO", # Ørsted
    "IBE.MC",    # Iberdrola
    "ENEL.MI",   # Enel
    "VWS.CO",    # Vestas Wind Systems
    "FSLR",      # First Solar
    "EDPR.LS",   # EDP Renewables
    "BEP",       # Brookfield Renewable
    "ENPH",      # Enphase Energy
    "SEDG",      # SolarEdge Technologies
    "CSIQ",      # Canadian Solar
    "JKS",       # JinkoSolar
    "VER.VI",    # Verbund
    "SCATC.OL",  # Scatec
    "ANE.MC",    # Acciona Energía
    "0916.HK",   # China Longyuan Power
    "300274.SZ"  # Sungrow Power Supply
}
"""

date = "2026-04-17"

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

    for i in list(ticker_dict_event):
        event_data_ARs = func.calculate_ER_AR_CAR(ticker_dict_estimate[i], ticker_dict_event[i], market)
        check_event_data_AR = func.check_abnormal_returns(event_data_ARs)
        if check_event_data_AR is None:
            del ticker_dict_estimate[i]
            del ticker_dict_event[i]
        else:
            ticker_dict_event[i] = check_event_data_AR
    
    if len(ticker_dict_event) == 0:
        return{"error": "Too much missing data"}
    

    combined_stocks = func.combine_stocks(*ticker_dict_event.values())

    t_tests_values = func.t_test(combined_stocks, date) 
    w_tests_values = func.wilcoxon_test(combined_stocks, date)
    
    residual_standard_deviation_df = pd.DataFrame(index = (["residual variance", "degrees of freedom"]))
    for i in range(len(ticker_dict_estimate)):
        ticker = list(ticker_dict_estimate.keys())[i]
        residual_standard_deviation_df.loc["residual variance", ticker] = list(ticker_dict_estimate.values())[i]["residual variance"].iloc[0]
        residual_standard_deviation_df.loc["degrees of freedom", ticker] = list(ticker_dict_estimate.values())[i]["degrees of freedom"].iloc[0]

    single_test = func.single_comp_CAR_test(combined_stocks, residual_standard_deviation_df, date)

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
#analisys(date)

event_dates = ["2026-03-02", "2026-04-08", "2026-04-24"]

t_tests = pd.DataFrame(index = event_dates, columns= ["p-value", "significance α 0.01", "significance α 0.05"])
w_tests = pd.DataFrame(index = event_dates, columns= ["p-value", "significance α 0.01", "significance α 0.05"])
CARs = pd.DataFrame(index = event_dates)

for i in event_dates:
    combined_stocks, t_tests_values, w_tests_values, event_CARs, single_test = analisys(i)
    t_tests.loc[i,"p-value"] = t_tests_values[1] 
    if t_tests.loc[i,"p-value"]<0.01:
        t_tests.loc[i,"significance α 0.01"] = "significant"
    else:
        t_tests.loc[i,"significance α 0.01"] = "not significant"
    
    if t_tests.loc[i,"p-value"]<0.05:
        t_tests.loc[i,"significance α 0.05"] = "significant"
    else:
        t_tests.loc[i,"significance α 0.05"] = "not significant"


    w_tests.loc[i,"p-value"] = w_tests_values[1]

    if w_tests.loc[i,"p-value"]<0.01:
        w_tests.loc[i,"significance α 0.01"] = "significant"
    else:
        w_tests.loc[i,"significance α 0.01"] = "not significant"
    
    if w_tests.loc[i,"p-value"]<0.05:
        w_tests.loc[i,"significance α 0.05"] = "significant"
    else:
        w_tests.loc[i,"significance α 0.05"] = "not significant"
    
    for x in analisys(i)[3].columns:
        CARs.loc[i,x] = event_CARs.iloc[0][x]

print(t_tests)
print(w_tests)
print(CARs)
