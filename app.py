# -*- coding:utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
@st.cache_data

def load_data(df_name):
    # CSV 파일 읽어오기
    df = pd.read_csv(f"./input/{df_name}.csv")
    return df

def plot_bar_chart(data, x_label, y_label, title):
    st.title(title)
    st.bar_chart(data)

def main():
    st.title("Instacart Data Dashboard")

    # 데이터 불러오기
    orders_df = load_data('orders')

    # 1. 데이터셋 내 주문 수 통계
    cnt_srs = orders_df.eval_set.value_counts()
    plot_bar_chart(cnt_srs, 'Eval set type', 'Number of Occurrences', '각 데이터세트의 행 수')

    # 2. 4 to 100 orders of a customer
    cnt_srs = orders_df.groupby("user_id")["order_number"].aggregate(np.max).reset_index()
    cnt_srs = cnt_srs.order_number.value_counts()
    plot_bar_chart(cnt_srs, 'Maximum order number', 'Number of Occurrences', '각 사용자별 주문 분배')

    # 3. Ordering habit changes with day of week
    plot_bar_chart(orders_df['order_dow'].value_counts(), 'Day of week', 'Count', '요일별 주문빈도')

    # 4. Distribution with respect to time of the day
    plot_bar_chart(orders_df['order_hour_of_day'].value_counts(), 'Hour of day', 'Count', '시간대별 주문 빈도')

    # 나머지 코드...

if __name__ == "__main__":
    main()
