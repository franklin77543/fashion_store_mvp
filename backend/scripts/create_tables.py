"""
測試腳本：建立資料庫表並驗證結構
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import Base, engine
from app.models import (
    Gender, MasterCategory, SubCategory, ArticleType,
    Colour, Season, Usage, Brand,
    Product, ProductImage, ProductAttribute, ProductSize,
    Order, OrderItem, ProductReview, ProductEmbedding
)


def create_all_tables():
    """建立所有資料表"""
    print("🚀 開始建立資料庫表...")
    print(f"📁 資料庫位置: {engine.url}")
    print()
    
    try:
        # 建立所有表
        Base.metadata.create_all(bind=engine)
        
        print("✅ 資料庫表建立成功！")
        print()
        print("📊 已建立的資料表:")
        print("-" * 60)
        
        # 列出所有表
        tables = Base.metadata.tables.keys()
        for i, table_name in enumerate(sorted(tables), 1):
            print(f"{i:2d}. {table_name}")
        
        print()
        print(f"📈 總共建立了 {len(tables)} 個資料表")
        print()
        
        # 驗證表結構
        print("🔍 驗證資料表結構...")
        print("-" * 60)
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        # 檢查幾個關鍵表
        key_tables = ['products', 'genders', 'orders', 'product_images']
        for table_name in key_tables:
            if table_name in tables:
                columns = inspector.get_columns(table_name)
                indexes = inspector.get_indexes(table_name)
                foreign_keys = inspector.get_foreign_keys(table_name)
                
                print(f"\n📋 {table_name}:")
                print(f"  - 欄位數: {len(columns)}")
                print(f"  - 索引數: {len(indexes)}")
                print(f"  - 外鍵數: {len(foreign_keys)}")
        
        print()
        print("=" * 60)
        print("✅ 所有驗證完成！資料庫已準備就緒。")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        raise


def drop_all_tables():
    """刪除所有資料表（謹慎使用）"""
    print("⚠️  警告：即將刪除所有資料表...")
    confirm = input("確定要刪除嗎？(yes/no): ")
    
    if confirm.lower() == 'yes':
        Base.metadata.drop_all(bind=engine)
        print("✅ 所有資料表已刪除")
    else:
        print("❌ 取消刪除操作")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='資料庫表管理工具')
    parser.add_argument('--drop', action='store_true', help='刪除所有資料表')
    parser.add_argument('--create', action='store_true', help='建立所有資料表')
    
    args = parser.parse_args()
    
    if args.drop:
        drop_all_tables()
    elif args.create or len(sys.argv) == 1:
        create_all_tables()
    else:
        parser.print_help()
