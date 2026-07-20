
from datetime import datetime
from datetime import timedelta
import functions as func
import pandas as pd
from pathlib import Path


############################################################################################################
#tickers for my project
#IOCs
"""
tickers = [
    "XOM",      # Exxon Mobil Corporation
    "BP",       # BP p.l.c.
    "SHEL",     # Shell plc
    "CVX",      # Chevron Corporation
    "TTE",      # TotalEnergies SE
    "E",        # Eni S.p.A. ADR
    "COP",      # ConocoPhillips
    "REP.MC",   # Repsol S.A.
    "APA",      # APA Corporation
    "DVN",      # Devon Energy Corporation
    "CNQ"       # Canadian Natural Resources Limited,
]
"""
#NOCs
"""
tickers ={    
    "2222.SR",   # Saudi Aramco
    "PBR",       # Petrobras (brazil)
    "EQNR",      # Equinor 
    "EC",        # Ecopetrol (columbia)
    "YPF",       # YPF (spain)
    "0857.HK",   # PetroChina
    "0386.HK",   # Sinopec (china)
    "0883.HK",   # CNOOC (China national offshore company)
    "ONGC.NS",   # ONGC (Oil and Natural Gas Corporation Limited [India])
    "OIL.NS",    # Oil India
    "PTTEP.BK",  # PTT Exploration and Production (thailand)
    "OMV.VI"     # OMV
}
"""

#all OCs

tickers = [
    "XOM",      # Exxon Mobil Corporation
    "BP",       # BP p.l.c.
    "SHEL",     # Shell plc
    "CVX",      # Chevron Corporation
    "TTE",      # TotalEnergies SE
    "E",        # Eni S.p.A. ADR
    "COP",      # ConocoPhillips
    "REP.MC",   # Repsol S.A.
    "APA",      # APA Corporation
    "DVN",      # Devon Energy Corporation
    "CNQ" ,      # Canadian Natural Resources Limited,
    "PBR",       # Petrobras (brazil)
    "EQNR",      # Equinor 
    "EC",        # Ecopetrol (columbia)
    "YPF",       # YPF (spain)
    "0857.HK",   # PetroChina
    "0386.HK",   # Sinopec (china)
    "0883.HK",   # CNOOC (China national offshore company)
    "ONGC.NS",   # ONGC (Oil and Natural Gas Corporation Limited [India])
    "OIL.NS",    # Oil India
    "PTTEP.BK",  # PTT Exploration and Production (thailand)
    "OMV.VI"     # OMV
]


#Renewable Companies
"""
tickers = {
        "NEE",        # NextEra Energy USA
    "ORSTED.CO", # Ørsted danish
    "IBE.MC",    # Iberdrola Spain
    "ENEL.MI",   # Enel Italy
    "VWS.CO",    # Vestas Wind Systems Denmark
    "FSLR",      # First Solar USA
    "EDPR.LS",   # EDP Renewables Spain
    "BEP",       # Brookfield Renewable
    "ENPH",      # Enphase Energy USA
    "SEDG",      # SolarEdge Technologies israel
    "CSIQ",      # Canadian Solar
    "JKS",       # JinkoSolar chinese
    "VER.VI",    # Verbund
    "SCATC.OL",  # Scatec Norway
    "ANE.MC",    # Acciona Energía Spain
    "0916.HK",   # China Longyuan Power
    "300274.SZ"  # Sungrow Power Supply China 
}
############################################################################################################
#tickers for controll
"""
"""
#us tickers for controll
tickers = [
    "XOM",      # Exxon Mobil
    "BP",       # BP
    "CVX",      # Chevron
    "COP",      # ConocoPhillips
    "APA",      # Apache / APA Corporation
    "DVN",      # Devon Energy
    "APC",      # Anadarko
    "CHK"       # Chesapeake
]
"""
"""
#non us tickers for controll
tickers = [
    "SHEL",       # Shell
    "TTE",        # TotalEnergies
    "LUKOY",      # Lukoil
    "E",          # Eni
    "SNGS.ME",    # Surgutneftegas
    "TNKBP.ME",   # TNK-BP
    "REP.MC",     # Repsol
    "NVTK.ME",    # Novatek
    "BG.L",       # BG Group
    "BHP",        # BHP Billiton / BHP Group
    "CNQ"         # Canadian Natural Resources
]
"""

"""
#all tickers for controll
tickers = [
    "XOM",
    "BP",
    "SHEL",
    "CVX",
    "TTE",
    "LUKOY",
    "E",
    "SNGS.ME",
    "TNKBP.ME",
    "COP",
    "REP.MC",
    "NVTK.ME",
    "BG.L",
    "APA",
    "DVN",
    "APC",
    "BHP",
    "CHK",
    "CNQ"

]
"""
#golf war
"""
tickers = [
    "XOM",       # Exxon Mobil
    "BP",        # BP
    "SHEL",      # Shell
    "CVX",       # Chevron
    "E",         # Eni
    "COP",       # ConocoPhillips
    "REP.MC",    # Repsol
    "BG.L",      # BG Group
    "APA",       # Apache / APA Corporation
    "DVN",       # Devon Energy
    "APC",       # Anadarko
    "BHP",       # BHP Billiton / BHP Group
    "CHK",       # Chesapeake
    "CNQ",       # Canadian Natural Resources
    "TTE",       # Total / TotalEnergies
    "LUKOY",     # Lukoil
    "SNGS.ME",   # Surgutneftegas
    "TNKBP.ME",  # TNK-BP
    "NVTK.ME"    # Novatek
]
"""
#afghan war
"""
tickers = [
    "XOM",       # Exxon Mobil
    "BP",        # BP
    "SHEL",      # Shell
    "CVX",       # Chevron
    "E",         # Eni
    "COP",       # ConocoPhillips
    "REP.MC",    # Repsol
    "BG.L",      # BG Group
    "APA",       # Apache / APA Corporation
    "DVN",       # Devon Energy
    "APC",       # Anadarko
    "BHP",       # BHP Billiton / BHP Group
    "CHK",       # Chesapeake
    "CNQ",       # Canadian Natural Resources

    "TTE",       # Total / TotalEnergies
    "LUKOY",     # Lukoil
    "SNGS.ME",   # Surgutneftegas
    "TNKBP.ME",  # TNK-BP
    "NVTK.ME"    # Novatek
]
"""

#iraq war
"""
tickers = [
    "XOM",       # Exxon Mobil
    "BP",        # BP
    "SHEL",      # Shell
    "CVX",       # Chevron
    "E",         # Eni
    "COP",       # ConocoPhillips
    "REP.MC",    # Repsol
    "BG.L",      # BG Group
    "APA",       # Apache / APA Corporation
    "DVN",       # Devon Energy
    "APC",       # Anadarko
    "BHP",       # BHP Billiton / BHP Group
    "CHK",       # Chesapeake

    "TTE",       # Total / TotalEnergies
    "LUKOY",     # Lukoil
    "SNGS.ME",   # Surgutneftegas
    "TNKBP.ME",  # TNK-BP
    "NVTK.ME"    # Novatek
]
"""

def analisys(date):
##########################################################################################################
#user input   

    while isinstance(date, datetime) != True:
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            date = input("Please use the given date yyyy-mm-dd: ")
    
    start_event = date - timedelta(days = 20)
    end_event = date + timedelta(days = 20)
    start_estimation = date - timedelta(days = 170)
    end_estimation = date - timedelta(days = 40)
##########################################################################################################
#calculates Market data for OLS and expected returns

    market_event = func.get_finance_data("^990100-USD-STRD", start_event, end_event)
    market_event = func.check_data(market_event,False)
    market_event = func.calculate_returns(market_event)
    
    market_estimation = func.get_finance_data("^990100-USD-STRD", start_estimation, end_estimation)
    market_estimation = func.check_data(market_estimation,True)
    market_estimation = func.calculate_returns(market_estimation)

    if market_event is None:
        return {"error": "Market Data is not available"}
    
    if market_estimation is None:
        return {"error": "Market Data is not available"}
##########################################################################################################
#download market data and check if enough values are available

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
##########################################################################################################
#check if event and estimation window have the same tickers

    for i in list(ticker_dict_event):
        if i not in ticker_dict_estimate:
            del ticker_dict_event[i]
    for i in list(ticker_dict_estimate):
        if i not in ticker_dict_event:
            del ticker_dict_estimate[i]

    if len(ticker_dict_event) == 0:
        return {"error": "Ticker Data not availble"}
##########################################################################################################
#calculate returns for event and estimation window

    for i in ticker_dict_event:
        ticker_dict_event[i] = func.calculate_returns(ticker_dict_event[i])


    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.calculate_returns(ticker_dict_estimate[i])
##########################################################################################################
#calculate alpha and beta through OLS with estimation window

    for i in ticker_dict_estimate:
        ticker_dict_estimate[i] = func.calculate_alpha_beta(ticker_dict_estimate[i], market_estimation)
##########################################################################################################
#calculate ER/AR/CAR and save in event dataframe; check if stocks have enough AR values to analyse, if not delete them

    for i in list(ticker_dict_event):
        event_data_ARs = func.calculate_ER_AR_CAR(ticker_dict_estimate[i], ticker_dict_event[i], market_event)
        check_event_data_AR = func.check_abnormal_returns(event_data_ARs, date)
        if check_event_data_AR is None:
            del ticker_dict_estimate[i]
            del ticker_dict_event[i]
        else:
            ticker_dict_event[i] = check_event_data_AR
    
    if len(ticker_dict_event) == 0:
        return{"error": "Too much missing data"}
##########################################################################################################
#combine stocks into new dataframe

    combined_stocks = func.combine_stocks(*ticker_dict_event.values())
    #for i in combined_stocks.index:

    for i in list(combined_stocks.index):
        row_ARs = combined_stocks.loc[i].iloc[0::2]
        missing_ARs_date = row_ARs.isna().sum()

        if missing_ARs_date > 2:
            print(f"Deleted date {i}; {missing_ARs_date} tickers had missing ARs")
            combined_stocks = combined_stocks.drop(index=i)

    for i in list(combined_stocks.columns.get_level_values(0).unique()):

        missing_ARs = combined_stocks[i].iloc[:, 0].isna().sum()

        if missing_ARs > 0:
            print(f"Deleted ticker {i}; {missing_ARs} missing ARs")

            del combined_stocks[i]
            del ticker_dict_event[i]
            del ticker_dict_estimate[i]

##########################################################################################################
#run t-test, wilcoxon test

    t_tests_values = func.t_test(combined_stocks, date) 
    w_tests_values = func.wilcoxon_test(combined_stocks, date)
##########################################################################################################
#take residual variance and degrees of freedom, previously calculated in OLS out of estimation window and use to run Market Model test

    residual_standard_deviation_df = pd.DataFrame(index = (["residual variance", "degrees of freedom"]))
    for i in range(len(ticker_dict_estimate)):
        ticker = list(ticker_dict_estimate.keys())[i]
        residual_standard_deviation_df.loc["residual variance", ticker] = list(ticker_dict_estimate.values())[i]["residual variance"].iloc[0]
        residual_standard_deviation_df.loc["degrees of freedom", ticker] = list(ticker_dict_estimate.values())[i]["degrees of freedom"].iloc[0]

    single_test = func.single_comp_CAR_test(combined_stocks, residual_standard_deviation_df, date)
##########################################################################################################
#calculate CAR around event window (i manually changed to 5+- days in all the functions, i dont know why anymore.. i could have just used this window from the beginning)

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
##########################################################################################################
#creates files before return
    results_folder = Path("results")
    results_folder.mkdir(exist_ok=True)

    #date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
    file_path = results_folder / f"{pd.to_datetime(date).strftime('%Y-%m-%d')}_results.xlsx"

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        combined_stocks.to_excel(writer, sheet_name="combined_stocks")
        event_CARs.to_excel(writer, sheet_name="event_CARs")
        single_test.to_excel(writer, sheet_name="market_model_test")

    return combined_stocks, t_tests_values, w_tests_values, event_CARs, single_test

##########################################################################################################
#checks the event dates during the IRAN/US/ISRAEL conflict and combines them into dataframes that can be presented more easily instead of a bunch of ARs and CARs and values
#that arent easily 

event_dates = ["2026-03-02", "2026-04-08", "2026-04-20"]

t_tests = pd.DataFrame(index = event_dates, columns= ["p-value", "significance α 0.01", "significance α 0.05"])
w_tests = pd.DataFrame(index = event_dates, columns= ["p-value", "significance α 0.01", "significance α 0.05"])
t_test_p_values = pd.DataFrame(index = event_dates, columns= ["p-value"])
w_test_p_values = pd.DataFrame(index = event_dates, columns= ["p-value"])
CARs = pd.DataFrame(index = event_dates)
market_model_test = pd.DataFrame(index = event_dates)
plot_folder = Path("results/plots")
plot_folder.mkdir(parents=True, exist_ok=True)


for i in event_dates:
    combined_stocks, t_tests_values, w_tests_values, event_CARs, single_test = analisys(i)
    print(f"{i} wilcoxon: t-statistic {w_tests_values[0]}")
    print(f"{i} t-test: t-statistic {t_tests_values[0]}")
    t_tests.loc[i,"p-value"] = t_tests_values[1]
    w_tests.loc[i,"p-value"] = w_tests_values[1] 
    if t_tests.loc[i,"p-value"]<0.01:
        t_tests.loc[i,"significance α 0.01"] = "significant"
    else:
        t_tests.loc[i,"significance α 0.01"] = "not significant"
    
    if t_tests.loc[i,"p-value"]<0.05:
        t_tests.loc[i,"significance α 0.05"] = "significant"
    else:
        t_tests.loc[i,"significance α 0.05"] = "not significant"

    if w_tests.loc[i,"p-value"]<0.01:
        w_tests.loc[i,"significance α 0.01"] = "significant"
    else:
        w_tests.loc[i,"significance α 0.01"] = "not significant"
    
    if w_tests.loc[i,"p-value"]<0.05:
        w_tests.loc[i,"significance α 0.05"] = "significant"
    else:
        w_tests.loc[i,"significance α 0.05"] = "not significant"
    
    for y in single_test.index:
        if single_test.loc[y]["p-value"] < 0.01:
            market_model_test.loc[i,f"{y} α 0.01"] = "s"
        else:
            market_model_test.loc[i,f"{y} α 0.01"] = "ns"

        if single_test.loc[y]["p-value"] < 0.05:
            market_model_test.loc[i,f"{y} α 0.05"] = "s"
        else:
            market_model_test.loc[i,f"{y} α 0.05"] = "ns"

    for x in event_CARs.columns:
        CARs.loc[i,x] = event_CARs.iloc[0][x]

    fig = func.plot_data(combined_stocks)

    fig.write_html(plot_folder / f"CARs_{i}.html")

CARs = CARs.fillna("not included")
market_model_test = market_model_test.fillna("not included")


results_folder = Path("results")
results_folder.mkdir(exist_ok=True)

excel_path = results_folder / "analysis_results.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    t_tests.to_excel(writer, sheet_name="t_tests")
    w_tests.to_excel(writer, sheet_name="w_tests")
    CARs.to_excel(writer, sheet_name="CARs")
    market_model_test.to_excel(writer, sheet_name="market_model_test")


print(f"t-test: {t_tests}")
print(f"wilcoxon test: {w_tests}")
print(f"CARs: {CARs}")
print(f"Market model test: {market_model_test}")
