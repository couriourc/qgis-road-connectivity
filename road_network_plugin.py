# -*- coding: utf-8 -*-
"""
QGIS 并查集道路网络高亮插件
实现点击道路时，高亮显示所有连通的道路
"""

from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import (
    QgsProject, QgsFeature, QgsVectorLayer,
    QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer,
    QgsSingleSymbolRenderer, QgsLineSymbol
)
from qgis.gui import QgsMapToolIdentifyFeature


class UnionFind:
    """并查集数据结构"""
    
    def __init__(self):
        self.parent = {}
        self.rank = {}
    
    def make_set(self, x):
        """创建单元素集合"""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
    
    def find(self, x):
        """查找根节点（带路径压缩）"""
        if x not in self.parent:
            self.make_set(x)
        
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]
    
    def union(self, x, y):
        """合并两个集合（按秩合并）"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        # 按秩合并
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
    
    def get_component(self, x):
        """获取元素所在连通分量的所有元素"""
        root = self.find(x)
        component = set()
        for node in self.parent:
            if self.find(node) == root:
                component.add(node)
        return component


class RoadNetworkHighlighter:
    """道路网络高亮器"""
    
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.uf = UnionFind()
        self.current_layer = None
        self.original_renderer = None
        self.node_to_features = {}  # 节点到要素ID的映射
        
    def build_union_find(self, layer):
        """构建并查集结构"""
        self.uf = UnionFind()
        self.node_to_features = {}
        self.current_layer = layer
        
        # 保存原始渲染器
        self.original_renderer = layer.renderer().clone()
        
        # 遍历所有要素，建立并查集
        features = layer.getFeatures()
        
        for feature in features:
            gid = feature.id()
            
            # 获取 source 和 target 字段
            source = feature['source'] if 'source' in feature.fields().names() else None
            target = feature['target'] if 'target' in feature.fields().names() else None
            
            if source is None or target is None:
                continue
            
            # 建立并查集
            self.uf.make_set(source)
            self.uf.make_set(target)
            self.uf.union(source, target)
            
            # 记录节点到要素的映射
            if source not in self.node_to_features:
                self.node_to_features[source] = set()
            if target not in self.node_to_features:
                self.node_to_features[target] = set()
            
            self.node_to_features[source].add(gid)
            self.node_to_features[target].add(gid)
        
        return True
    
    def highlight_connected_roads(self, feature):
        """高亮显示连通的道路"""
        if not self.current_layer:
            return
        
        # 获取当前要素的 source 和 target
        source = feature['source'] if 'source' in feature.fields().names() else None
        target = feature['target'] if 'target' in feature.fields().names() else None
        
        if source is None or target is None:
            QMessageBox.warning(
                None, 
                "警告", 
                "所选图层缺少 'source' 或 'target' 字段！"
            )
            return
        
        # 获取连通分量
        component = self.uf.get_component(source)
        
        # 收集所有连通的要素ID
        connected_feature_ids = set()
        for node in component:
            if node in self.node_to_features:
                connected_feature_ids.update(self.node_to_features[node])
        
        # 高亮显示
        self.current_layer.selectByIds(list(connected_feature_ids))
        
        # 显示信息
        QMessageBox.information(
            None,
            "连通性分析",
            f"找到 {len(connected_feature_ids)} 条连通道路\n"
            f"连通节点数: {len(component)}"
        )
        
        # 缩放到选中要素
        self.canvas.zoomToSelected(self.current_layer)
    
    def reset_selection(self):
        """重置选择"""
        if self.current_layer:
            self.current_layer.removeSelection()


class RoadNetworkPlugin:
    """QGIS 插件主类"""
    
    def __init__(self, iface):
        self.iface = iface
        self.highlighter = RoadNetworkHighlighter(iface)
        self.map_tool = None
        self.action = None
    
    def initGui(self):
        """初始化 GUI"""
        self.action = QAction("道路连通性分析", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.toggle_tool)
        
        # 添加到工具栏
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&道路网络分析", self.action)
    
    def unload(self):
        """卸载插件"""
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&道路网络分析", self.action)
        
        if self.map_tool:
            self.iface.mapCanvas().unsetMapTool(self.map_tool)
    
    def toggle_tool(self, checked):
        """切换工具状态"""
        if checked:
            self.activate_tool()
        else:
            self.deactivate_tool()
    
    def activate_tool(self):
        """激活工具"""
        # 获取当前活动图层
        layer = self.iface.activeLayer()
        
        if not layer or not isinstance(layer, QgsVectorLayer):
            QMessageBox.warning(
                None,
                "错误",
                "请选择一个矢量图层！"
            )
            self.action.setChecked(False)
            return
        
        # 检查必要字段
        field_names = [f.name() for f in layer.fields()]
        if 'source' not in field_names or 'target' not in field_names:
            QMessageBox.warning(
                None,
                "错误",
                "图层必须包含 'source' 和 'target' 字段！"
            )
            self.action.setChecked(False)
            return
        
        # 构建并查集
        self.highlighter.build_union_find(layer)
        
        # 创建地图工具
        self.map_tool = QgsMapToolIdentifyFeature(self.iface.mapCanvas(), layer)
        self.map_tool.featureIdentified.connect(self.on_feature_identified)
        
        # 设置地图工具
        self.iface.mapCanvas().setMapTool(self.map_tool)
        
        QMessageBox.information(
            None,
            "提示",
            "已激活道路连通性分析工具\n点击任意道路查看连通网络"
        )
    
    def deactivate_tool(self):
        """停用工具"""
        if self.map_tool:
            self.iface.mapCanvas().unsetMapTool(self.map_tool)
            self.map_tool = None
        
        self.highlighter.reset_selection()
    
    def on_feature_identified(self, feature):
        """要素被识别时的回调"""
        self.highlighter.highlight_connected_roads(feature)


# QGIS 插件入口点
def classFactory(iface):
    return RoadNetworkPlugin(iface)