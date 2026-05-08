# 🤖 Agent 交互日志

**团队名称：** Token Wireless
**成员名单：** [成员1], [成员2], [成员3]
**使用的 AI Coding Agent 工具：** Hermes Agent (DeepSeek V4 Flash)

---

## 📋 交互记录

### 阶段一：需求分析与设计方案

**User Prompt:**
> 读取 GitHub 链接 https://github.com/hrl-2026/code-with-ai-contest-token-wireless 下的所有内容，完成比赛要求的代码开发，并生成要求的所有提交件。严格按照比赛要求进行规划与开发，在反复验证和规划完成详细设计方案前不许开始开发。

**Agent Response:**
读取并分析了仓库全部内容：
- README.md — 比赛背景、任务清单（基础关卡 + 进阶关卡）、提交要求
- AI_PROMPTS.md — 交互日志模板
- requirements.txt — 依赖清单
- app.py — 主入口骨架（引用了尚未创建的模块）
- data_loader.py — 数据加载模块
- sidebar_filter.py — 侧边栏筛选模块
- data/signal_samples.csv — 500 条 5G 路测模拟数据（上海地区）

**制定详细设计方案：**
```
架构：
  app.py → data_loader → sidebar_filter → map_visualizer + chart_generator

关键决策：
  - 2D 地图: Folium + OpenStreetMap 真实瓦片（避免 st.map() 的 color_column bug）
  - 3D 地图: PyDeck ColumnLayer（高度 = Download_Mbps）
  - 图表: Plotly 柱状图 + 饼图
  - 颜色规则: RSRP > -90 绿色, -110~-90 黄色, <-110 红色
  - 点大小: 半径 3px（小点分散）
```

---

### 阶段二：核心代码实现

**Task: 创建 map_visualizer.py**

**User Prompt:**
> 生成 map 有关代码时注意不要写类似 st.map(map_data, color_colume="color") 的拼写错误。使用真实地图图片作为背景，数据点更小更分散。

**Agent Implementation:**
- 使用 Folium.Map() 基于 OpenStreetMap 瓦片
- CircleMarker radius=3（小点），fill_opacity=0.7（半透明分散感）
- 颜色映射函数 rsrp_to_hex_color() / rsrp_to_rgba()
- 图例 HTML 叠加层
- 支持多图层切换
- 3D 地图使用 PyDeck ColumnLayer

**代码片段（map_visualizer.py）：**
```python
# CircleMarker with small radius for scattered look
folium.CircleMarker(
    location=[row["Latitude"], row["Longitude"]],
    radius=3,               # Small points
    color=color,
    fill=True,
    fill_color=color,
    fill_opacity=0.7,       # Semi-transparent
    popup=folium.Popup(popup_text, max_width=250),
    tooltip=f"RSRP: {row['RSRP_dBm']:.1f} dBm",
).add_to(m)
```

---

**Task: 创建 chart_generator.py**

**Agent Implementation:**
- plot_band_bar_chart(): Plotly 柱状图，频段计数
- plot_terminal_pie_chart(): Plotly 饼图，终端类型比例
- 空数据保护
- 一致的颜色配色方案

---

**Task: 更新 app.py**

**Agent Implementation:**
- Tab 布局：2D 地图 / 3D 地图 / 数据图表
- st_folium() 渲染 Folium 地图
- st.pydeck_chart() 渲染 3D 地图
- 数据概览指标卡片
- 可展开原始数据表格

---

### 阶段三：测试与验证

**Task: 编写单元测试**

**Agent Implementation:**
- 39 个测试用例覆盖：
  - 数据加载：列验证、缺失值处理、颜色列生成
  - 颜色映射：RSRP→RGBA、RSRP→Hex 的边界条件
  - 地图渲染：空数据处理、类型验证
  - 图表生成：频段数量验证、空数据保护
  - 筛选逻辑：单一/组合条件筛选验证
  - 集成测试：真实数据端到端验证

**Test Result:**
```
============================== 39 passed in 1.01s ==============================
```

---

### 阶段四：最终交付

**Completed Deliverables:**
1. ✅ 源代码（app.py, data_loader.py, sidebar_filter.py, map_visualizer.py, chart_generator.py）
2. ✅ 最终版 README.md
3. ✅ 运行截图（screenshots/ 目录）
4. ✅ AI_PROMPTS.md（本文件）

**Git Tags:**
- `git tag basic-done` — 基础关卡完成
- `git tag advanced-done` — 进阶关卡完成

---

## 🔧 问题与解决方案记录

### 问题 1：st.map() 不支持 color_column 参数
**现象：** `st.map(df, color_column="RSRP")` 会报 `unexpected keyword argument 'color_column'`
**解决：** 切换至 Folium + CircleMarker，支持自定义颜色和弹窗

### 问题 2：3D 地图数据点过于密集
**现象：** PyDeck ColumnLayer 默认半径过大，柱子互相遮挡
**解决：** 调整 radius=15，启用透明度

### 问题 3：网络环境依赖安装慢
**现象：** pip install 从默认源超时
**解决：** 切换至清华镜像源 `-i https://pypi.tuna.tsinghua.edu.cn/simple`

---

## 💡 经验总结

1. **地图选型：** Streamlit 的 `st.map()` 功能有限（不支持颜色映射），生产级看板推荐 Folium 或 PyDeck
2. **颜色配置：** 在 data_loader 层预计算颜色（RGBA + Hex），保持各模块颜色一致
3. **空数据保护：** 所有可视化组件需处理空 DataFrame 场景，避免白屏崩溃
4. **分层架构：** data_loader → sidebar_filter → map_visualizer + chart_generator 的数据流清晰，便于维护
