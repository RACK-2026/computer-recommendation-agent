"""一键采集脚本 - 搜索并解析评测数据，构建本地数据库"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_collector.collector import ReviewCollector


async def main():
    print("=" * 50)
    print("  电脑评测数据采集器")
    print("=" * 50)
    print()

    collector = ReviewCollector(batch_size=3)

    def progress(current, total, model):
        print(f"  [{current}/{total}] {model}...")

    print("开始采集...")
    print()

    results = await collector.collect_all(progress_callback=progress)

    print()
    print("=" * 50)
    print("  采集完成")
    print(f"  总产品数: {results['total']}")
    print(f"  采集成功: {results['success']}")
    print(f"  采集失败: {results['failed']}")
    print(f"  评测总数: {results['reviews_collected']}")
    print("=" * 50)
    print()
    print("现在可以启动服务: python run.py")


if __name__ == "__main__":
    asyncio.run(main())

