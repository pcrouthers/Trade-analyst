import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime
import plotly.express as px
from ollama import generate

# Function to load and save trades
def load_trades():
    try:
        return pd.read_csv('trades.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Time Entry', 'Market', 'Trade Direction', 'Entry Price', 'Position Size', 
                                      'Exit Price', 'Take Profit', 'Stop Loss', 'Profit/Loss', 'Trade Rationale', 
                                      'Market Conditions', 'Emotional Reflection', 'Post-Trade Analysis'])

def save_trades(df):
    df.to_csv('trades.csv', index=False)

# Initialize DataFrame
df = load_trades()

# Streamlit tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trade Journal", "Performance Metrics", "Cumulative P/L Over Time", "P/L Calendar", "AI Trade Analyst"])

# Sidebar for Trade Journal Entry
with st.sidebar:
    st.subheader("Trade Journal Entry")
    
    date = st.date_input("Date", datetime.today())
    time_entry = st.time_input("Time Entry", datetime.now().time())
    market = st.selectbox("Market", ['Micro E-mini Nasdaq', 'E-mini S&P 500'])
    trade_direction = st.selectbox("Trade Direction", ['Long', 'Short'])
    entry_price = st.number_input("Entry Price", format="%.2f")
    position_size = st.number_input("Position Size", min_value=1)
    exit_price = st.number_input("Exit Price", format="%.2f")
    take_profit = st.number_input("Take Profit", format="%.2f", value=0.0)
    stop_loss = st.number_input("Stop Loss", format="%.2f", value=0.0)
    trade_rationale = st.text_area("Trade Rationale")
    market_conditions = st.text_area("Market Conditions")
    emotional_reflection = st.text_area("Emotional Reflection")
    post_trade_analysis = st.text_area("Post-Trade Analysis")

    if st.button("Save Trade"):
        profit_loss = (exit_price - entry_price) * position_size if trade_direction == 'Long' else (entry_price - exit_price) * position_size
        new_trade = pd.DataFrame({
            'Date': [date],
            'Time Entry': [time_entry],
            'Market': [market],
            'Trade Direction': [trade_direction],
            'Entry Price': [entry_price],
            'Position Size': [position_size],
            'Exit Price': [exit_price],
            'Take Profit': [take_profit],
            'Stop Loss': [stop_loss],
            'Profit/Loss': [profit_loss],
            'Trade Rationale': [trade_rationale],
            'Market Conditions': [market_conditions],
            'Emotional Reflection': [emotional_reflection],
            'Post-Trade Analysis': [post_trade_analysis]
        })
        
        df = pd.concat([df, new_trade], ignore_index=True)  # Replaced append with concat
        save_trades(df)
        st.success("Trade saved successfully!")

    if st.button("Delete All Trades"):
        df = pd.DataFrame(columns=df.columns)  # Reset the DataFrame
        save_trades(df)
        st.success("All trades deleted!")

# Tab 1: Trade Journal
with tab1:
    st.subheader("Trade Journal")
    st.dataframe(df)

# Tab 2: Performance Metrics
with tab2:
    st.subheader("Performance Metrics")
    if not df.empty:
        st.write(f"Total Trades: {len(df)}")
        st.write(f"Total Profit/Loss: ${df['Profit/Loss'].sum():.2f}")
        st.write(f"Winning Trades: {len(df[df['Profit/Loss'] > 0])}")
        st.write(f"Losing Trades: {len(df[df['Profit/Loss'] < 0])}")
        st.write(f"Win Rate: {len(df[df['Profit/Loss'] > 0]) / len(df) * 100:.2f}%")
    else:
        st.write("No trades to display.")

# Tab 3: Cumulative P/L Over Time
with tab3:
    st.subheader("Cumulative Profit/Loss Over Time")
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is in datetime format
        cumulative_pl = df.groupby('Date')['Profit/Loss'].sum().cumsum().reset_index()
        fig = px.line(cumulative_pl, x='Date', y='Profit/Loss', title='Cumulative Profit/Loss Over Time', labels={'Profit/Loss': 'Cumulative P/L'})
        st.plotly_chart(fig)
    else:
        st.write("No trades to display.")

# Tab 4: P/L Calendar

   

# Tab 5: AI Trade Analyst
with tab5:
    st.subheader("AI Trade Analyst")
    
    if st.button("Analyze Trades"):
        # Check if the required columns are in the DataFrame
        required_columns = ['Date', 'Market', 'Trade Direction', 'Entry Price', 'Exit Price', 
                            'Profit/Loss', 'Trade Rationale', 'Market Conditions']
        
        if all(col in df.columns for col in required_columns):
            trade_analysis_input = df[required_columns].to_string(index=False)
            
            # Show a spinner while AI processes the request
            with st.spinner("Analyzing trades..."):
                # Call the AI model (assuming 'generate' function for trade analysis)
                response = generate('phi3', f"What can I improve on based on the following trades?\n{trade_analysis_input} Keep response concise")
            
            # Display the AI-generated response
            st.success("AI Analysis:")
            st.write(response['response'])
        else:
            st.warning("Not all required columns are present in the DataFrame. Please ensure trades have been saved correctly.")