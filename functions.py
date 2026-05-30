import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px
from scipy.stats import ttest_1samp
from scipy.stats import wilcoxon
from scipy.stats import t as student_t
#https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
#https://media.datacamp.com/legacy/image/upload/v1676302827/Marketing/Blog/Data_Wrangling_Cheat_Sheet.pdf
"""
tickers = ["XOM", "CVX", "SHEL", "BP", "TTE", "PBR", "ONGC.NS", "EQNR", "NWMD.TA"]

for ticker in tickers:
    df = yf.download(
        ticker,
        period="max",
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        print(ticker, "no data")
    else:
        print(ticker, df.index.min().date(), "to", df.index.max().date())
"""
#########################################################################################

#https://ranaroussi.github.io/yfinance/reference/index.html
#get_finance_data downloads single ticker data and returns single level index data frame with only adjusted closing data
#auto adjust = True already adjusts for stock splits and dividends. so when the stock sinks but the value for the shareholders didnt
#really, it already adjusts it.
#repair = true already fixed a variety of price errors https://ranaroussi.github.io/yfinance/advanced/price_repair.html
#sadly only perfect for us marked (ask if okay or if you should try to apply the ideas manually) - i dont really understand how it 
#could only work perfect for us prices... why... wouldnt they program it to just automatically work with all tickers? they surely
#didnt go through all the us data. i dont understand things, im very bad at programing.


def get_finance_data(ticker, start, end):
    data = yf.download(ticker, start, end, progress=False, interval="1d", repair = True, auto_adjust= True)
    if data.empty:
        print(f"{ticker} is not available")
    else:
        data = data[["Close"]]
        data.columns = data.columns.droplevel(0)
        return data



#check_data takes single column data(adjusted closing stock price) and cleans it for further use
def check_data(data, estimation_window=True):
    #check_data can be used to check for estimation window(window will be set 150 so OLS can atleast calculate 120 values)
    #and for event window, which needs a stricter restriction because of the smaller window size
    if data is None:
        return None

    if data.empty:
        return None

    if estimation_window == True:
        max_missing = 0.2
    else:
        max_missing = 0.1
    
    data = data.sort_index() #Sorts dates in a proper fashion
    data = data.groupby(data.index).first() #Uses first date only -> removes duplicate dates
    data = data.where(data > 0) #only uses stock prices over 0
    
    missing_data = data.iloc[:,0].isna().mean() #mean of boolean list gives percentages

    if missing_data > max_missing:
        print("missing data is too big")
        return None
    else:
        return data
    
#this function is very self explanatory. as seen in the mathematical explenation, the returns are just the return change from the
#prior day. so we can just use the percentage change and already got it
def calculate_returns(data):
    if data is None:
        return None
    
    if data.empty:
        return None
    

    data[f"{data.columns[0]} Returns"] = data.iloc[:,0].pct_change()
    return data

#this function first calculates alpha and beta with OLS through a statsmodel function.
#This seems a little messy because alpha and beta are just one value and its weird in the dataframe to have a series full of just one
#value, but i didnt really know how to do it cleaner and it seemed convenient to me. This dataframe wont be used to plot things anyways
#so i thought this is okay. 
#Its alos kinda messy, because i call on the market data and the stock data through the column number (iloc) and not the name, but i
#had the problem that they were the same name first ("Returns") because in the function calculate_returns i initialy just named them
#"Returns". I had to join them, because OLS needs no missing values or infitites, but to join them they need different names.
#so then i just added the individual stock name to the "Return" column. This might be a little messy later when im calculating ER and AR
#but it works right now so yeah, there you go
#https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html how to use OLS statsmodel   
def calculate_alpha_beta(stock_data, market_data):
    temp_data = stock_data.iloc[:,[1]].join(market_data.iloc[:,[1]], how = "inner")
    temp_data = temp_data.dropna()

    y = temp_data.iloc[:,0]
    X = temp_data.iloc[:,1]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()


    stock_data["alpha"] = model.params.iloc[0]
    stock_data["beta"] = model.params.iloc[1]
    stock_data["residual variance"] = model.mse_resid
    stock_data["degrees of freedom"] = model.df_resid
    print(stock_data)
    return stock_data



#So here we put in the data frame for estimation window, because we need the alpha and beta and the event window to actually calculate
#the expected and abnormal returns. Its the same problem as incalculate_alpha_beta, that i have to use iloc[:,[1]] to call on the returns
#instead of just ["Returns"]. I could have said [f"{event_data.columns[0]} Returns] but that looked even messier to me idk.
def calculate_ER_AR_CAR(estimation_data, event_data, market_data):  
    event_data["Expected Returns"] = estimation_data.iloc[0]["alpha"] + estimation_data.iloc[0]["beta"] * market_data.iloc[:,1]
    event_data["Abnormal Returns"] = event_data.iloc[:,1] - event_data["Expected Returns"]
    event_data["CAR"] = event_data["Abnormal Returns"].cumsum()
    return event_data

#So this one just makes a plotable multilayer dataframe with all the stocks and theyre AR and CAR
def combine_stocks(*data):
    combined_data = pd.DataFrame()

    for i in data:
        combined_data[i.columns[0], "Abnormal returns"] = i["Abnormal Returns"]
        combined_data[i.columns[0], "Comulative abnormal returns"] = i["CAR"]
        combined_data.columns = pd.MultiIndex.from_tuples(combined_data.columns)
        #combined_data = combined_data.dropna()
    return combined_data

#https://media.datacamp.com/legacy/image/upload/v1668605954/Marketing/Blog/Plotly_Cheat_Sheet.pdf
def plot_data(data):
    col_len = data.shape[1]
    col = []
    
    i = 0
    while i < col_len:
        
        col.append(i)
        i += 2
    data_CAR = data.iloc[:, 1: : 2]
    data_CAR.columns = data_CAR.columns.droplevel(1)

    fig = px.line(
        data_CAR,
        x = data_CAR.index,
        y = data_CAR.columns,
        title = "CARs of all companies"
    )
    fig.add_hline(y=0, line_dash = "dash")
    fig.show()

#https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
def t_test(data, date):
    data_ARs = data.iloc[:, 0 : : 2]

    data_ARs.columns = data_ARs.columns.droplevel(1)
    
    event_date_index = data_ARs.index.get_loc(date)
    start_position = event_date_index -5
    end_position = event_date_index + 6


    data_ARs = data_ARs.iloc[start_position:end_position, :]


    event_CARs = {}
    for i in range(len(data_ARs.columns)):
        event_CARs[data_ARs.columns[i]] = data_ARs.iloc[:,i].sum()


    alpha = 0.01
    test = ttest_1samp(list(event_CARs.values()), 0, nan_policy= "omit", alternative= "two-sided")
    t_value = test.statistic
    p_value = test.pvalue
    

    if p_value > alpha:
        
        return t_value, p_value, f"Accept t-test Null Hypothysis. CARs are too close to 0 to reject - date is not significant"
    else:
        
        return t_value, p_value, f"Reject t-test Null Hypothysis.  CARs are significantly different from 0 - date is significant"
    
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
def wilcoxon_test(data, date):
    data_ARs = data.iloc[:, 0 : : 2]
    data_ARs.columns = data_ARs.columns.droplevel(1)
    event_date_index = data_ARs.index.get_loc(date)
    start_position = event_date_index -5
    end_position = event_date_index + 6
    data_ARs = data_ARs.iloc[start_position:end_position, :]


    event_CARs = {}
    for i in range(len(data_ARs.columns)):
        event_CARs[data_ARs.columns[i]] = data_ARs.iloc[:,i].sum()
 

    alpha = 0.01
    test = wilcoxon(list(event_CARs.values()), 0, nan_policy = "omit", alternative= "two-sided")
    w_value = test.statistic
    p_value = test.pvalue


    if p_value > alpha:
        return w_value, p_value, f"Accept Wilcoxon Null Hypothysis. CAR values are around zero - date is not significant"
    else:
        return w_value, p_value, f"Reject Wilcoxon Null Hypothysis. CAR values are positve/negative heavy - date is significant"
    


def single_comp_CAR_test(event_data, residuals, date):
    data_ARs = event_data.iloc[:, 0 : : 2]
    data_ARs.columns = data_ARs.columns.droplevel(1)
    event_date_index = data_ARs.index.get_loc(date)
    start_position = event_date_index -5
    end_position = event_date_index + 6
    data_ARs = data_ARs.iloc[start_position:end_position, :]
    alpha = 0.01


    event_CARs = pd.DataFrame(index = ["CAR"])
    for i in range(len(data_ARs.columns)):
        col_ARs = data_ARs.columns[i]
        event_CARs.loc["CAR", col_ARs] = data_ARs.iloc[:,i].sum()


    L = len(data_ARs)
    t_CAR = pd.DataFrame(index=["tCAR"])
    for i in range(len(event_CARs.columns)):
        col_CARs = event_CARs.columns[i]
        t_CAR.loc["tCAR", col_CARs] = (event_CARs.iloc[0, i])/(np.sqrt(L*residuals.iloc[0, i]))
    

    #https://www.geeksforgeeks.org/machine-learning/how-to-find-a-p-value-from-a-t-score-in-python/#how-to-find-a-pvalue-from-a-tscore
    single_com_test = pd.DataFrame(index = t_CAR.columns, columns = (["p-value", "α 0.01", "α 0.05"]), dtype = object)
    for i in range(len(t_CAR.columns)):
        col_t_Car = t_CAR.columns[i]
        single_com_test.loc[col_t_Car, "p-value"] = student_t.sf(np.abs(t_CAR.iloc[0,i]), ((residuals.iloc[1,i])-2))*2
        if single_com_test.loc[col_t_Car, "p-value"] < 0.01:
            single_com_test.loc[col_t_Car, "α 0.01"] = ("Reject null hypothesis at alpha 0.01. Abnormal Returns are statistically significantly different to estimation data")
        else:
            single_com_test.loc[col_t_Car, "α 0.01"] = ("Fail to reject null hypothesis at alpha 0.01. Abnormal Returns are not statistically significantly different to estimation data")
        
        if single_com_test.loc[col_t_Car, "p-value"] < 0.05:
            single_com_test.loc[col_t_Car, "α 0.05"] = ("Reject null hypothesis at alpha 0.05. Abnormal Returns are statistically significantly different to estimation data")
        else:
            single_com_test.loc[col_t_Car, "α 0.05"] = ("Fail to reject null hypothesis at alpha 0.05. Abnormal Returns are not statistically significantly different to estimation data")
    return single_com_test



##############################################################################################################
