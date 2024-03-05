import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# アプリのタイトルを設定
st.title('日程調整')

# ユーザーが開始日を設定
start_date = st.date_input('開始日', datetime.now())
end_date = start_date + timedelta(days=6)  # 開始日から6日後
date_list = pd.date_range(start_date, end_date).tolist()  # 選択された開始日から日程リストを生成

# 初期データフレームの作成
if 'df' not in st.session_state or st.button('開始日を設定'):
    st.session_state['df'] = pd.DataFrame({
        '日付': [date.strftime('%Y-%m-%d') for date in date_list],
        **{f'ユーザー{j}': ['未' for _ in date_list] for j in range(1, 21)},  # 20ユーザー分の列を動的に生成
    })

# ユーザー入力の取得
for index, date in enumerate(st.session_state['df']['日付']):
    with st.expander(f"{date}"):
        for j in range(1, 21):  # 各ユーザーの選択肢、20人まで対応
            choice = st.radio(f"ユーザー{j}:", ('〇', '×', '未'), key=f"{index}-{j}", index=2)
            st.session_state['df'].at[index, f'ユーザー{j}'] = choice

# 選択肢の表示
st.write('各日にちの選択肢:')
st.write(st.session_state['df'])

# 集計結果の表示
st.write('集計結果:')
for date in st.session_state['df']['日付']:
    day_data = st.session_state['df'][st.session_state['df']['日付'] == date]
    # 〇と×の数をカウント
    count_o = (day_data == '〇').sum().sum()  # '〇'の総数
    count_x = (day_data == '×').sum().sum()  # '×'の総数
    st.write(f"{date}: 〇 = {count_o}, × = {count_x}")
