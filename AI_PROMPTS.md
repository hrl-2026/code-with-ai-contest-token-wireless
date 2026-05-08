# 🤖 Agent 交互日志

**团队名称：** Token Wireless
**成员名单：** [成员1], [成员2], [成员3]
**使用的 AI Coding Agent 工具：** Hermes Agent (DeepSeek V4 Flash)

---

## 📋 交互记录

### 阶段一：需求分析与设计方案

**User Prompt:**
> 读取 GitHub 链接 https://github.com/hrl-2026/code-with-ai-contest-token-wireless 下的所有内容，完成比赛要求的代码开发，并生成要求的所有提交件。严格按照比赛要求进行规划与开发，在反复验证和规划完成详细设计方案前不许开始开发。

---

### 阶段二：核心代码实现

**User Prompt:**
> 生成 map 有关代码时注意不要写类似 st.map(map_data, color_colume="color") 的拼写错误。使用真实地图图片作为背景，数据点更小更分散。

---

**User Prompt:**
> Points colored by RSRP: 🟢 Good (> -90 dBm) | 🟡 Fair (-110 ~ -90 dBm) | 🔴 Weak (< -110 dBm). Hover for details, use layer control to switch map style.
>
> NameError: name 'st_folium' is not defined

---

**User Prompt:**
> 3D Signal Intensity Map (PyDeck)
> 3D columns where height represents download speed (Mbps) and color represents RSRP signal strength. Drag to rotate, scroll to zoom.
>
> TypeError: PydeckMixin.pydeck_chart() got an unexpected keyword argument 'height'

---

**User Prompt:**
> 还是刚才的任务，任务要求里有：数据概览图表：在地图下方，让 AI 生成一个柱状图或饼图，统计当前数据中"各频段的基站数量"或"不同类型终端的占比"。但你把数据概览图标单开了，没有放在2d和3d图下面，请修改

---

**User Prompt:**
> 还是刚才的任务，按照比赛要求帮我把所有内容推到github：code-with-ai-contest-token-wireless上：https://github.com/hrl-2026/code-with-ai-contest-token-wireless/blob/main/README.md

---

**User Prompt:**
> 任务里要求"基础关卡完成：提交代码并执行 git tag basic-done，随后 git push origin basic-done。进阶关卡完成：提交代码并执行 git tag advanced-done，随后 git push origin advanced-done。 (评委将严格以对应 Tag 被推送到代码仓服务器的时间戳作为最终的完赛时间) " 问：这个做到了吗

---

**User Prompt:**
> 3d图片加载不出来，要点一下放大才能加载和查看，这个修复一下

---

**User Prompt:**
> 还是刚才的任务， 运行截图：提供 2-3 张 Web 应用运行时的截图，展示地图和侧边栏交互。这个任务没有按要求，要用png截图，不是html交互，2d和3d截图包含数据图，截取全面一点。

---

**User Prompt:**
> 还是刚才的任务，你没有更新AI_PROMPTS.md和README.md，把现在AI_PROMPTS.md 里面的你的思考路径删掉、把所有我给你输入过的prompts记录其中，然后根据上个命令的修改更新README.md

---

### 阶段三：测试与验证

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

### 问题 2：st.pydeck_chart() 不支持 height 参数
**现象：** `st.pydeck_chart(deck, height=600)` 报 TypeError
**解决：** 移除 height 参数，在 pdk.Deck() 中设置 height=600

### 问题 3：st_folium 未导入
**现象：** `NameError: name 'st_folium' is not defined`
**解决：** 添加 `from streamlit_folium import st_folium` 导入

### 问题 4：3D PyDeck 地图初始不渲染
**现象：** 3D 地图打开时显示为空白，需点击全屏放大后才加载
**解决：** 在 pdk.Deck() 中添加 height=600，并用 st.container(height=650) 包裹

### 问题 5：网络环境依赖安装慢 / 地图瓦片加载失败
**现象：** pip install 超时；OpenStreetMap/CartoDB 瓦片在中国大陆无法加载
**解决：** 切换至清华镜像源 `-i https://pypi.tuna.tsinghua.edu.cn/simple`

---

## 💡 经验总结

1. **地图选型：** Streamlit 的 `st.map()` 功能有限（不支持颜色映射），生产级看板推荐 Folium 或 PyDeck
2. **颜色配置：** 在 data_loader 层预计算颜色（RGBA + Hex），保持各模块颜色一致
3. **空数据保护：** 所有可视化组件需处理空 DataFrame 场景，避免白屏崩溃
4. **分层架构：** data_loader → sidebar_filter → map_visualizer + chart_generator 的数据流清晰，便于维护
5. **Headless 截图：** Playwright 在 headless 模式下 WebGL/PyDeck 无法渲染，地图瓦片受网络环境影响可能不显示
