"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .api.health import router as health_router
from .api.chat import router as chat_router
from .db.engine import init_db

# 应用启动时初始化数据库
init_db()

app = FastAPI(title="电脑推荐助手", version="1.0.0")

# 注册路由
app.include_router(health_router)
app.include_router(chat_router)

# 挂载静态文件
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# 首页 - SPA
@app.get("/")
async def index():
    return FileResponse(str(Path(__file__).parent.parent / "templates" / "index.html"))

