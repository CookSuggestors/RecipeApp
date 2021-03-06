import requests
import numpy as np
import pandas as pd
import random
from time import sleep
import os

class rakuten_api:

    # 楽天APIを呼び出し，入力食材のマッチ数の多い順にソートする
    # 楽天APIが受け取るデータ(リスト形式)：input_food_list
    def call_api(self, input_food_list):        

        categoryId_list = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, \
                        26, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55] # レシピのカテゴリIDリスト

        target_categoryId_list = random.sample(categoryId_list, 3) # レシピのカテゴリIDリストからランダムにカテゴリを抽出

        REQUEST_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
        API_ID = os.environ["API_ID"]

        api_result = [] # json結果を入れるためのリスト

        # カテゴリの数だけAPIを呼び出す
        for categoryId in target_categoryId_list:
            
            serch_params = {
            "format" : "json",
            "applicationId" : API_ID,
            "formatVersion" : 2,
            "elements" : "recipeTitle,recipeMaterial,recipeCost,foodImageUrl,recipeUrl", # レシピタイトル，食材，費用，画像URL，レシピURL
            "categoryId" : categoryId # レシピのカテゴリID
            }
            response = requests.get(REQUEST_URL, serch_params) # レスポンス結果
            result = response.json() # レスポンス結果をjson形式で表示
            api_result.extend(result['result']) 
            sleep(1) # APIへの連続したリクエストを防止するため．1秒は最低必要．

        idx_len = len(target_categoryId_list) * 4 # カテゴリ毎のレシピ数：カテゴリ数 × 上位4件のレシピ

        for idx in range(idx_len):
            
            matched_syokuzai_list = set(input_food_list) & set(api_result[idx]['recipeMaterial']) # マッチした食材名リスト
            not_matched_syokuzai_list = set(input_food_list) ^ set(api_result[idx]['recipeMaterial']) # マッチしなかった食材名リスト
            match_num = len(matched_syokuzai_list)  # マッチした食材数
            api_result[idx]['matchNum'] = match_num # jsonファイルに'マッチ数'の要素を追加
            api_result[idx]['notMatchRecipeMaterial'] = list(not_matched_syokuzai_list) # jsonファイルに'マッチしなかった食材名リスト'の要素を追加

        sorted_api_result = sorted(api_result, key=lambda x: x['matchNum'], reverse=True) # マッチ数が多い順に表示する

        return sorted_api_result

    # 上位n件のレシピを出力する
    def output_recipe(self, recipe_num, sorted_api_result):
        result = []
        for i in range(recipe_num): 
            result.append(sorted_api_result[i])

        return result