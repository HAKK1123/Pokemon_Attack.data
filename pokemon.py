# 必要なライブラリをインポート
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import japanize_matplotlib
import requests

# Streamlitアプリのタイトルを設定
st.title('ポケモンデータ可視化アプリ')
st.caption("800体のポケモンデータを読み込み、800体のポケモンの攻撃のデータを可視化します。\n"
           "ポケモンの名前を入力すると詳細情報を表示することができます。")
# カレントディレクトリにファイルがなければダウンロード
if not os.path.exists('pokemon.csv'):
    url = 'https://raw.githubusercontent.com/swarajpande4/pokemon-analysis/main/dataset/pokemon.csv'
    response = requests.get(url)
    with open('pokemon.csv', 'wb') as file:
        file.write(response.content)

# ポケモンデータの読み込み
pokemon_data = pd.read_csv('pokemon.csv')

# japanese_nameから日本語の名前だけを抽出
pokemon_data['japanese_name'] = pokemon_data['japanese_name'].apply(lambda x: re.findall(r'[\u30A1-\u30FF]+', x)[0])

# statusのカラム名を日本語に変換するための辞書
status_dic = {'hp': 'HP', 'attack': 'こうげき', 'defense': 'ぼうぎょ', 'sp_attack': 'とくこう', 'sp_defense': 'とくぼう', 'speed': 'すばやさ'}

# statusのカラム名を日本語に変換
pokemon_data.columns = pokemon_data.columns.map(lambda x: status_dic.get(x, x))

# type1とtype2を日本語に変換するための辞書
type_dict = {
    'grass': 'くさ', 'fire': 'ほのお', 'water': 'みず', 'bug': 'むし', 'normal': 'ノーマル',
    'poison': 'どく', 'electric': 'でんき', 'ground': 'じめん', 'fairy': 'フェアリー', 'fighting': 'かくとう',
    'psychic': 'エスパー', 'rock': 'いわ', 'ghost': 'ゴースト', 'ice': 'こおり', 'dragon': 'ドラゴン',
    'dark': 'あく', 'steel': 'はがね', 'flying': 'ひこう', pd.NA: 'タイプなし'
}

# type1とtype2を日本語に変換
pokemon_data['type1'] = pokemon_data['type1'].map(lambda x: type_dict.get(x, x))
pokemon_data['type2'] = pokemon_data['type2'].map(lambda x: type_dict.get(x, x))

# 母平均
attack_pop_mean = pokemon_data['こうげき'].mean()

# ヒストグラムを描画
sns.histplot(data=pokemon_data, x='こうげき', bins=20)
# タイトルを設定
plt.title(f'ポケモン８００体の「こうげき」のヒストグラム')
# フィギュアオブジェクトを取得
fig = plt.gcf()
# MatplotlibのフィギュアオブジェクトをStreamlitに渡す
st.pyplot(fig)

# 母分散
attack_pop_var = pokemon_data['こうげき'].var(ddof=0)

# 母標準偏差
attack_pop_std = pokemon_data['こうげき'].std(ddof=0)

# ヒストグラムを描画
ax = sns.histplot(data=pokemon_data, x='こうげき', bins=20)
# Axesオブジェクトのy軸の下限と上限を取得
ymin, ymax = ax.get_ylim()
# 母平均の位置を示す矢印を描画
plt.arrow(attack_pop_mean, ymax, 0, -ymax, length_includes_head=True, color='red', width=.5, head_length=20.0)
# テキストを印字
plt.text(attack_pop_mean*1.01, ymax*.9, f'母平均：{attack_pop_mean:.1f}', color='red', fontsize=24)
# 母標準偏差の示す矢印を描画
plt.arrow(attack_pop_mean, 10, attack_pop_std, 0, length_includes_head=True, color='red', width=2)
plt.arrow(attack_pop_mean, 10, -attack_pop_std, 0, length_includes_head=True, color='red', width=2)
# テキストを印字
t = plt.text(attack_pop_mean*1.04, 17, f'母標準偏差：{attack_pop_std:.1f}', color='red', fontsize=24)
# テキストを囲むバウンディングボックスを描画
t.set_bbox(dict(facecolor='w', alpha=0.5))

# タイプ別の「こうげき」の箱ひげ図を描画
plt.figure(figsize=(10, 6))
sns.boxplot(data=pokemon_data, x='type1', y='こうげき').set_title('タイプ別の「こうげき」の箱ひげ図')
plt.xticks(rotation=45)
fig_boxplot = plt.gcf()
st.pyplot(fig_boxplot)



# ポケモンの種類ごとの分布をヒストグラムで表示
plt.figure(figsize=(10, 6))
sns.histplot(data=pokemon_data, x='type1')
plt.xticks(rotation=45)
fig_hist = plt.gcf()
st.pyplot(fig_hist)

# ポケモンの名前を入力して詳細情報を表示
pokemon_name = st.text_input('ポケモンの名前を入力してください')
selected_pokemon = pokemon_data[pokemon_data['japanese_name'].str.contains(pokemon_name, case=False)]
if not selected_pokemon.empty:
    st.write(selected_pokemon)
else:
    st.write('該当するポケモンが見つかりません')


