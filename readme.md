# 🛣️ QGIS Road Network Connectivity Analyzer

[English](#english) | [中文](#中文)

<div id="english"></div>

## English

A QGIS plugin for fast road network connectivity analysis based on Union-Find algorithm. Click any road feature to automatically highlight all connected roads in the same network component.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![QGIS](https://img.shields.io/badge/QGIS-3.0+-green.svg)](https://qgis.org)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)

### ✨ Features

- **🚀 Lightning Fast**: Union-Find algorithm with near O(1) query time complexity
- **🎯 One-Click Analysis**: Click any road to select all connected roads instantly
- **📊 Real-time Statistics**: Display number of connected roads and nodes
- **🔍 Auto Zoom**: Automatically zoom to selected road extent
- **💡 Visual Feedback**: Clear highlighting of connected road networks
- **🔧 Easy to Use**: Simple toolbar button, no complex configuration needed

### 📸 Screenshots

```
[Add screenshots here showing:]
1. Plugin toolbar button
2. Before click - normal road display
3. After click - highlighted connected roads
4. Statistics dialog
```

### 🚀 Quick Start

#### Installation

**Method 1: Manual Installation (Recommended)**

1. Download or clone this repository:
```bash
git clone https://github.com/couriourc/qgis-road-connectivity.git
```

2. Locate your QGIS plugins directory:
   - **Windows**: `C:\Users\{username}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`

3. Copy the `road_network_analyzer` folder to the plugins directory

4. Restart QGIS

5. Enable the plugin:
   - Go to **Plugins** → **Manage and Install Plugins**
   - Find "Road Network Analyzer" in the "Installed" tab
   - Check the box to enable it

**Method 2: From QGIS Plugin Repository (Coming Soon)**
```
Plugins → Manage and Install Plugins → All → Search "Road Network Analyzer"
```

#### Basic Usage

1. **Prepare Your Data**
   
   Your road layer must contain these fields:
   - `source` (Integer/String): Start node ID
   - `target` (Integer/String): End node ID
   
   Example data structure:
   ```
   | gid | source | target | name       | fclass    |
   | --- | ------ | ------ | ---------- | --------- |
   | 1   | 1001   | 1002   | Route 204  | primary   |
   | 2   | 1002   | 1003   | Route 204  | primary   |
   | 3   | 1003   | 1004   | Route 204  | primary   |
   | 4   | 2001   | 2002   | County 101 | secondary |
   ```

2. **Load Your Layer**
   - Open your road network layer in QGIS
   - Ensure the layer is selected in the Layers Panel

3. **Activate the Tool**
   - Click the "Road Network Connectivity" button in the toolbar
   - Or go to **Plugins** → **Road Network Analysis** → **Road Network Connectivity**

4. **Click to Analyze**
   - Click any road feature on the map
   - All connected roads will be highlighted automatically
   - A dialog will show statistics (number of connected roads and nodes)
   - Map will zoom to the extent of selected roads

5. **Deactivate**
   - Click the tool button again to deactivate
   - Or select another map tool

### 📊 Data Requirements

#### Required Fields

| Field    | Type           | Description                       |
| -------- | -------------- | --------------------------------- |
| `source` | Integer/String | Start node ID of the road segment |
| `target` | Integer/String | End node ID of the road segment   |

#### Optional Fields

| Field    | Description           | Purpose                                        |
| -------- | --------------------- | ---------------------------------------------- |
| `gid`    | Feature unique ID     | Tracking and management                        |
| `name`   | Road name             | Identification                                 |
| `fclass` | Road classification   | Filtering (e.g., motorway, primary, secondary) |
| `ref`    | Road reference number | Like S204, G104 in China                       |

#### Compatible Data Sources

1. **OpenStreetMap (OSM)**
   - Import with osm2pgsql or QGIS
   - Usually contains required fields

2. **pgRouting**
   - Generate topology with `pgr_createTopology()`
   - Fully compatible

3. **Custom Data**
   - Ensure `source` and `target` fields exist
   - Node IDs should be consistent (adjacent roads share nodes)

### 🧮 Algorithm

This plugin uses the **Union-Find (Disjoint Set Union)** data structure for efficient connectivity analysis.

#### Core Operations

```python
find(x)    # Find root node - O(α(n)) ≈ O(1)
union(x,y) # Merge two sets - O(α(n)) ≈ O(1)
```

#### Optimizations

- **Path Compression**: Flatten tree structure during find operations
- **Union by Rank**: Keep trees balanced by attaching smaller tree to larger tree

#### Time Complexity

| Operation     | Complexity | Note                  |
| ------------- | ---------- | --------------------- |
| Build         | O(n)       | n = number of roads   |
| Find          | O(α(n))    | α(n) ≈ constant (< 5) |
| Union         | O(α(n))    | Same as find          |
| Get Component | O(n)       | Traverse all nodes    |

### 🎯 Use Cases

1. **Network Completeness Check**
   - Verify if a provincial road is fully connected
   - Identify gaps or breaks in road networks

2. **Isolated Network Detection**
   - Find disconnected road components
   - Useful for data quality control

3. **Infrastructure Planning**
   - Identify critical bridges and bottlenecks
   - Analyze network resilience

4. **Data Quality Assurance**
   - Detect topology errors
   - Find dead-end roads

### 🛠️ Development

#### Project Structure

```
road_network_analyzer/
├── __init__.py              # Plugin initialization
├── road_network_plugin.py   # Main plugin code
├── metadata.txt             # Plugin metadata
├── README.md               # This file
├── LICENSE                 # MIT License
└── icons/                  # Plugin icons (optional)
    └── icon.png
```

#### Requirements

- QGIS >= 3.0
- Python >= 3.6
- PyQt5 (included with QGIS)

#### Building from Source

```bash
# Clone repository
git clone https://github.com/couriourc/qgis-road-connectivity.git
cd qgis-road-connectivity

# No build step needed - pure Python plugin
# Copy to QGIS plugins directory and restart QGIS
```

#### Running Tests

```bash
# Unit tests (coming soon)
python -m pytest tests/

# Integration tests in QGIS
# Use QGIS Python Console to test
```

### 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**
   - Open an issue with detailed description
   - Include QGIS version, OS, and error messages

2. **Suggest Features**
   - Open an issue with your idea
   - Explain the use case and benefits

3. **Submit Pull Requests**
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/AmazingFeature`)
   - Commit your changes (`git commit -m 'Add some AmazingFeature'`)
   - Push to the branch (`git push origin feature/AmazingFeature`)
   - Open a Pull Request

#### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Update README for new features
- Test with multiple QGIS versions if possible

### 📝 Changelog

#### Version 1.0.0 (2024-11-08)
- Initial release
- Basic Union-Find implementation
- Click-to-highlight functionality
- Statistics display
- Auto-zoom to selected features

### ❓ FAQ

**Q: Why do I get "Layer must contain 'source' and 'target' fields" error?**

A: Your layer is missing required fields. Use pgRouting's `pgr_createTopology()` or manually add these fields with node IDs.

**Q: Can I use this with OSM data directly?**

A: Yes, but OSM data needs topology processing first. Use osm2pgrouting or similar tools to generate source/target fields.

**Q: How do I handle large datasets (> 100k roads)?**

A: The plugin handles large datasets efficiently due to Union-Find optimization. Initial building may take a few seconds, but queries are instant.

**Q: Can I export the connectivity analysis results?**

A: Yes, see the Advanced Usage section in the full documentation for Python console scripts to add component_id fields.

**Q: Does this work with 3D road networks?**

A: The plugin analyzes topological connectivity only, not geometric 3D connections (e.g., overpasses are treated as connected).

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- QGIS Development Team for the excellent GIS platform
- OpenStreetMap contributors for road network data
- pgRouting project for routing and network analysis inspiration

### 📧 Contact

- **Author**: CouriourC
- **Email**: godakid@outlook.com
- **GitHub**: [@couriourc](https://github.com/couriourc)
- **Issues**: [GitHub Issues](https://github.com/couriourc/qgis-road-connectivity/issues)

---

<div id="中文"></div>

## 中文

基于并查集算法的 QGIS 道路网络连通性分析插件。点击任意道路要素，自动高亮显示所有与之连通的道路。

### ✨ 功能特性

- **🚀 高效算法**：基于并查集数据结构，查询时间复杂度接近 O(1)
- **🎯 一键操作**：点击任意道路，自动选中所有连通道路
- **📊 实时统计**：显示连通道路数量和节点数
- **🔍 自动缩放**：自动缩放地图到选中道路范围
- **💡 可视化**：直观的高亮显示效果
- **🔧 易用性**：简单的工具栏按钮，无需复杂配置

### 🚀 快速开始

#### 安装方法

**方法一：手动安装（推荐）**

1. 下载或克隆本仓库：
```bash
git clone https://github.com/couriourc/qgis-road-connectivity.git
```

2. 定位 QGIS 插件目录：
   - **Windows**: `C:\Users\{用户名}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`

3. 将 `road_network_analyzer` 文件夹复制到插件目录

4. 重启 QGIS

5. 启用插件：
   - 打开 **插件** → **管理和安装插件**
   - 在"已安装"标签页找到"Road Network Analyzer"
   - 勾选启用

**方法二：从 QGIS 插件仓库安装（即将推出）**
```
插件 → 管理和安装插件 → 全部 → 搜索 "Road Network Analyzer"
```

#### 基本使用

1. **准备数据**
   
   道路图层必须包含以下字段：
   - `source`（整数/字符串）：起点节点 ID
   - `target`（整数/字符串）：终点节点 ID
   
   数据结构示例：
   ```
   | gid | source | target | name    | fclass    |
   | --- | ------ | ------ | ------- | --------- |
   | 1   | 1001   | 1002   | 省道204 | primary   |
   | 2   | 1002   | 1003   | 省道204 | primary   |
   | 3   | 1003   | 1004   | 省道204 | primary   |
   | 4   | 2001   | 2002   | 县道101 | secondary |
   ```

2. **加载图层**
   - 在 QGIS 中打开道路网络图层
   - 确保图层在图层面板中被选中

3. **激活工具**
   - 点击工具栏的"道路连通性分析"按钮
   - 或选择菜单 **插件** → **道路网络分析** → **道路连通性分析**

4. **点击分析**
   - 在地图上点击任意道路要素
   - 所有连通的道路将自动高亮显示
   - 弹出对话框显示统计信息（连通道路数和节点数）
   - 地图自动缩放到选中道路范围

5. **停用工具**
   - 再次点击工具按钮停用
   - 或选择其他地图工具

### 📊 数据要求

#### 必需字段

| 字段     | 类型        | 说明            |
| -------- | ----------- | --------------- |
| `source` | 整数/字符串 | 道路起点节点 ID |
| `target` | 整数/字符串 | 道路终点节点 ID |

#### 可选字段

| 字段     | 说明         | 用途                                    |
| -------- | ------------ | --------------------------------------- |
| `gid`    | 要素唯一标识 | 追踪和管理                              |
| `name`   | 道路名称     | 识别                                    |
| `fclass` | 道路功能分类 | 过滤（如 motorway, primary, secondary） |
| `ref`    | 道路编号     | 如中国的 S204, G104                     |

#### 兼容数据源

1. **OpenStreetMap (OSM)**
   - 使用 osm2pgsql 或 QGIS 导入
   - 通常包含所需字段

2. **pgRouting**
   - 使用 `pgr_createTopology()` 生成拓扑
   - 完全兼容

3. **自定义数据**
   - 确保包含 `source` 和 `target` 字段
   - 节点 ID 应保持一致（相邻道路共享节点）

### 🧮 算法原理

本插件使用**并查集（Union-Find / Disjoint Set Union）**数据结构进行高效的连通性分析。

#### 核心操作

```python
find(x)    # 查找根节点 - O(α(n)) ≈ O(1)
union(x,y) # 合并两个集合 - O(α(n)) ≈ O(1)
```

#### 优化技术

- **路径压缩**：在查找过程中扁平化树结构
- **按秩合并**：将较小的树附加到较大的树以保持平衡

#### 时间复杂度

| 操作         | 复杂度  | 说明               |
| ------------ | ------- | ------------------ |
| 构建         | O(n)    | n = 道路数量       |
| 查找         | O(α(n)) | α(n) ≈ 常数（< 5） |
| 合并         | O(α(n)) | 同查找             |
| 获取连通分量 | O(n)    | 遍历所有节点       |

### 🎯 应用场景

1. **道路网络完整性检查**
   - 验证省道是否完整连通
   - 识别道路网络中的缺口或断点

2. **孤立网络检测**
   - 发现断开的道路组件
   - 用于数据质量控制

3. **基础设施规划**
   - 识别关键桥梁和瓶颈
   - 分析网络韧性

4. **数据质量保证**
   - 检测拓扑错误
   - 查找断头路

### 🛠️ 开发说明

#### 项目结构

```
road_network_analyzer/
├── __init__.py              # 插件初始化
├── road_network_plugin.py   # 主程序代码
├── metadata.txt             # 插件元数据
├── README.md               # 本文件
├── LICENSE                 # MIT 许可证
└── icons/                  # 插件图标（可选）
    └── icon.png
```

#### 依赖要求

- QGIS >= 3.0
- Python >= 3.6
- PyQt5（QGIS 自带）

#### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/couriourc/qgis-road-connectivity.git
cd qgis-road-connectivity

# 无需构建步骤 - 纯 Python 插件
# 复制到 QGIS 插件目录并重启 QGIS
```

### 🤝 贡献指南

欢迎贡献！以下是你可以帮助的方式：

1. **报告 Bug**
   - 开启 Issue 并提供详细描述
   - 包含 QGIS 版本、操作系统和错误信息

2. **建议新功能**
   - 开启 Issue 说明你的想法
   - 解释使用场景和好处

3. **提交 Pull Request**
   - Fork 本仓库
   - 创建功能分支（`git checkout -b feature/新功能`）
   - 提交更改（`git commit -m '添加某某功能'`）
   - 推送到分支（`git push origin feature/新功能`）
   - 开启 Pull Request

#### 开发规范

- 遵循 PEP 8 代码风格
- 为所有函数添加文档字符串
- 更新 README 说明新功能
- 尽可能测试多个 QGIS 版本

### 📝 更新日志

#### 版本 1.0.0 (2024-11-08)
- 初始版本发布
- 基础并查集实现
- 点击高亮功能
- 统计信息显示
- 自动缩放到选中要素

### ❓ 常见问题

**问：为什么提示"图层必须包含 'source' 和 'target' 字段"错误？**

答：你的图层缺少必需字段。使用 pgRouting 的 `pgr_createTopology()` 或手动添加带节点 ID 的这些字段。

**问：能直接使用 OSM 数据吗？**

答：可以，但 OSM 数据需要先进行拓扑处理。使用 osm2pgrouting 或类似工具生成 source/target 字段。

**问：如何处理大数据集（> 10万条道路）？**

答：插件由于并查集优化可以高效处理大数据集。初次构建可能需要几秒钟，但查询是即时的。

**问：能导出连通性分析结果吗？**

答：可以，查看完整文档中的高级用法部分，有 Python 控制台脚本示例来添加 component_id 字段。

**问：支持 3D 道路网络吗？**

答：插件只分析拓扑连通性，不考虑几何 3D 连接（如立交桥会被视为连通）。

### 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

### 🙏 致谢

- QGIS 开发团队提供的优秀 GIS 平台
- OpenStreetMap 贡献者提供的道路网络数据
- pgRouting 项目提供的路由和网络分析灵感

### 📧 联系方式

- **作者**：CouriourC
- **邮箱**：godakid@outlook.com
- **GitHub**：[@couriourc](https://github.com/couriourc)
- **问题反馈**：[GitHub Issues](https://github.com/couriourc/qgis-road-connectivity/issues)

---

## ⭐ Star History

如果这个项目对你有帮助，请给一个 Star ⭐！

If this project helps you, please give it a star ⭐!
