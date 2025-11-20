"""
測試 SQLAlchemy Models 的 CRUD 操作
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models import (
    Gender, MasterCategory, SubCategory, ArticleType,
    Colour, Season, Usage, Brand, Product
)


def test_create_lookup_data():
    """測試建立查找表資料"""
    print("=" * 80)
    print("🧪 測試 1: 建立查找表資料")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 1. 建立性別資料
        print("\n📝 建立性別資料...")
        genders_data = [
            {"name": "Men", "display_name": "男性"},
            {"name": "Women", "display_name": "女性"},
            {"name": "Boys", "display_name": "男童"},
            {"name": "Girls", "display_name": "女童"},
            {"name": "Unisex", "display_name": "中性"},
        ]
        
        created_count = 0
        for data in genders_data:
            existing = db.query(Gender).filter_by(name=data["name"]).first()
            if not existing:
                gender = Gender(**data)
                db.add(gender)
                created_count += 1
        
        db.commit()
        print(f"✅ 成功建立 {created_count} 個性別分類 (共 {len(genders_data)} 個)")
        
        # 2. 建立主分類
        print("\n📝 建立主分類...")
        master_categories_data = [
            {"name": "Apparel", "display_name": "服飾"},
            {"name": "Accessories", "display_name": "配件"},
            {"name": "Footwear", "display_name": "鞋類"},
        ]

        created_count = 0
        for data in master_categories_data:
            existing = db.query(MasterCategory).filter_by(name=data["name"]).first()
            if not existing:
                master_category = MasterCategory(**data)
                db.add(master_category)
                created_count += 1

        db.commit()
        print(f"✅ 成功建立 {created_count} 個主分類 (共 {len(master_categories_data)} 個)")

        # 3. 建立子分類
        print("\n📝 建立子分類...")
        apparel_cat = db.query(MasterCategory).filter_by(name="Apparel").first()

        sub_categories_data = [
            {"master_category_id": apparel_cat.id, "name": "Topwear", "display_name": "上衣"},
            {"master_category_id": apparel_cat.id, "name": "Bottomwear", "display_name": "下著"},
        ]
        
        created_count = 0
        for data in sub_categories_data:
            existing = db.query(SubCategory).filter_by(name=data["name"]).first()
            if not existing:
                sub_cat = SubCategory(**data)
                db.add(sub_cat)
                created_count += 1
        
        db.commit()
        print(f"✅ 成功建立 {created_count} 個子分類 (共 {len(sub_categories_data)} 個)")
        
        # 4. 建立顏色
        print("\n📝 建立顏色...")
        colours_data = [
            {"name": "Black", "display_name": "黑色", "hex_code": "#000000"},
            {"name": "White", "display_name": "白色", "hex_code": "#FFFFFF"},
            {"name": "Blue", "display_name": "藍色", "hex_code": "#0000FF"},
        ]
        
        created_count = 0
        for data in colours_data:
            existing = db.query(Colour).filter_by(name=data["name"]).first()
            if not existing:
                colour = Colour(**data)
                db.add(colour)
                created_count += 1
        
        db.commit()
        print(f"✅ 成功建立 {created_count} 個顏色 (共 {len(colours_data)} 個)")
        
        # 5. 建立季節
        print("\n📝 建立季節...")
        seasons_data = [
            {"name": "Summer", "display_name": "夏季"},
            {"name": "Winter", "display_name": "冬季"},
        ]
        
        created_count = 0
        for data in seasons_data:
            existing = db.query(Season).filter_by(name=data["name"]).first()
            if not existing:
                season = Season(**data)
                db.add(season)
                created_count += 1
        
        db.commit()
        print(f"✅ 成功建立 {created_count} 個季節 (共 {len(seasons_data)} 個)")
        
        # 6. 建立使用場合
        print("\n📝 建立使用場合...")
        usages_data = [
            {"name": "Casual", "display_name": "休閒"},
            {"name": "Formal", "display_name": "正式"},
        ]
        
        created_count = 0
        for data in usages_data:
            existing = db.query(Usage).filter_by(name=data["name"]).first()
            if not existing:
                usage = Usage(**data)
                db.add(usage)
                created_count += 1
        
        db.commit()
        print(f"✅ 成功建立 {created_count} 個使用場合 (共 {len(usages_data)} 個)")
        
        # 7. 建立品牌
        print("\n📝 建立品牌...")
        brands_data = [
            {"name": "Nike", "display_name": "Nike"},
            {"name": "Adidas", "display_name": "Adidas"},
        ]
        
        created_count = 0
        for data in brands_data:
            existing = db.query(Brand).filter_by(name=data["name"]).first()
            if not existing:
                brand = Brand(**data)
                db.add(brand)
                created_count += 1
        
        db.commit()
        print(f"✅ 成功建立 {created_count} 個品牌 (共 {len(brands_data)} 個)")
        
        print("\n" + "=" * 80)
        print("✅ 所有查找表資料建立成功！")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def test_read_lookup_data():
    """測試讀取查找表資料"""
    print("\n" + "=" * 80)
    print("🧪 測試 2: 讀取查找表資料")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 讀取所有性別
        print("\n📖 讀取性別資料:")
        genders = db.query(Gender).all()
        for gender in genders:
            print(f"  - {gender.name} ({gender.display_name})")
        
        # 讀取所有主分類
        print("\n📖 讀取主分類:")
        master_categories = db.query(MasterCategory).all()
        for cat in master_categories:
            print(f"  - {cat.name} ({cat.display_name})")
        
        # 讀取所有顏色
        print("\n📖 讀取顏色:")
        colours = db.query(Colour).all()
        for colour in colours:
            print(f"  - {colour.name} ({colour.display_name}) {colour.hex_code}")
        
        print("\n✅ 讀取成功！")
        
    finally:
        db.close()


def test_create_product():
    """測試建立商品"""
    print("\n" + "=" * 80)
    print("🧪 測試 3: 建立商品資料")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 取得關聯資料的 ID
        gender = db.query(Gender).filter_by(name="Men").first()
        master_category = db.query(MasterCategory).filter_by(name="Apparel").first()
        sub_cat = db.query(SubCategory).filter_by(name="Topwear").first()
        colour = db.query(Colour).filter_by(name="Black").first()
        season = db.query(Season).filter_by(name="Summer").first()
        usage = db.query(Usage).filter_by(name="Casual").first()
        brand = db.query(Brand).filter_by(name="Nike").first()
        
        # 建立測試商品
        print("\n📝 建立測試商品...")
        product = Product(
            id=99999,  # 測試用 ID
            product_display_name="Nike Men Black Casual T-Shirt",
            gender_id=gender.id if gender else None,
            master_category_id=master_category.id if master_category else None,
            sub_category_id=sub_cat.id if sub_cat else None,
            base_colour_id=colour.id if colour else None,
            season_id=season.id if season else None,
            usage_id=usage.id if usage else None,
            brand_id=brand.id if brand else None,
            price=1299.00,
            discounted_price=999.00,
            discount_percent=23,
            description="高品質棉質 T-Shirt，適合日常休閒穿著",
            is_active=True,
            stock_count=100,
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        print(f"✅ 成功建立商品: ID={product.id}, 名稱={product.product_display_name}")
        print(f"   價格: ${product.price} → ${product.discounted_price} (折扣 {product.discount_percent}%)")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def test_read_product_with_relations():
    """測試讀取商品及其關聯資料"""
    print("\n" + "=" * 80)
    print("🧪 測試 4: 讀取商品及關聯資料")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 讀取剛才建立的商品
        product = db.query(Product).filter_by(id=99999).first()
        
        if product:
            print(f"\n📦 商品資訊:")
            print(f"  ID: {product.id}")
            print(f"  名稱: {product.product_display_name}")
            print(f"  價格: ${product.price}")
            print(f"  折扣價: ${product.discounted_price}")
            
            # 透過關聯讀取相關資料
            print(f"\n🔗 關聯資料:")
            if product.gender:
                print(f"  性別: {product.gender.name} ({product.gender.display_name})")
            if product.master_category:
                print(f"  主分類: {product.master_category.name} ({product.master_category.display_name})")
            if product.sub_category:
                print(f"  子分類: {product.sub_category.name} ({product.sub_category.display_name})")
            if product.base_colour:
                print(f"  顏色: {product.base_colour.name} ({product.base_colour.display_name})")
            if product.season:
                print(f"  季節: {product.season.name} ({product.season.display_name})")
            if product.usage:
                print(f"  使用場合: {product.usage.name} ({product.usage.display_name})")
            if product.brand:
                print(f"  品牌: {product.brand.name}")
            
            print("\n✅ 關聯查詢成功！")
        else:
            print("❌ 找不到商品")
            
    finally:
        db.close()


def test_update_product():
    """測試更新商品"""
    print("\n" + "=" * 80)
    print("🧪 測試 5: 更新商品資料")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        product = db.query(Product).filter_by(id=99999).first()
        
        if product:
            print(f"\n📝 原始價格: ${product.price}")
            
            # 更新價格
            product.price = 1499.00
            product.discounted_price = 1199.00
            product.stock_count = 150
            
            db.commit()
            db.refresh(product)
            
            print(f"✅ 更新後價格: ${product.price}")
            print(f"   庫存: {product.stock_count}")
        else:
            print("❌ 找不到商品")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def test_query_with_filter():
    """測試查詢與篩選"""
    print("\n" + "=" * 80)
    print("🧪 測試 6: 查詢與篩選")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 查詢所有上架的商品
        print("\n🔍 查詢所有上架商品:")
        active_products = db.query(Product).filter(Product.is_active == True).all()
        print(f"  找到 {len(active_products)} 件上架商品")
        
        # 查詢價格在 1000-1500 之間的商品
        print("\n🔍 查詢價格 $1000-$1500 的商品:")
        price_range_products = db.query(Product).filter(
            Product.price >= 1000,
            Product.price <= 1500
        ).all()
        print(f"  找到 {len(price_range_products)} 件商品")
        
        for p in price_range_products:
            print(f"    - {p.product_display_name}: ${p.price}")
        
        print("\n✅ 查詢成功！")
        
    finally:
        db.close()


def test_delete_test_data():
    """測試刪除測試資料"""
    print("\n" + "=" * 80)
    print("🧪 測試 7: 刪除測試資料")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 刪除測試商品
        product = db.query(Product).filter_by(id=99999).first()
        if product:
            db.delete(product)
            db.commit()
            print("✅ 成功刪除測試商品")
        
        # 確認已刪除
        check = db.query(Product).filter_by(id=99999).first()
        if check is None:
            print("✅ 確認商品已刪除")
        else:
            print("❌ 商品仍然存在")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """執行所有測試"""
    print("\n" + "🚀" * 40)
    print("SQLAlchemy Models CRUD 測試")
    print("🚀" * 40 + "\n")
    
    try:
        # 執行測試
        test_create_lookup_data()
        test_read_lookup_data()
        test_create_product()
        test_read_product_with_relations()
        test_update_product()
        test_query_with_filter()
        test_delete_test_data()
        
        print("\n" + "=" * 80)
        print("🎉 所有測試通過！SQLAlchemy Models 運作正常")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ 測試失敗: {e}")
        print("=" * 80 + "\n")
        raise


if __name__ == "__main__":
    main()
