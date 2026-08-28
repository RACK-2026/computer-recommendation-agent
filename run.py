"""启动脚本"""
import sys
import io

# 设置控制台编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("[电脑推荐助手] 启动中...")
    print(f"[访问地址] http://{settings.app_host}:{settings.app_port}")
    print("[提示] 按 Ctrl+C 停止服务\n")
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False
    )

