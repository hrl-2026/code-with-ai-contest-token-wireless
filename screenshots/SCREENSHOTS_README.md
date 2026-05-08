# Screenshots

> 由于当前是服务器环境（无浏览器），地图以 HTML 文件形式提供。  
> 在本地 `streamlit run app.py` 后可在浏览器中直接查看真实地图截图。

---

## Screenshot 1: 2D 信号地图 (交互式 HTML)

**文件：** `map_2d.html`
**描述：** Folium 2D 地图，基于 OpenStreetMap 真实地图瓦片。
- 数据点按 RSRP 信号强度着色（绿/黄/红）
- 点大小半径 3px，半透明（散落效果）
- 点击弹窗显示详细信号参数
- 支持图层切换（OpenStreetMap / CartoDB）

**预览方式：** 直接在浏览器打开 `screenshots/map_2d.html`  
或在终端运行 `streamlit run app.py` 后查看 Tab 1。

---

## Screenshot 2: 3D 信号地图 (交互式 HTML)

**文件：** `map_3d.html`
**描述：** PyDeck 3D 柱状地图 (deck.gl)。
- 柱子高度 = Download_Mbps（下载速率）
- 柱子颜色 = RSRP 信号强度
- 支持鼠标拖拽旋转和滚轮缩放

**预览方式：** 直接在浏览器打开 `screenshots/map_3d.html`  
或在终端运行 `streamlit run app.py` 后查看 Tab 2。

---

## Screenshot 3: 数据图表 (PNG + HTML)

**文件：** `charts.png`（静态 PNG） / `charts_combined.html`（交互式 HTML）  
**描述：** Plotly 交互式图表。

### 频段基站数量柱状图
- X 轴：5G 频段 (n28, n41, n78)
- Y 轴：基站数量
- 不同频段使用不同颜色

### 终端类型分布饼图
- Smartphone（智能手机）
- CPE（客户终端设备）
- IoT（物联网设备）

---

## 快速查看方式

```bash
# 方法一：直接运行看板（推荐）
cd code-with-ai-contest-token-wireless
source venv/bin/activate
streamlit run app.py

# 方法二：浏览器打开 HTML 文件
# 直接在文件管理器中双击打开 screenshots/ 下的 .html 文件
```
