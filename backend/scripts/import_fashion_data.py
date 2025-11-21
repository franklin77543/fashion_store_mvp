"""
匯入 Fashion Dataset 到資料庫
- 讀取 styles.csv 和 styles/*.json
- 資料清理與轉換
- 批次匯入到 SQLite 資料庫
"""
import sys
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models import (
    Gender, MasterCategory, SubCategory, ArticleType,
    Colour, Season, Usage, Brand, Product, ProductImage,
    ProductAttribute, ProductSize
)


class FashionDataImporter:
    """Fashion Dataset 匯入器"""
    
    def __init__(self, dataset_path: str = "../fashion-dataset"):
        self.dataset_path = Path(dataset_path)
        self.csv_path = self.dataset_path / "styles.csv"
        self.json_dir = self.dataset_path / "styles"
        self.images_dir = self.dataset_path / "images"
        
        self.db = SessionLocal()
        
        # 快取查找表 ID (避免重複查詢)
        self.gender_cache: Dict[str, int] = {}
        self.master_category_cache: Dict[str, int] = {}
        self.sub_category_cache: Dict[str, int] = {}
        self.article_type_cache: Dict[str, int] = {}
        self.colour_cache: Dict[str, int] = {}
        self.season_cache: Dict[str, int] = {}
        self.usage_cache: Dict[str, int] = {}
        self.brand_cache: Dict[str, int] = {}
        
        # 統計資料
        self.stats = {
            "total_rows": 0,
            "successful_imports": 0,
            "failed_imports": 0,
            "skipped_rows": 0,
            "lookup_tables": {},
            "errors": []
        }
    
    def import_all(self):
        """執行完整匯入流程"""
        print("=" * 80)
        print("🚀 開始匯入 Fashion Dataset")
        print("=" * 80)
        
        try:
            # 1. 匯入查找表
            self.import_lookup_tables()
            
            # 2. 讀取 CSV
            print("\n" + "=" * 80)
            print("📖 讀取 CSV 檔案...")
            df = pd.read_csv(self.csv_path, on_bad_lines='skip', encoding='utf-8')
            self.stats["total_rows"] = len(df)
            print(f"✅ 讀取 {len(df)} 筆資料")
            
            # 3. 批次匯入商品
            self.import_products(df)
            
            # 4. 顯示統計
            self.print_statistics()
            
            print("\n" + "=" * 80)
            print("🎉 資料匯入完成！")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n❌ 匯入失敗: {e}")
            self.db.rollback()
            raise
        finally:
            self.db.close()
    
    def import_lookup_tables(self):
        """匯入所有查找表"""
        print("\n" + "=" * 80)
        print("📊 匯入查找表...")
        print("=" * 80)
        
        # 讀取 CSV 以取得所有唯一值 (處理格式錯誤)
        df = pd.read_csv(self.csv_path, on_bad_lines='skip', encoding='utf-8')
        
        # 1. Genders
        self._import_genders(df)
        
        # 2. Categories
        self._import_master_categories(df)
        
        # 3. Sub Categories
        self._import_sub_categories(df)
        
        # 4. Article Types
        self._import_article_types(df)
        
        # 5. Colours
        self._import_colours(df)
        
        # 6. Seasons
        self._import_seasons(df)
        
        # 7. Usages
        self._import_usages(df)
        
        # 8. Brands
        self._import_brands(df)
        
        print("\n✅ 所有查找表匯入完成")
    
    def _import_master_categories(self, df: pd.DataFrame):
        """
        匯入主分類
        """
        print("\n📝 匯入主分類 (MasterCategories)...")

        unique_master_categories = df['masterCategory'].dropna().unique()
        created = 0

        for cat_name in unique_master_categories:
            existing = self.db.query(MasterCategory).filter_by(name=cat_name).first()
            if not existing:
                master_category = MasterCategory(
                    name=cat_name,
                    display_name=self._translate_category(cat_name)
                )
                self.db.add(master_category)
                created += 1

        self.db.commit()

        # 建立快取
        for cat in self.db.query(MasterCategory).all():
            self.master_category_cache[cat.name] = cat.id

        total = len(self.master_category_cache)
        print(f"✅ 主分類: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["master_categories"] = total
    
    def _import_sub_categories(self, df: pd.DataFrame):
        """匯入子分類"""
        print("\n📝 匯入子分類 (Sub Categories)...")
        
        # 需要同時考慮 category 和 subCategory 的組合
        unique_pairs = df[['masterCategory', 'subCategory']].dropna().drop_duplicates()
        created = 0
        
        for _, row in unique_pairs.iterrows():
            master_cat_name = row['masterCategory']
            sub_cat_name = row['subCategory']

            if master_cat_name not in self.master_category_cache:
                continue

            existing = self.db.query(SubCategory).filter_by(name=sub_cat_name).first()
            if not existing:
                sub_cat = SubCategory(
                    master_category_id=self.master_category_cache[master_cat_name],
                    name=sub_cat_name,
                    display_name=self._translate_sub_category(sub_cat_name)
                )
                self.db.add(sub_cat)
                created += 1
        
        self.db.commit()
        
        # 建立快取
        for sub_cat in self.db.query(SubCategory).all():
            self.sub_category_cache[sub_cat.name] = sub_cat.id
        
        total = len(self.sub_category_cache)
        print(f"✅ 子分類: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["sub_categories"] = total
    
    def _import_article_types(self, df: pd.DataFrame):
        """匯入商品類型"""
        print("\n📝 匯入商品類型 (Article Types)...")
        
        unique_types = df['articleType'].dropna().unique()
        created = 0
        
        for type_name in unique_types:
            existing = self.db.query(ArticleType).filter_by(name=type_name).first()
            if not existing:
                article_type = ArticleType(
                    name=type_name,
                    display_name=type_name  # 保持原名
                )
                self.db.add(article_type)
                created += 1
        
        self.db.commit()
        
        # 建立快取
        for at in self.db.query(ArticleType).all():
            self.article_type_cache[at.name] = at.id
        
        total = len(self.article_type_cache)
        print(f"✅ 商品類型: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["article_types"] = total
    
    def _import_colours(self, df: pd.DataFrame):
        """匯入顏色"""
        print("\n📝 匯入顏色 (Colours)...")
        
        unique_colours = df['baseColour'].dropna().unique()
        created = 0
        
        for colour_name in unique_colours:
            # 標準化顏色名稱 (處理大小寫、空格)
            colour_name_clean = colour_name.strip()
            
            existing = self.db.query(Colour).filter_by(name=colour_name_clean).first()
            if not existing:
                colour = Colour(
                    name=colour_name_clean,
                    display_name=self._translate_colour(colour_name_clean),
                    hex_code=self._get_colour_hex(colour_name_clean)
                )
                self.db.add(colour)
                created += 1
        
        self.db.commit()
        
        # 建立快取
        for colour in self.db.query(Colour).all():
            self.colour_cache[colour.name] = colour.id
        
        total = len(self.colour_cache)
        print(f"✅ 顏色: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["colours"] = total
    
    def _import_seasons(self, df: pd.DataFrame):
        """匯入季節"""
        print("\n📝 匯入季節 (Seasons)...")
        
        unique_seasons = df['season'].dropna().unique()
        created = 0
        
        for season_name in unique_seasons:
            existing = self.db.query(Season).filter_by(name=season_name).first()
            if not existing:
                season = Season(
                    name=season_name,
                    display_name=self._translate_season(season_name)
                )
                self.db.add(season)
                created += 1
        
        self.db.commit()
        
        # 建立快取
        for season in self.db.query(Season).all():
            self.season_cache[season.name] = season.id
        
        total = len(self.season_cache)
        print(f"✅ 季節: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["seasons"] = total
    
    def _import_usages(self, df: pd.DataFrame):
        """匯入使用場合"""
        print("\n📝 匯入使用場合 (Usages)...")
        
        unique_usages = df['usage'].dropna().unique()
        created = 0
        
        for usage_name in unique_usages:
            existing = self.db.query(Usage).filter_by(name=usage_name).first()
            if not existing:
                usage = Usage(
                    name=usage_name,
                    display_name=self._translate_usage(usage_name)
                )
                self.db.add(usage)
                created += 1
        
        self.db.commit()
        
        # 建立快取
        for usage in self.db.query(Usage).all():
            self.usage_cache[usage.name] = usage.id
        
        total = len(self.usage_cache)
        print(f"✅ 使用場合: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["usages"] = total
    
    def _import_brands(self, df: pd.DataFrame):
        """匯入品牌 (從 JSON 讀取)"""
        print("\n📝 匯入品牌 (Brands)...")
        
        brands_set: Set[str] = set()
        
        # 從 JSON 檔案讀取品牌
        json_files = list(self.json_dir.glob("*.json"))
        for json_file in json_files[:1000]:  # 先讀取 1000 個檔案以建立品牌列表
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'data' in data and 'brandName' in data['data']:
                        brand_name = data['data']['brandName']
                        if brand_name and brand_name.strip():
                            brands_set.add(brand_name.strip())
            except Exception:
                continue
        
        created = 0
        for brand_name in brands_set:
            existing = self.db.query(Brand).filter_by(name=brand_name).first()
            if not existing:
                brand = Brand(
                    name=brand_name,
                    display_name=brand_name,
                    is_active=True
                )
                self.db.add(brand)
                created += 1
        
        self.db.commit()
        
        # 建立快取
        for brand in self.db.query(Brand).all():
            self.brand_cache[brand.name] = brand.id
        
        total = len(self.brand_cache)
        print(f"✅ 品牌: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["brands"] = total
    
    def import_products(self, df: pd.DataFrame):
        """批次匯入商品"""
        print("\n" + "=" * 80)
        print("📦 匯入商品資料...")
        print("=" * 80)
        
        batch_size = 100
        total_rows = len(df)
        
        for batch_start in range(0, total_rows, batch_size):
            batch_end = min(batch_start + batch_size, total_rows)
            batch_df = df.iloc[batch_start:batch_end]
            
            for idx, row in batch_df.iterrows():
                try:
                    self._import_single_product(row)
                    self.stats["successful_imports"] += 1
                except Exception as e:
                    self.stats["failed_imports"] += 1
                    self.stats["errors"].append({
                        "row": idx,
                        "product_id": row.get('id'),
                        "error": str(e)
                    })
                    # Rollback 當前錯誤，繼續處理下一筆
                    self.db.rollback()
            
            # 批次提交
            try:
                self.db.commit()
            except Exception as e:
                print(f"⚠️ 批次提交失敗: {e}")
                self.db.rollback()
            
            # 進度顯示
            progress = (batch_end / total_rows) * 100
            print(f"進度: {batch_end}/{total_rows} ({progress:.1f}%) - "
                  f"成功: {self.stats['successful_imports']}, "
                  f"失敗: {self.stats['failed_imports']}")
        
        print(f"\n✅ 商品匯入完成: {self.stats['successful_imports']} 筆成功")
    
    def _import_single_product(self, row: pd.Series):
        """匯入單一商品"""
        product_id = int(row['id'])
        
        # 檢查是否已存在
        existing = self.db.query(Product).filter_by(id=product_id).first()
        if existing:
            self.stats["skipped_rows"] += 1
            return
        
        # 檢查必要欄位
        product_name = row.get('productDisplayName')
        if pd.isna(product_name) or not str(product_name).strip():
            # 跳過沒有商品名稱的資料
            self.stats["skipped_rows"] += 1
            return
        
        # 讀取 JSON 資料
        json_data = self._read_product_json(product_id)
        
        # 建立商品
        product = Product(
            id=product_id,
            product_display_name=str(product_name).strip(),
            gender_id=self._get_gender_id(row.get('gender')),
            master_category_id=self._get_master_category_id(row.get('masterCategory')),
            sub_category_id=self._get_sub_category_id(row.get('subCategory')),
            article_type_id=self._get_article_type_id(row.get('articleType')),
            base_colour_id=self._get_colour_id(row.get('baseColour')),
            season_id=self._get_season_id(row.get('season')),
            usage_id=self._get_usage_id(row.get('usage')),
            year=self._parse_year(row.get('year')),
            brand_id=self._get_brand_id_from_json(json_data),
            price=self._parse_price(json_data),
            description=self._get_description(json_data),
            is_active=True,
            stock_count=100  # 預設庫存
        )
        
        self.db.add(product)
        self.db.flush()  # 取得 product.id
        
        # 匯入圖片
        self._import_product_images(product, json_data)
        
        # 匯入屬性
        self._import_product_attributes(product, json_data)
    
    def _import_product_images(self, product: Product, json_data: Optional[Dict]):
        """匯入商品圖片"""
        if not json_data or 'data' not in json_data:
            return
        
        data = json_data['data']
        display_order = 0
        
        # 主圖
        if 'styleImages' in data:
            style_images = data['styleImages']
            
            # Default (正面圖)
            if 'default' in style_images:
                image_url = style_images['default'].get('imageURL', '')
                if image_url:
                    product_image = ProductImage(
                        product_id=product.id,
                        image_type='front',
                        image_url=image_url,
                        is_primary=True,
                        display_order=display_order
                    )
                    self.db.add(product_image)
                    display_order += 1
                    product.has_front_image = True
            
            # Back
            if 'back' in style_images:
                image_url = style_images['back'].get('imageURL', '')
                if image_url:
                    product_image = ProductImage(
                        product_id=product.id,
                        image_type='back',
                        image_url=image_url,
                        is_primary=False,
                        display_order=display_order
                    )
                    self.db.add(product_image)
                    display_order += 1
                    product.has_back_image = True
            
            # Search
            if 'search' in style_images:
                image_url = style_images['search'].get('imageURL', '')
                if image_url:
                    product_image = ProductImage(
                        product_id=product.id,
                        image_type='search',
                        image_url=image_url,
                        is_primary=False,
                        display_order=display_order
                    )
                    self.db.add(product_image)
                    product.has_search_image = True
    
    def _import_product_attributes(self, product: Product, json_data: Optional[Dict]):
        """匯入商品屬性"""
        if not json_data or 'data' not in json_data:
            return
        
        data = json_data['data']
        
        # 從 JSON 提取各種屬性
        attributes = {}
        
        if 'productDescriptors' in data:
            descriptors = data['productDescriptors'].get('description', {})
            for key, value in descriptors.items():
                if value:
                    attributes[key] = str(value)
        
        # 儲存屬性
        for key, value in attributes.items():
            product_attr = ProductAttribute(
                product_id=product.id,
                attribute_key=key,
                attribute_value=value
            )
            self.db.add(product_attr)

    def _import_genders(self, df: pd.DataFrame):
        """匯入性別查找表"""
        print("\n📝 匯入性別 (Genders)...")
        unique_genders = df['gender'].dropna().unique()
        created = 0
        for gender_name in unique_genders:
            existing = self.db.query(Gender).filter_by(name=gender_name).first()
            if not existing:
                gender = Gender(
                    name=gender_name,
                    display_name=self._translate_gender(gender_name)
                )
                self.db.add(gender)
                created += 1
        self.db.commit()
        # 建立快取
        for gender in self.db.query(Gender).all():
            self.gender_cache[gender.name] = gender.id
        total = len(self.gender_cache)
        print(f"✅ 性別: {total} 個 (新增 {created} 個)")
        self.stats["lookup_tables"]["genders"] = total

    def _read_product_json(self, product_id: int) -> Optional[Dict]:
        """讀取商品 JSON 檔案"""
        json_file = self.json_dir / f"{product_id}.json"
        if not json_file.exists():
            return None
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    # ===== 輔助方法 =====
    
    def _get_gender_id(self, gender_name) -> Optional[int]:
        if pd.isna(gender_name):
            return None
        return self.gender_cache.get(gender_name)
    
    def _get_master_category_id(self, master_category_name) -> Optional[int]:
        if pd.isna(master_category_name):
            return None
        return self.master_category_cache.get(master_category_name)
    
    def _get_sub_category_id(self, sub_category_name) -> Optional[int]:
        if pd.isna(sub_category_name):
            return None
        return self.sub_category_cache.get(sub_category_name)
    
    def _get_article_type_id(self, article_type_name) -> Optional[int]:
        if pd.isna(article_type_name):
            return None
        return self.article_type_cache.get(article_type_name)
    
    def _get_colour_id(self, colour_name) -> Optional[int]:
        if pd.isna(colour_name):
            return None
        colour_name_clean = str(colour_name).strip()
        return self.colour_cache.get(colour_name_clean)
    
    def _get_season_id(self, season_name) -> Optional[int]:
        if pd.isna(season_name):
            return None
        return self.season_cache.get(season_name)
    
    def _get_usage_id(self, usage_name) -> Optional[int]:
        if pd.isna(usage_name):
            return None
        return self.usage_cache.get(usage_name)
    
    def _get_brand_id_from_json(self, json_data: Optional[Dict]) -> Optional[int]:
        if not json_data or 'data' not in json_data:
            return None
        
        brand_name = json_data['data'].get('brandName')
        if not brand_name:
            return None
        
        return self.brand_cache.get(brand_name.strip())
    
    def _parse_year(self, year_value) -> Optional[int]:
        if pd.isna(year_value):
            return None
        try:
            return int(year_value)
        except (ValueError, TypeError):
            return None
    
    def _parse_price(self, json_data: Optional[Dict]) -> float:
        """從 JSON 解析價格"""
        if not json_data or 'data' not in json_data:
            return 0.0
        
        price_str = json_data['data'].get('price', '0')
        if not price_str:
            return 0.0
        
        # 移除貨幣符號和逗號
        price_str = str(price_str).replace('₹', '').replace(',', '').strip()
        
        try:
            return float(price_str)
        except (ValueError, TypeError):
            return 0.0
    
    def _get_description(self, json_data: Optional[Dict]) -> Optional[str]:
        """從 JSON 取得商品描述"""
        if not json_data or 'data' not in json_data:
            return None
        
        return json_data['data'].get('productDisplayName')
    
    # ===== 翻譯方法 =====
    
    def _translate_gender(self, name: str) -> str:
        translations = {
            'Men': '男性',
            'Women': '女性',
            'Boys': '男童',
            'Girls': '女童',
            'Unisex': '中性'
        }
        return translations.get(name, name)
    
    def _translate_category(self, name: str) -> str:
        translations = {
            'Apparel': '服飾',
            'Accessories': '配件',
            'Footwear': '鞋類',
            'Personal Care': '個人護理',
            'Free Items': '免費商品',
            'Sporting Goods': '運動用品',
            'Home': '居家用品'
        }
        return translations.get(name, name)
    
    def _translate_sub_category(self, name: str) -> str:
        translations = {
            'Topwear': '上衣',
            'Bottomwear': '下著',
            'Shoes': '鞋子',
            'Watches': '手錶',
            'Socks': '襪子',
            'Bags': '包包',
            'Belts': '皮帶',
            'Flip Flops': '拖鞋',
            'Innerwear': '內衣',
            'Sandal': '涼鞋',
            'Shoe Accessories': '鞋類配件',
            'Fragrance': '香水',
            'Jewellery': '珠寶',
            'Eyewear': '眼鏡',
            'Dress': '洋裝',
            'Loungewear and Nightwear': '居家睡衣',
            'Wallets': '錢包',
            'Apparel Set': '套裝',
            'Headwear': '帽子',
            'Mufflers': '圍巾',
            'Skin Care': '護膚品',
            'Makeup': '化妝品',
            'Free Gifts': '贈品',
            'Ties': '領帶',
            'Skin': '皮膚保養',
            'Beauty Accessories': '美妝配件',
            'Water Bottle': '水壺',
            'Sports Accessories': '運動配件',
            'Stoles': '披肩',
            'Scarves': '圍巾',
            'Sports Equipment': '運動器材',
            'Cufflinks': '袖扣',
            'Hair Accessory': '髮飾',
            'Gloves': '手套',
            'Umbrellas': '雨傘',
            'Vouchers': '禮券',
            'Lips': '唇部保養',
            'Saree': '紗麗',
            'Perfumes': '香水'
        }
        return translations.get(name, name)
    
    def _translate_colour(self, name: str) -> str:
        translations = {
            'Black': '黑色',
            'White': '白色',
            'Blue': '藍色',
            'Red': '紅色',
            'Grey': '灰色',
            'Navy Blue': '海軍藍',
            'Green': '綠色',
            'Purple': '紫色',
            'Pink': '粉紅色',
            'Yellow': '黃色',
            'Orange': '橙色',
            'Brown': '棕色',
            'Beige': '米色',
            'Olive': '橄欖綠',
            'Maroon': '栗色',
            'Silver': '銀色',
            'Gold': '金色',
            'Cream': '奶油色',
            'Tan': '褐色',
            'Khaki': '卡其色',
            'Turquoise Blue': '土耳其藍',
            'Charcoal': '炭灰色',
            'Coffee Brown': '咖啡棕',
            'Mushroom Brown': '蘑菇棕',
            'Burgundy': '勃根地紅',
            'Lavender': '薰衣草紫',
            'Mint': '薄荷綠',
            'Peach': '桃色',
            'Coral': '珊瑚色',
            'Rust': '鐵鏽色',
            'Teal': '水鴨色',
            'Multi': '多色',
            'Metallic': '金屬色',
            'Fluorescent Green': '螢光綠'
        }
        return translations.get(name, name)
    
    def _translate_season(self, name: str) -> str:
        translations = {
            'Summer': '夏季',
            'Winter': '冬季',
            'Spring': '春季',
            'Fall': '秋季'
        }
        return translations.get(name, name)
    
    def _translate_usage(self, name: str) -> str:
        translations = {
            'Casual': '休閒',
            'Formal': '正式',
            'Sports': '運動',
            'Ethnic': '民族風',
            'Party': '派對',
            'Smart Casual': '智能休閒',
            'Travel': '旅行',
            'Home': '居家'
        }
        return translations.get(name, name)
    
    def _get_colour_hex(self, name: str) -> Optional[str]:
        """取得顏色的 HEX 代碼"""
        colour_hex = {
            'Black': '#000000',
            'White': '#FFFFFF',
            'Blue': '#0000FF',
            'Red': '#FF0000',
            'Grey': '#808080',
            'Navy Blue': '#000080',
            'Green': '#008000',
            'Purple': '#800080',
            'Pink': '#FFC0CB',
            'Yellow': '#FFFF00',
            'Orange': '#FFA500',
            'Brown': '#A52A2A',
            'Beige': '#F5F5DC',
            'Olive': '#808000',
            'Maroon': '#800000',
            'Silver': '#C0C0C0',
            'Gold': '#FFD700',
            'Cream': '#FFFDD0',
            'Tan': '#D2B48C',
            'Khaki': '#F0E68C',
            'Turquoise Blue': '#40E0D0',
            'Charcoal': '#36454F',
            'Coffee Brown': '#6F4E37',
            'Burgundy': '#800020',
            'Lavender': '#E6E6FA',
            'Mint': '#98FF98',
            'Peach': '#FFE5B4',
            'Coral': '#FF7F50',
            'Teal': '#008080'
        }
        return colour_hex.get(name)
    
    def print_statistics(self):
        """顯示匯入統計"""
        print("\n" + "=" * 80)
        print("📊 匯入統計")
        print("=" * 80)
        
        print(f"\n查找表:")
        for table_name, count in self.stats["lookup_tables"].items():
            print(f"  - {table_name}: {count} 筆")
        
        print(f"\n商品:")
        print(f"  - 總筆數: {self.stats['total_rows']}")
        print(f"  - 成功匯入: {self.stats['successful_imports']}")
        print(f"  - 失敗: {self.stats['failed_imports']}")
        print(f"  - 跳過 (已存在): {self.stats['skipped_rows']}")
        
        if self.stats["errors"]:
            print(f"\n❌ 錯誤記錄 (前 10 筆):")
            for error in self.stats["errors"][:10]:
                print(f"  - 行 {error['row']} (ID: {error['product_id']}): {error['error']}")


def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(description='匯入 Fashion Dataset')
    parser.add_argument('--dataset-path', default='../fashion-dataset',
                        help='Dataset 路徑')
    
    args = parser.parse_args()
    
    importer = FashionDataImporter(args.dataset_path)
    importer.import_all()


if __name__ == "__main__":
    main()
