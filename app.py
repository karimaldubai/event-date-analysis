import streamlit as st
from main import analisys
from datetime import datetime
from datetime import timedelta
import plotly.express as px

st.title("Oil Stock Analysis around Event Date")

if "event_date" not in st.session_state:
    st.session_state.event_date = None

user_input = st.chat_input("Please type Date of event in yyyy-mm-dd: ", key = "event_date_input_babababababa")

if user_input is not None:
        try:
            event_date = datetime.strptime(user_input, "%Y-%m-%d")
            if event_date.weekday() >= 5:
                st.session_state.event_date = None
                st.error("Please choose a weekday. Weekends are not trading days.")
            else:
                st.session_state.event_date = event_date
                st.success("Date accepted")
                st.write(f"Date: {user_input}")
        except ValueError:
            st.error("Please use the format yyyy-mm-dd")

if st.session_state.event_date is not None:
    results = analisys(st.session_state.event_date)
    if isinstance(results, dict) and "error" in results:
        st.error(results["error"])
        st.stop()


    st.header(f"result for {st.session_state.event_date}")
    st.subheader("Comulative Abnormal Returns Graph")


    chart_data = results[0].iloc[:,1::2]
    chart_data.columns = chart_data.columns.droplevel(1)


    fig = px.line(
    chart_data,
    x = chart_data.index,
    y = chart_data.columns,
    title = "CARs of all companies"
    )
    fig.add_hline(y=0, line_dash = "dash")
    st.plotly_chart(fig)    


    st.subheader("Abnormal Returns and Cumulative Abnormal Returns")
    st.dataframe(results[0])

    st.subheader("CARs used for T-Test/Wilcoxon test")
    st.dataframe(results[3])
    
    st.subheader("T-Test results")
    st.dataframe(results[1])

    st.subheader("Wilcoxon test results")
    st.dataframe(results[2])

    st.subheader("Market Model Test for individual companies")
    st.dataframe(results[4])


    
