"""
分析 Fashion Dataset 的資料結構
- 分析 styles.csv 的欄位和資料分布
- 分析 styles/*.json 的詳細資訊
- 統計資料完整性
"""

import pandas as pd
import json
import os
from pathlib import Path
from collections import Counter

# 設定資料路徑
BASE_DIR = Path(__file__).parent.parent.parent
DATASET_DIR = BASE_DIR / "fashion-dataset"
CSV_FILE = DATASET_DIR / "styles.csv"
JSON_DIR = DATASET_DIR / "styles"
IMAGES_DIR = DATASET_DIR / "images"

def analyze_csv():
    """分析 styles.csv 檔案"""
    print("=" * 80)
    print("📊 分析 styles.csv")
    print("=" * 80)
    
    # 讀取 CSV
    df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
    
    print(f"\n✅ 成功讀取 CSV 檔案")
    print(f"📦 總商品數量: {len(df):,}")
    
    # 顯示欄位資訊
    print(f"\n📋 欄位列表 ({len(df.columns)} 個欄位):")
    print("-" * 80)
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        print(f"{i:2d}. {col:25s} | 型態: {str(dtype):10s} | 缺失: {null_count:6,} ({null_pct:5.2f}%)")
    
    # 顯示前 5 筆資料
    print(f"\n📄 前 5 筆資料:")
    print("-" * 80)
    print(df.head())
    
    # 統計各欄位的分布
    print(f"\n📊 資料分布統計:")
    print("-" * 80)
    
    categorical_cols = ['gender', 'masterCategory', 'subCategory', 'articleType', 
                       'baseColour', 'season', 'usage']
    
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n▶ {col}:")
            value_counts = df[col].value_counts()
            for val, count in value_counts.head(10).items():
                pct = (count / len(df)) * 100
                print(f"  - {str(val):30s}: {count:6,} ({pct:5.2f}%)")
            if len(value_counts) > 10:
                print(f"  ... 還有 {len(value_counts) - 10} 個其他值")
    
    # 年份統計
    if 'year' in df.columns:
        print(f"\n▶ year:")
        year_counts = df['year'].value_counts().sort_index()
        for year, count in year_counts.items():
            if pd.notna(year):
                pct = (count / len(df)) * 100
                print(f"  - {int(year)}: {count:6,} ({pct:5.2f}%)")
    
    return df

def analyze_json_files(df, sample_size=10):
    """分析 styles/*.json 檔案"""
    print("\n" + "=" * 80)
    print("📊 分析 styles/*.json 檔案")
    print("=" * 80)
    
    if not JSON_DIR.exists():
        print(f"❌ 找不到 JSON 目錄: {JSON_DIR}")
        return
    
    json_files = list(JSON_DIR.glob("*.json"))
    print(f"\n📦 JSON 檔案數量: {len(json_files):,}")
    
    if len(json_files) == 0:
        print("⚠️  沒有找到 JSON 檔案")
        return
    
    # 收集所有欄位
    all_fields = set()
    sample_data = []
    
    print(f"\n🔍 分析前 {sample_size} 個 JSON 檔案...")
    
    for i, json_file in enumerate(json_files[:sample_size]):
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                all_fields.update(data.keys())
                sample_data.append(data)
            except json.JSONDecodeError:
                print(f"⚠️  無法解析: {json_file.name}")
    
    print(f"\n📋 JSON 檔案包含的欄位 ({len(all_fields)} 個):")
    print("-" * 80)
    for field in sorted(all_fields):
        print(f"  - {field}")
    
    # 顯示範例資料
    if sample_data:
        print(f"\n📄 第一個 JSON 檔案的完整內容:")
        print("-" * 80)
        print(json.dumps(sample_data[0], indent=2, ensure_ascii=False))
        
        # 分析價格資訊
        prices = [d.get('price') for d in sample_data if d.get('price')]
        if prices:
            print(f"\n💰 價格資訊範例:")
            for i, price in enumerate(prices[:5], 1):
                print(f"  {i}. {price}")

def check_images(df):
    """檢查圖片檔案存在性"""
    print("\n" + "=" * 80)
    print("🖼️  檢查圖片檔案")
    print("=" * 80)
    
    if not IMAGES_DIR.exists():
        print(f"❌ 找不到圖片目錄: {IMAGES_DIR}")
        return
    
    # 統計圖片數量
    image_files = list(IMAGES_DIR.glob("*.jpg"))
    print(f"\n📦 圖片檔案數量: {len(image_files):,}")
    
    # 檢查前 100 個商品的圖片是否存在
    sample_ids = df['id'].head(100).tolist()
    missing_count = 0
    
    for product_id in sample_ids:
        img_path = IMAGES_DIR / f"{product_id}.jpg"
        if not img_path.exists():
            missing_count += 1
    
    print(f"✅ 前 100 個商品中，{100 - missing_count} 個有對應圖片")
    print(f"⚠️  前 100 個商品中，{missing_count} 個缺少圖片")
    
    if missing_count > 0:
        print(f"\n💡 建議: 部分商品可能沒有對應的圖片檔案")

def generate_summary():
    """生成摘要報告"""
    print("\n" + "=" * 80)
    print("📝 分析摘要")
    print("=" * 80)
    
    print(f"""
✅ CSV 檔案位置: {CSV_FILE}
✅ JSON 檔案目錄: {JSON_DIR}
✅ 圖片檔案目錄: {IMAGES_DIR}

下一步建議:
1. 根據分析結果設計資料庫結構 (Task 1.4)
2. 建立 DBML 檔案定義資料表
3. 處理缺失值策略
4. 設計資料清洗流程
    """)

def main():
    """主程式"""
    print("\n🚀 Fashion Dataset 資料分析工具")
    print(f"📁 資料集路徑: {DATASET_DIR}")
    
    # 檢查 CSV 檔案是否存在
    if not CSV_FILE.exists():
        print(f"\n❌ 找不到 CSV 檔案: {CSV_FILE}")
        print("請確認 fashion-dataset/styles.csv 檔案存在")
        return
    
    # 1. 分析 CSV
    df = analyze_csv()
    
    # 2. 分析 JSON
    analyze_json_files(df, sample_size=10)
    
    # 3. 檢查圖片
    check_images(df)
    
    # 4. 生成摘要
    generate_summary()
    
    print("\n✅ 分析完成！\n")

if __name__ == "__main__":
    main()
