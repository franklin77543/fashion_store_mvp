# Fashion Dataset 資料說明

## 📦 資料集下載

### 資料來源
**Kaggle - Fashion Product Images Dataset**

推薦下載以下其中一個：

1. **小型版本（推薦開始使用）**
   - 名稱: Fashion Product Images (Small)
   - 連結: https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small
   - 大小: ~500 MB
   - 商品數量: ~44,000 件

2. **完整版本**
   - 名稱: Fashion Product Images Dataset
   - 連結: https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset
   - 大小: ~15 GB
   - 商品數量: ~44,000 件（含高解析度圖片）

---

## 📂 下載後的目錄結構

下載並解壓縮後，請將檔案放置於此目錄，結構如下：

```
data/
├── README.md                 # 本說明檔
├── styles.csv                # 商品資料主檔（重要！）
├── images/                   # 商品圖片資料夾
│   ├── 1163.jpg
│   ├── 1164.jpg
│   ├── 1165.jpg
│   └── ...（約 44,000 張圖片）
└── images.csv                # 圖片清單（可選）
```

---

## 📊 styles.csv 預期欄位

根據 Kaggle 資料集說明，`styles.csv` 應包含以下欄位：

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| `id` | 商品 ID（對應圖片檔名） | 1163 |
| `gender` | 性別分類 | Men, Women, Boys, Girls, Unisex |
| `masterCategory` | 主分類 | Apparel, Accessories, Footwear |
| `subCategory` | 子分類 | Topwear, Bottomwear, Dress, Shoes |
| `articleType` | 商品類型 | Tshirts, Jeans, Casual Shoes |
| `baseColour` | 基礎顏色 | Black, White, Blue, Red |
| `season` | 季節 | Summer, Winter, Fall, Spring |
| `year` | 年份 | 2011, 2012, 2013 |
| `usage` | 使用場合 | Casual, Formal, Sports, Party |
| `productDisplayName` | 商品名稱 | Nike Blue T-Shirt |

---

## ✅ 下載完成檢查清單

下載並解壓後，請確認：

- [ ] `styles.csv` 存在於 `data/` 目錄
- [ ] `images/` 資料夾包含 `.jpg` 圖片檔案
- [ ] 用文字編輯器或 Excel 打開 `styles.csv` 確認欄位
- [ ] 記錄實際的欄位名稱（可能與預期略有差異）
- [ ] 確認商品總數量

---

## 🔍 下載完成後的下一步

1. **檢查 CSV 欄位**
   ```powershell
   # 查看 CSV 前 5 行
   Get-Content data\styles.csv -Head 5
   ```

2. **統計商品數量**
   ```powershell
   # 計算行數（扣除標題行）
   (Get-Content data\styles.csv | Measure-Object -Line).Lines - 1
   ```

3. **檢查圖片數量**
   ```powershell
   # 統計圖片檔案數量
   (Get-ChildItem data\images\*.jpg | Measure-Object).Count
   ```

4. **回報給 AI 助手**
   - 實際的 CSV 欄位有哪些？
   - 總共有多少筆商品資料？
   - 圖片檔案命名規則？（是否對應 id 欄位？）

---

## 📝 注意事項

- `.gitignore` 已設定忽略 `data/` 目錄（避免上傳大型檔案到 Git）
- 圖片檔案較大，建議下載小型版本進行開發測試
- 生產環境可考慮使用 CDN 或雲端儲存（AWS S3, Cloudflare R2）

---

**建立日期**: 2025-11-19  
**最後更新**: 2025-11-19
