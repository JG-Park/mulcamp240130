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

def custom_subheader(title, color):
    st.markdown(f'<h3 style="color: {color};">{title}</span>', unsafe_allow_html=True)
    

def plot_bar_chart(data, x_label, y_label, title):
    custom_subheader(title, '#9ED2BE')
    st.bar_chart(data)

    st.xlabel = x_label
    st.ylabel = y_label

def main():
    st.title("Instacart Data Dashboard")

    # 데이터 불러오기
    orders_df = load_data('orders')
    order_products_train_df = load_data('order_products__train')
    order_products_prior_df = load_data('order_products__prior')

    # 데이터셋 내 주문 수 통계
    cnt_srs = orders_df.eval_set.value_counts()
    plot_bar_chart(cnt_srs, 'Eval set type', 'Number of Occurrences', '각 데이터세트의 행 수')

    # 각 사용자별 주문 분배
    cnt_srs = orders_df.groupby("user_id")["order_number"].aggregate(np.max).reset_index()
    cnt_srs = cnt_srs.order_number.value_counts()
    plot_bar_chart(cnt_srs, 'Maximum order number', 'Number of Occurrences', '각 사용자별 주문 분배')

    # 요일별 주문빈도
    plot_bar_chart(orders_df['order_dow'].value_counts(), 'Day of week', 'Count', '요일별 주문빈도')

    # 시간대별 주문 빈도
    plot_bar_chart(orders_df['order_hour_of_day'].value_counts(), '시간대', '주문 횟수', '시간대별 주문 빈도')

    # 주문 간격 확인
    plot_bar_chart(orders_df['days_since_prior_order'].value_counts(), '이전 주문 이후 일수', '주문 횟수', '주문 간격 빈도')

    # 이전 주문 비율 (prior set 및 train set)
    custom_subheader('이전 주문 비율', '#9ED2BE')
    prior_reorder_ratio = order_products_prior_df['reordered'].sum() / order_products_prior_df.shape[0]
    train_reorder_ratio = order_products_train_df['reordered'].sum() / order_products_train_df.shape[0]


    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("prior set", f"{prior_reorder_ratio:.2%}")
    with col2:
        st.metric("train set", f"{train_reorder_ratio:.2%}")

    # 재주문이 없는 상품 비율
    custom_subheader('재주문이 없는 상품 비율', '#9ED2BE')

    # prior set
    grouped_df_prior = order_products_prior_df.groupby("order_id")["reordered"].aggregate("sum").reset_index()
    grouped_df_prior["reordered"].loc[grouped_df_prior["reordered"] > 1] = 1
    no_reorder_ratio_prior = grouped_df_prior.reordered.value_counts(normalize=True).loc[0]

    # train set
    grouped_df_train = order_products_train_df.groupby("order_id")["reordered"].aggregate("sum").reset_index()
    grouped_df_train["reordered"].loc[grouped_df_train["reordered"] > 1] = 1
    no_reorder_ratio_train = grouped_df_train.reordered.value_counts(normalize=True).loc[0]

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("prior set", f"{no_reorder_ratio_prior:.2%}")
    with col2:
        st.metric("train set", f"{no_reorder_ratio_train:.2%}")

if __name__ == "__main__":
    main()
