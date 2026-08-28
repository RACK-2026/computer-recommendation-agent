"""枚举定义"""
from enum import Enum


class DeviceType(str, Enum):
    LAPTOP = "笔记本"
    DESKTOP = "台式机"
    BOTH = "都推荐"


class UserGroup(str, Enum):
    STUDENT = "学生"
    GAMER = "游戏玩家"
    BUSINESS = "商务办公"
    DESIGNER = "设计师/程序员"
    GENERAL = "普通家用"


class ConversationStep(str, Enum):
    GREETING = "greeting"
    CLARIFYING = "clarifying"
    SEARCHING = "searching"
    RECOMMENDING = "recommending"
    FOLLOWUP = "followup"

