"""
驗證資料匯入結果
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models import (
    Gender, MasterCategory, SubCategory, ArticleType,
    Colour, Season, Usage, Brand, Product, ProductImage,
    ProductAttribute
)


def verify_import():
    """驗證資料匯入結果"""
    print("=" * 80)
    print("🔍 驗證資料匯入結果")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 查找表統計
        print("\n📊 查找表統計:")
        print(f"  性別 (Genders): {db.query(Gender).count()} 筆")
        print(f"  主分類 (MasterCategories): {db.query(MasterCategory).count()} 筆")
        print(f"  子分類 (Sub Categories): {db.query(SubCategory).count()} 筆")
        print(f"  商品類型 (Article Types): {db.query(ArticleType).count()} 筆")
        print(f"  顏色 (Colours): {db.query(Colour).count()} 筆")
        print(f"  季節 (Seasons): {db.query(Season).count()} 筆")
        print(f"  使用場合 (Usages): {db.query(Usage).count()} 筆")
        print(f"  品牌 (Brands): {db.query(Brand).count()} 筆")
        
        # 商品統計
        print("\n📦 商品統計:")
        total_products = db.query(Product).count()
        print(f"  總商品數: {total_products:,} 筆")
        
        active_products = db.query(Product).filter(Product.is_active == True).count()
        print(f"  上架商品: {active_products:,} 筆")
        
        products_with_price = db.query(Product).filter(Product.price > 0).count()
        print(f"  有價格的商品: {products_with_price:,} 筆")
        
        # 圖片統計
        print("\n🖼️  圖片統計:")
        total_images = db.query(ProductImage).count()
        print(f"  總圖片數: {total_images:,} 筆")
        
        products_with_front = db.query(Product).filter(Product.has_front_image == True).count()
        products_with_back = db.query(Product).filter(Product.has_back_image == True).count()
        products_with_search = db.query(Product).filter(Product.has_search_image == True).count()
        
        print(f"  有正面圖的商品: {products_with_front:,} 筆")
        print(f"  有背面圖的商品: {products_with_back:,} 筆")
        print(f"  有搜尋圖的商品: {products_with_search:,} 筆")
        
        # 屬性統計
        print("\n🏷️  屬性統計:")
        total_attributes = db.query(ProductAttribute).count()
        print(f"  總屬性數: {total_attributes:,} 筆")
        
        products_with_attrs = db.query(ProductAttribute.product_id).distinct().count()
        print(f"  有屬性的商品: {products_with_attrs:,} 筆")
        
        # 分類分布
        print("\n📋 性別分布:")
        for gender in db.query(Gender).all():
            count = db.query(Product).filter(Product.gender_id == gender.id).count()
            if count > 0:
                percentage = (count / total_products) * 100
                print(f"  {gender.display_name}: {count:,} 筆 ({percentage:.1f}%)")
        
        print("\n📋 主分類分布:")
        for master_category in db.query(MasterCategory).all():
            count = db.query(Product).filter(Product.master_category_id == master_category.id).count()
            if count > 0:
                percentage = (count / total_products) * 100
                print(f"  {master_category.display_name}: {count:,} 筆 ({percentage:.1f}%)")
        
        # 價格範圍
        print("\n💰 價格統計:")
        min_price = db.query(Product).filter(Product.price > 0).order_by(Product.price).first()
        max_price = db.query(Product).filter(Product.price > 0).order_by(Product.price.desc()).first()
        
        if min_price and max_price:
            print(f"  最低價: ${min_price.price:.2f} - {min_price.product_display_name}")
            print(f"  最高價: ${max_price.price:.2f} - {max_price.product_display_name}")
        
        # 隨機抽樣檢查
        print("\n🎲 隨機商品範例:")
        import random
        sample_ids = random.sample(range(10000, 50000), 3)
        
        for product_id in sample_ids:
            product = db.query(Product).filter_by(id=product_id).first()
            if product:
                print(f"\n  商品 #{product.id}:")
                print(f"    名稱: {product.product_display_name}")
                if product.gender:
                    print(f"    性別: {product.gender.display_name}")
                if product.master_category:
                    print(f"    分類: {product.master_category.display_name}")
                if product.price:
                    print(f"    價格: ${product.price:.2f}")
                
                image_count = db.query(ProductImage).filter_by(product_id=product.id).count()
                attr_count = db.query(ProductAttribute).filter_by(product_id=product.id).count()
                print(f"    圖片: {image_count} 張, 屬性: {attr_count} 個")
        
        print("\n" + "=" * 80)
        print("✅ 驗證完成！")
        print("=" * 80)
        
    finally:
        db.close()


if __name__ == "__main__":
    verify_import()
