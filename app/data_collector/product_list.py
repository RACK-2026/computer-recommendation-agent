"""预定义热门口袋名单（80款笔记本 + 20款台式机）"""
from typing import List, Dict
from ..models import DeviceType


def get_product_list() -> List[Dict]:
    """返回预定义产品清单"""
    return LAPTOPS + DESKTOPS


# ============================================================
# 笔记本清单 (80款) - 覆盖各品牌/价位/人群
# ============================================================
LAPTOPS = [
    # --- 联想 (14款) ---
    {"brand": "联想", "series": "拯救者", "model": "拯救者 Y7000P 2025", "device": "laptop"},
    {"brand": "联想", "series": "拯救者", "model": "拯救者 Y9000P 2025", "device": "laptop"},
    {"brand": "联想", "series": "拯救者", "model": "拯救者 R9000P 2025", "device": "laptop"},
    {"brand": "联想", "series": "拯救者", "model": "拯救者 Y7000 2024", "device": "laptop"},
    {"brand": "联想", "series": "小新", "model": "小新 Pro 16 2025", "device": "laptop"},
    {"brand": "联想", "series": "小新", "model": "小新 Pro 14 2025", "device": "laptop"},
    {"brand": "联想", "series": "小新", "model": "小新 16 2025", "device": "laptop"},
    {"brand": "联想", "series": "ThinkBook", "model": "ThinkBook 14+ 2025", "device": "laptop"},
    {"brand": "联想", "series": "ThinkBook", "model": "ThinkBook 16+ 2025", "device": "laptop"},
    {"brand": "联想", "series": "ThinkBook", "model": "ThinkBook 13x Gen 4", "device": "laptop"},
    {"brand": "联想", "series": "ThinkPad", "model": "ThinkPad X1 Carbon Gen 12", "device": "laptop"},
    {"brand": "联想", "series": "ThinkPad", "model": "ThinkPad T14p Gen 2", "device": "laptop"},
    {"brand": "联想", "series": "ThinkPad", "model": "ThinkPad E16 Gen 2", "device": "laptop"},
    {"brand": "联想", "series": "Yoga", "model": "Yoga Pro 14s 2025", "device": "laptop"},

    # --- 华硕 (10款) ---
    {"brand": "华硕", "series": "天选", "model": "天选 4", "device": "laptop"},
    {"brand": "华硕", "series": "天选", "model": "天选 5 Pro", "device": "laptop"},
    {"brand": "华硕", "series": "天选", "model": "天选 Air 2025", "device": "laptop"},
    {"brand": "华硕", "series": "ROG", "model": "ROG 枪神8 Plus", "device": "laptop"},
    {"brand": "华硕", "series": "ROG", "model": "ROG 魔霸新锐 2025", "device": "laptop"},
    {"brand": "华硕", "series": "ROG", "model": "ROG 幻14 Air", "device": "laptop"},
    {"brand": "华硕", "series": "ROG", "model": "ROG 幻16", "device": "laptop"},
    {"brand": "华硕", "series": "无畏", "model": "无畏 Pro 15 2025", "device": "laptop"},
    {"brand": "华硕", "series": "无畏", "model": "无畏 15i 2025", "device": "laptop"},
    {"brand": "华硕", "series": "灵耀", "model": "灵耀14 2025", "device": "laptop"},

    # --- 惠普 (8款) ---
    {"brand": "惠普", "series": "暗影精灵", "model": "暗影精灵 10", "device": "laptop"},
    {"brand": "惠普", "series": "暗影精灵", "model": "暗影精灵 9", "device": "laptop"},
    {"brand": "惠普", "series": "暗影精灵", "model": "暗影精灵 乐享版", "device": "laptop"},
    {"brand": "惠普", "series": "战66", "model": "战66 七代 2025", "device": "laptop"},
    {"brand": "惠普", "series": "战X", "model": "战X 2025 锐龙版", "device": "laptop"},
    {"brand": "惠普", "series": "星Book", "model": "星Book Pro 14 2025", "device": "laptop"},
    {"brand": "惠普", "series": "星Book", "model": "星Book 14 2025", "device": "laptop"},
    {"brand": "惠普", "series": "Spectre", "model": "Spectre x360 16", "device": "laptop"},

    # --- 戴尔 (6款) ---
    {"brand": "戴尔", "series": "游匣", "model": "游匣 G16 2025", "device": "laptop"},
    {"brand": "戴尔", "series": "游匣", "model": "游匣 G15 2024", "device": "laptop"},
    {"brand": "戴尔", "series": "XPS", "model": "XPS 16 2025", "device": "laptop"},
    {"brand": "戴尔", "series": "XPS", "model": "XPS 14 2025", "device": "laptop"},
    {"brand": "戴尔", "series": "灵越", "model": "灵越 16 Plus", "device": "laptop"},
    {"brand": "戴尔", "series": "灵越", "model": "灵越 14 Pro", "device": "laptop"},

    # --- 华为 (6款) ---
    {"brand": "华为", "series": "MateBook", "model": "MateBook X Pro 2025", "device": "laptop"},
    {"brand": "华为", "series": "MateBook", "model": "MateBook 14 2025", "device": "laptop"},
    {"brand": "华为", "series": "MateBook", "model": "MateBook 16s 2025", "device": "laptop"},
    {"brand": "华为", "series": "MateBook", "model": "MateBook D 16 2025", "device": "laptop"},
    {"brand": "华为", "series": "MateBook", "model": "MateBook 14s 2024", "device": "laptop"},
    {"brand": "华为", "series": "MateBook", "model": "MateBook GT 14", "device": "laptop"},

    # --- 小米/Redmi (5款) ---
    {"brand": "小米", "series": "RedmiBook", "model": "RedmiBook Pro 16 2025", "device": "laptop"},
    {"brand": "小米", "series": "RedmiBook", "model": "RedmiBook Pro 14 2025", "device": "laptop"},
    {"brand": "小米", "series": "RedmiBook", "model": "RedmiBook 16 2025", "device": "laptop"},
    {"brand": "小米", "series": "小米", "model": "小米笔记本 Pro 16 2024", "device": "laptop"},
    {"brand": "小米", "series": "RedmiG", "model": "Redmi G 游戏本 2024", "device": "laptop"},

    # --- 苹果 (4款) ---
    {"brand": "苹果", "series": "MacBook Pro", "model": "MacBook Pro 14 M4 Pro", "device": "laptop"},
    {"brand": "苹果", "series": "MacBook Pro", "model": "MacBook Pro 16 M4 Max", "device": "laptop"},
    {"brand": "苹果", "series": "MacBook Air", "model": "MacBook Air M3", "device": "laptop"},
    {"brand": "苹果", "series": "MacBook Air", "model": "MacBook Air M4", "device": "laptop"},

    # --- 宏碁 (5款) ---
    {"brand": "宏碁", "series": "掠夺者", "model": "掠夺者 擎 Neo 2025", "device": "laptop"},
    {"brand": "宏碁", "series": "掠夺者", "model": "掠夺者 战斧 16", "device": "laptop"},
    {"brand": "宏碁", "series": "非凡", "model": "非凡 Go 16 2025", "device": "laptop"},
    {"brand": "宏碁", "series": "蜂鸟", "model": "蜂鸟 Swift 14", "device": "laptop"},
    {"brand": "宏碁", "series": "暗影骑士", "model": "暗影骑士 龙 2025", "device": "laptop"},

    # --- 机械革命 (5款) ---
    {"brand": "机械革命", "series": "旷世", "model": "旷世 16 Pro 2025", "device": "laptop"},
    {"brand": "机械革命", "series": "耀世", "model": "耀世 15 Pro 2025", "device": "laptop"},
    {"brand": "机械革命", "series": "翼龙", "model": "翼龙 15 Pro 2025", "device": "laptop"},
    {"brand": "机械革命", "series": "极光", "model": "极光 X 2025", "device": "laptop"},
    {"brand": "机械革命", "series": "蛟龙", "model": "蛟龙 16 Pro 2025", "device": "laptop"},

    # --- 七彩虹 (3款) ---
    {"brand": "七彩虹", "series": "隐星", "model": "隐星 P16 2025", "device": "laptop"},
    {"brand": "七彩虹", "series": "将星", "model": "将星 X17 Pro 2025", "device": "laptop"},
    {"brand": "七彩虹", "series": "橘宝", "model": "橘宝 R15 2025", "device": "laptop"},

    # --- 神舟 (3款) ---
    {"brand": "神舟", "series": "战神", "model": "战神 S8 2025", "device": "laptop"},
    {"brand": "神舟", "series": "战神", "model": "战神 T8 Pro 2025", "device": "laptop"},
    {"brand": "神舟", "series": "优雅", "model": "优雅 X5 2025", "device": "laptop"},

    # --- 荣耀 (3款) ---
    {"brand": "荣耀", "series": "MagicBook", "model": "MagicBook Pro 16 2025", "device": "laptop"},
    {"brand": "荣耀", "series": "MagicBook", "model": "MagicBook 14 2025", "device": "laptop"},
    {"brand": "荣耀", "series": "MagicBook", "model": "MagicBook X 16 Pro 2025", "device": "laptop"},

    # --- 微星 (3款) ---
    {"brand": "微星", "series": "泰坦", "model": "泰坦 GP68 HX 2025", "device": "laptop"},
    {"brand": "微星", "series": "绝影", "model": "绝影 16 AI Studio", "device": "laptop"},
    {"brand": "微星", "series": "创造者", "model": "创造者 Z16 HX", "device": "laptop"},
]

# ============================================================
# 台式机清单 (20款)
# ============================================================
DESKTOPS = [
    # 品牌整机
    {"brand": "联想", "series": "拯救者", "model": "拯救者 刃7000K 2025", "device": "desktop"},
    {"brand": "联想", "series": "拯救者", "model": "拯救者 刃9000K 2025", "device": "desktop"},
    {"brand": "联想", "series": "GeekPro", "model": "GeekPro 2025", "device": "desktop"},
    {"brand": "惠普", "series": "暗影精灵", "model": "暗影精灵 10 台式机", "device": "desktop"},
    {"brand": "惠普", "series": "战99", "model": "战99 桌面工作站 2025", "device": "desktop"},
    {"brand": "戴尔", "series": "XPS", "model": "XPS Desktop 8960", "device": "desktop"},
    {"brand": "戴尔", "series": "游匣", "model": "游匣 G5 台式机", "device": "desktop"},
    {"brand": "华硕", "series": "ROG", "model": "ROG 冰刃 X 2025", "device": "desktop"},
    {"brand": "华硕", "series": "天选", "model": "天选 X 2025 台式机", "device": "desktop"},
    {"brand": "苹果", "series": "Mac", "model": "Mac Mini M4 Pro", "device": "desktop"},
    {"brand": "苹果", "series": "Mac", "model": "Mac Studio M3 Ultra", "device": "desktop"},
    {"brand": "苹果", "series": "Mac", "model": "Mac Pro M4", "device": "desktop"},

    # DIY 方案
    {"brand": "DIY", "series": "入门办公", "model": "DIY 办公主机 (i5-13400/16G/512G)", "device": "desktop"},
    {"brand": "DIY", "series": "主流游戏", "model": "DIY 游戏主机 (i5-13400F/RTX4060)", "device": "desktop"},
    {"brand": "DIY", "series": "高性能游戏", "model": "DIY 游戏主机 (i7-13700F/RTX4070)", "device": "desktop"},
    {"brand": "DIY", "series": "设计渲染", "model": "DIY 设计主机 (i7-13700K/RTX4070Ti)", "device": "desktop"},
    {"brand": "DIY", "series": "极致性能", "model": "DIY 旗舰主机 (i9-13900K/RTX4090)", "device": "desktop"},
    {"brand": "DIY", "series": "入门游戏", "model": "DIY 入门游戏机 (R5-7500F/RTX4060)", "device": "desktop"},
    {"brand": "DIY", "series": "ITX便携", "model": "DIY ITX 迷你主机 (R7-7800X3D/RTX4070)", "device": "desktop"},
    {"brand": "DIY", "series": "全白海景房", "model": "DIY 全白主题 (i5-13600KF/RTX4070)", "device": "desktop"},
]

