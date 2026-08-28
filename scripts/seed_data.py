"""内置种子数据 - 20款热门产品的评测聚合数据，无需联网也能用"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.product import (
    SessionLocal, ProductModel, ProductSpecs,
    ReviewModel, AggregatedScoreModel
)


SEED_PRODUCTS = [
    # ========== 笔记本 ==========
    {
        "product": {
            "brand": "联想", "series": "拯救者", "model_name": "拯救者 Y7000P 2025",
            "device_type": "笔记本", "price": 7299, "original_price": 7999,
            "specs": ProductSpecs(cpu="i7-13650HX", gpu="RTX 4060 8G", ram="16GB DDR5",
                storage="512GB SSD", screen_size="15.6英寸", refresh_rate="165Hz",
                weight="2.4kg", battery="80Wh", os="Windows 11"),
        },
        "reviews_count": 12, "video_reviews": 5,
        "agg": {
            "overall_score": 8.2, "positive_rate": 0.85,
            "performance_score": 8.5, "thermal_score": 8.0,
            "display_score": 8.0, "battery_score": 6.5,
            "build_score": 7.5, "price_score": 7.5,
            "common_pros": ["散热表现优秀", "性能释放充分", "屏幕素质好", "接口丰富", "品牌售后好"],
            "common_cons": ["机身较重不便携", "续航一般", "电源适配器偏大", "高负载噪音明显"],
            "suitable_for": ["游戏玩家", "设计师"],
        }
    },
    {
        "product": {
            "brand": "华硕", "series": "天选", "model_name": "天选 4",
            "device_type": "笔记本", "price": 7499, "original_price": 7999,
            "specs": ProductSpecs(cpu="i7-13650HX", gpu="RTX 4060 8G", ram="16GB DDR5",
                storage="512GB SSD", screen_size="15.6英寸", refresh_rate="165Hz",
                weight="2.1kg", battery="90Wh", os="Windows 11"),
        },
        "reviews_count": 10, "video_reviews": 4,
        "agg": {
            "overall_score": 7.9, "positive_rate": 0.80,
            "performance_score": 7.5, "thermal_score": 7.0,
            "display_score": 7.5, "battery_score": 8.0,
            "build_score": 7.0, "price_score": 7.0,
            "common_pros": ["续航表现不错", "重量控制好", "颜值高", "性价比尚可"],
            "common_cons": ["塑料感较强", "散热噪音大", "屏幕下边框宽", "高负载降频"],
            "suitable_for": ["游戏玩家", "学生"],
        }
    },
    {
        "product": {
            "brand": "惠普", "series": "暗影精灵", "model_name": "暗影精灵 10",
            "device_type": "笔记本", "price": 6999, "original_price": 7499,
            "specs": ProductSpecs(cpu="i7-13650HX", gpu="RTX 4050 6G", ram="16GB DDR5",
                storage="512GB SSD", screen_size="16.1英寸", refresh_rate="165Hz",
                weight="2.3kg", battery="83Wh", os="Windows 11"),
        },
        "reviews_count": 8, "video_reviews": 3,
        "agg": {
            "overall_score": 7.5, "positive_rate": 0.75,
            "performance_score": 7.0, "thermal_score": 6.5,
            "display_score": 6.5, "battery_score": 7.0,
            "build_score": 7.0, "price_score": 8.5,
            "common_pros": ["价格实惠性价比高", "屏幕尺寸大", "接口齐全", "品牌可靠"],
            "common_cons": ["散热表现一般", "屏幕分辨率偏低", "噪音偏大", "做工一般"],
            "suitable_for": ["学生", "游戏玩家"],
        }
    },
    {
        "product": {
            "brand": "联想", "series": "ThinkBook", "model_name": "ThinkBook 14+ 2025",
            "device_type": "笔记本", "price": 5999, "original_price": 6499,
            "specs": ProductSpecs(cpu="i5-13500H", gpu="集显", ram="16GB DDR5",
                storage="512GB SSD", screen_size="14英寸", refresh_rate="90Hz",
                weight="1.4kg", battery="62Wh", os="Windows 11"),
        },
        "reviews_count": 9, "video_reviews": 3,
        "agg": {
            "overall_score": 8.0, "positive_rate": 0.82,
            "performance_score": 7.0, "thermal_score": 7.0,
            "display_score": 8.5, "battery_score": 6.5,
            "build_score": 8.0, "price_score": 8.0,
            "common_pros": ["轻薄便携", "屏幕素质极高", "接口丰富实用", "性价比不错"],
            "common_cons": ["显卡性能不足", "高负载发热", "续航中等", "扬声器一般"],
            "suitable_for": ["商务办公", "学生", "编程"],
        }
    },
    {
        "product": {
            "brand": "苹果", "series": "MacBook Air", "model_name": "MacBook Air M3",
            "device_type": "笔记本", "price": 8999, "original_price": 9499,
            "specs": ProductSpecs(cpu="Apple M3", gpu="Apple M3 10核", ram="8GB",
                storage="256GB SSD", screen_size="13.6英寸", weight="1.24kg",
                battery="52.6Wh", os="macOS"),
        },
        "reviews_count": 15, "video_reviews": 6,
        "agg": {
            "overall_score": 8.8, "positive_rate": 0.90,
            "performance_score": 8.0, "thermal_score": 9.0,
            "display_score": 8.5, "battery_score": 9.5,
            "build_score": 9.5, "price_score": 6.0,
            "common_pros": ["极致轻薄便携", "续航非常出色", "系统生态优秀", "屏幕素质好", "无风扇零噪音"],
            "common_cons": ["价格偏贵", "内存不可扩展", "存储偏小", "部分软件兼容问题"],
            "suitable_for": ["商务办公", "设计师"],
        }
    },
    {
        "product": {
            "brand": "华为", "series": "MateBook", "model_name": "MateBook 14 2025",
            "device_type": "笔记本", "price": 5499, "original_price": 5999,
            "specs": ProductSpecs(cpu="i5-13500H", gpu="集显", ram="16GB DDR5",
                storage="512GB SSD", screen_size="14.2英寸", refresh_rate="120Hz",
                weight="1.31kg", battery="56Wh", os="Windows 11"),
        },
        "reviews_count": 8, "video_reviews": 3,
        "agg": {
            "overall_score": 7.8, "positive_rate": 0.78,
            "performance_score": 7.0, "thermal_score": 7.0,
            "display_score": 8.0, "battery_score": 7.0,
            "build_score": 8.5, "price_score": 7.5,
            "common_pros": ["轻薄做工精致", "屏幕素质好", "华为生态协同", "触控屏实用"],
            "common_cons": ["集显性能有限", "接口偏少", "续航一般", "高负载发热"],
            "suitable_for": ["商务办公", "学生"],
        }
    },
    {
        "product": {
            "brand": "小米", "series": "RedmiBook", "model_name": "RedmiBook Pro 16 2025",
            "device_type": "笔记本", "price": 4999, "original_price": 5499,
            "specs": ProductSpecs(cpu="i5-13500H", gpu="集显", ram="16GB DDR5",
                storage="512GB SSD", screen_size="16英寸", refresh_rate="120Hz",
                weight="1.78kg", battery="72Wh", os="Windows 11"),
        },
        "reviews_count": 7, "video_reviews": 2,
        "agg": {
            "overall_score": 7.6, "positive_rate": 0.76,
            "performance_score": 7.0, "thermal_score": 6.5,
            "display_score": 8.0, "battery_score": 7.5,
            "build_score": 7.0, "price_score": 9.0,
            "common_pros": ["性价比极高", "屏幕素质优秀", "续航不错", "小米生态"],
            "common_cons": ["做工一般", "散热有待提升", "重量偏重", "售后网点少"],
            "suitable_for": ["学生", "商务办公"],
        }
    },
    {
        "product": {
            "brand": "华硕", "series": "ROG", "model_name": "ROG 魔霸新锐 2025",
            "device_type": "笔记本", "price": 9999, "original_price": 10999,
            "specs": ProductSpecs(cpu="i9-13980HX", gpu="RTX 4070 8G", ram="16GB DDR5",
                storage="1TB SSD", screen_size="16英寸", refresh_rate="240Hz",
                weight="2.5kg", battery="90Wh", os="Windows 11"),
        },
        "reviews_count": 6, "video_reviews": 3,
        "agg": {
            "overall_score": 8.5, "positive_rate": 0.87,
            "performance_score": 9.0, "thermal_score": 8.0,
            "display_score": 8.5, "battery_score": 6.0,
            "build_score": 8.5, "price_score": 6.5,
            "common_pros": ["性能顶级", "屏幕素质极佳", "散热优秀", "品牌信仰加成"],
            "common_cons": ["价格昂贵", "机身沉重", "续航一般", "噪音大"],
            "suitable_for": ["游戏玩家", "设计师"],
        }
    },
    {
        "product": {
            "brand": "戴尔", "series": "游匣", "model_name": "游匣 G16 2025",
            "device_type": "笔记本", "price": 7999, "original_price": 8599,
            "specs": ProductSpecs(cpu="i7-13700HX", gpu="RTX 4060 8G", ram="16GB DDR5",
                storage="512GB SSD", screen_size="16英寸", refresh_rate="165Hz",
                weight="2.5kg", battery="86Wh", os="Windows 11"),
        },
        "reviews_count": 6, "video_reviews": 2,
        "agg": {
            "overall_score": 7.4, "positive_rate": 0.72,
            "performance_score": 7.5, "thermal_score": 7.0,
            "display_score": 7.5, "battery_score": 7.0,
            "build_score": 7.5, "price_score": 7.0,
            "common_pros": ["性能均衡", "品牌可靠", "售后好", "屏幕素质不错"],
            "common_cons": ["性价比一般", "机身偏重", "散热中规中矩", "外观设计保守"],
            "suitable_for": ["游戏玩家", "学生"],
        }
    },
    {
        "product": {
            "brand": "机械革命", "series": "旷世", "model_name": "旷世 16 Pro 2025",
            "device_type": "笔记本", "price": 6499, "original_price": 6999,
            "specs": ProductSpecs(cpu="i7-13650HX", gpu="RTX 4060 8G", ram="16GB DDR5",
                storage="1TB SSD", screen_size="16英寸", refresh_rate="240Hz",
                weight="2.4kg", battery="62Wh", os="Windows 11"),
        },
        "reviews_count": 5, "video_reviews": 2,
        "agg": {
            "overall_score": 7.7, "positive_rate": 0.75,
            "performance_score": 7.5, "thermal_score": 7.0,
            "display_score": 7.0, "battery_score": 5.5,
            "build_score": 6.5, "price_score": 8.5,
            "common_pros": ["性价比高", "配置给力", "屏幕刷新率高", "1TB大存储"],
            "common_cons": ["续航较差", "做工一般", "售后网点少", "品牌知名度低"],
            "suitable_for": ["游戏玩家", "学生"],
        }
    },
    {
        "product": {
            "brand": "联想", "series": "拯救者", "model_name": "拯救者 Y9000P 2025",
            "device_type": "笔记本", "price": 11999, "original_price": 12999,
            "specs": ProductSpecs(cpu="i9-13900HX", gpu="RTX 4070 8G", ram="32GB DDR5",
                storage="1TB SSD", screen_size="16英寸", refresh_rate="240Hz",
                weight="2.5kg", battery="80Wh", os="Windows 11"),
        },
        "reviews_count": 8, "video_reviews": 4,
        "agg": {
            "overall_score": 8.6, "positive_rate": 0.88,
            "performance_score": 9.0, "thermal_score": 8.5,
            "display_score": 8.5, "battery_score": 6.0,
            "build_score": 8.5, "price_score": 7.0,
            "common_pros": ["性能顶级", "散热优秀", "屏幕素质极佳", "接口丰富", "做工扎实"],
            "common_cons": ["价格较高", "机身沉重", "续航一般", "适配器大"],
            "suitable_for": ["游戏玩家", "设计师"],
        }
    },
    {
        "product": {
            "brand": "华硕", "series": "ROG", "model_name": "ROG 幻16 2025",
            "device_type": "笔记本", "price": 12499, "original_price": 13999,
            "specs": ProductSpecs(cpu="i9-13900H", gpu="RTX 4070 8G", ram="32GB DDR5",
                storage="1TB SSD", screen_size="16英寸", refresh_rate="240Hz",
                weight="2.0kg", battery="90Wh", os="Windows 11"),
        },
        "reviews_count": 10, "video_reviews": 5,
        "agg": {
            "overall_score": 8.8, "positive_rate": 0.90,
            "performance_score": 8.5, "thermal_score": 8.0,
            "display_score": 9.0, "battery_score": 7.0,
            "build_score": 9.0, "price_score": 6.5,
            "common_pros": ["轻薄性能兼顾", "屏幕素质顶级", "做工精致", "续航不错", "接口齐全"],
            "common_cons": ["价格不菲", "高负载噪音明显", "内存焊死不可升级"],
            "suitable_for": ["设计师", "游戏玩家"],
        }
    },
    {
        "product": {
            "brand": "机械革命", "series": "旷世", "model_name": "机械革命 旷世 16 Pro 2025",
            "device_type": "笔记本", "price": 6499, "original_price": 6999,
            "specs": ProductSpecs(cpu="i7-13650HX", gpu="RTX 4060 8G", ram="16GB DDR5",
                storage="1TB SSD", screen_size="16英寸", refresh_rate="240Hz",
                weight="2.4kg", battery="62Wh", os="Windows 11"),
        },
        "reviews_count": 6, "video_reviews": 3,
        "agg": {
            "overall_score": 7.8, "positive_rate": 0.76,
            "performance_score": 7.5, "thermal_score": 7.0,
            "display_score": 7.0, "battery_score": 5.5,
            "build_score": 6.5, "price_score": 8.5,
            "common_pros": ["性价比高", "配置给力", "240Hz高刷屏", "1TB大存储"],
            "common_cons": ["续航较差", "做工一般", "售后网点少", "品牌知名度低"],
            "suitable_for": ["游戏玩家", "学生"],
        }
    },
    {
        "product": {
            "brand": "苹果", "series": "MacBook Pro", "model_name": "MacBook Pro 14 M4 Pro",
            "device_type": "笔记本", "price": 14999, "original_price": 16499,
            "specs": ProductSpecs(cpu="Apple M4 Pro", gpu="Apple M4 Pro 20核", ram="24GB",
                storage="512GB SSD", screen_size="14.2英寸", refresh_rate="120Hz",
                weight="1.6kg", battery="70Wh", os="macOS"),
        },
        "reviews_count": 12, "video_reviews": 5,
        "agg": {
            "overall_score": 9.0, "positive_rate": 0.92,
            "performance_score": 9.5, "thermal_score": 8.5,
            "display_score": 9.0, "battery_score": 9.0,
            "build_score": 9.5, "price_score": 5.5,
            "common_pros": ["性能极强", "屏幕顶级", "续航出色", "做工精良", "生态优秀"],
            "common_cons": ["价格非常高", "内存硬盘升级贵", "部分软件兼容问题", "机身较重"],
            "suitable_for": ["设计师", "程序员"],
        }
    },
    # ========== 台式机 ==========
    {
        "product": {
            "brand": "DIY", "series": "入门游戏", "model_name": "DIY 入门游戏主机",
            "device_type": "台式机", "price": 4999,
            "specs": ProductSpecs(cpu="R5-7500F", gpu="RTX 4060", ram="16GB DDR5",
                storage="512GB SSD", os="Windows 11"),
        },
        "reviews_count": 8, "video_reviews": 4,
        "agg": {
            "overall_score": 8.5, "positive_rate": 0.88,
            "performance_score": 8.0, "thermal_score": 8.0,
            "display_score": 7.0, "battery_score": 3.0,
            "build_score": 7.5, "price_score": 9.5,
            "common_pros": ["性价比极高", "性能强劲", "可自由定制", "升级空间大"],
            "common_cons": ["需要自己组装", "无统一售后", "需自己排查问题", "占空间"],
            "suitable_for": ["游戏玩家", "学生"],
        }
    },
    {
        "product": {
            "brand": "DIY", "series": "主流游戏", "model_name": "DIY 主流游戏主机",
            "device_type": "台式机", "price": 6999,
            "specs": ProductSpecs(cpu="i5-13400F", gpu="RTX 4060 Ti", ram="32GB DDR5",
                storage="1TB SSD", os="Windows 11"),
        },
        "reviews_count": 10, "video_reviews": 5,
        "agg": {
            "overall_score": 8.8, "positive_rate": 0.90,
            "performance_score": 8.5, "thermal_score": 8.5,
            "display_score": 7.0, "battery_score": 3.0,
            "build_score": 8.0, "price_score": 9.0,
            "common_pros": ["性能甜品级", "性价比极高", "2K游戏通吃", "升级灵活"],
            "common_cons": ["需自己组装", "电源需要选好", "无品牌售后"],
            "suitable_for": ["游戏玩家", "设计师"],
        }
    },
    {
        "product": {
            "brand": "DIY", "series": "设计渲染", "model_name": "DIY 设计主机",
            "device_type": "台式机", "price": 9999,
            "specs": ProductSpecs(cpu="i7-13700K", gpu="RTX 4070 Ti", ram="32GB DDR5",
                storage="1TB SSD + 2TB HDD", os="Windows 11"),
        },
        "reviews_count": 6, "video_reviews": 3,
        "agg": {
            "overall_score": 9.0, "positive_rate": 0.90,
            "performance_score": 9.5, "thermal_score": 8.5,
            "display_score": 7.0, "battery_score": 3.0,
            "build_score": 8.0, "price_score": 7.5,
            "common_pros": ["渲染性能极强", "大内存大存储", "多任务流畅", "稳定性好"],
            "common_cons": ["价格较高", "功耗大", "需要良好散热", "需自己组装"],
            "suitable_for": ["设计师", "程序员"],
        }
    },
    {
        "product": {
            "brand": "联想", "series": "拯救者", "model_name": "拯救者 刃7000K 2025",
            "device_type": "台式机", "price": 6999, "original_price": 7499,
            "specs": ProductSpecs(cpu="i5-13400F", gpu="RTX 4060", ram="16GB DDR4",
                storage="512GB SSD", os="Windows 11"),
        },
        "reviews_count": 7, "video_reviews": 2,
        "agg": {
            "overall_score": 7.8, "positive_rate": 0.78,
            "performance_score": 7.5, "thermal_score": 8.0,
            "display_score": 7.0, "battery_score": 3.0,
            "build_score": 8.0, "price_score": 7.5,
            "common_pros": ["品牌整机省心", "散热不错", "售后方便", "即买即用"],
            "common_cons": ["比DIY贵", "扩展性有限", "电源功率偏小", "配置固定"],
            "suitable_for": ["游戏玩家", "学生"],
        }
    },
    {
        "product": {
            "brand": "惠普", "series": "战99", "model_name": "惠普 战99 2025",
            "device_type": "台式机", "price": 4999, "original_price": 5499,
            "specs": ProductSpecs(cpu="i5-13400", gpu="集显", ram="16GB DDR4",
                storage="512GB SSD", os="Windows 11"),
        },
        "reviews_count": 6, "video_reviews": 1,
        "agg": {
            "overall_score": 7.2, "positive_rate": 0.72,
            "performance_score": 6.5, "thermal_score": 8.0,
            "display_score": 7.0, "battery_score": 3.0,
            "build_score": 7.5, "price_score": 8.0,
            "common_pros": ["稳定可靠", "静音", "商务设计", "售后好"],
            "common_cons": ["显卡性能弱", "不适合游戏", "扩展性一般"],
            "suitable_for": ["商务办公", "普通家用"],
        }
    },
    {
        "product": {
            "brand": "苹果", "series": "Mac", "model_name": "Mac Mini M4 Pro",
            "device_type": "台式机", "price": 10999,
            "specs": ProductSpecs(cpu="Apple M4 Pro", gpu="Apple M4 Pro 20核", ram="24GB",
                storage="512GB SSD", os="macOS"),
        },
        "reviews_count": 9, "video_reviews": 4,
        "agg": {
            "overall_score": 8.6, "positive_rate": 0.87,
            "performance_score": 9.0, "thermal_score": 9.5,
            "display_score": 7.0, "battery_score": 3.0,
            "build_score": 9.0, "price_score": 6.5,
            "common_pros": ["体积小巧", "性能强劲", "非常静音", "功耗低", "macOS生态"],
            "common_cons": ["价格较高", "内存硬盘升级贵", "配件需另购", "游戏支持差"],
            "suitable_for": ["设计师", "程序员", "商务办公"],
        }
    },
]


def seed_database():
    """填充种子数据到数据库"""
    db = SessionLocal()

    try:
        for item in SEED_PRODUCTS:
            p = item["product"]
            # 检查是否已存在
            existing = db.query(ProductModel).filter(
                ProductModel.model_name == p["model_name"]
            ).first()
            if existing:
                continue

            specs = p.get("specs")
            product = ProductModel(
                brand=p["brand"],
                series=p["series"],
                model_name=p["model_name"],
                device_type=p["device_type"],
                price=p["price"],
                original_price=p.get("original_price"),
                specs_json=specs.model_dump_json() if specs else "{}",
            )
            db.add(product)
            db.flush()

            # 写入聚合评分
            agg = item["agg"]
            agg_record = AggregatedScoreModel(
                product_id=product.id,
                overall_score=agg["overall_score"],
                positive_rate=agg["positive_rate"],
                performance_score=agg.get("performance_score"),
                thermal_score=agg.get("thermal_score"),
                display_score=agg.get("display_score"),
                battery_score=agg.get("battery_score"),
                build_score=agg.get("build_score"),
                price_score=agg.get("price_score"),
                total_reviews=item["reviews_count"],
                video_reviews=item["video_reviews"],
                article_reviews=item["reviews_count"] - item["video_reviews"],
                common_pros_json=json.dumps(agg["common_pros"], ensure_ascii=False),
                common_cons_json=json.dumps(agg["common_cons"], ensure_ascii=False),
                suitable_for_json=json.dumps(agg["suitable_for"], ensure_ascii=False),
            )
            db.add(agg_record)

        db.commit()
        count = db.query(AggregatedScoreModel).count()
        print(f"种子数据导入完成！共 {count} 款产品有聚合评分。")

    except Exception as e:
        db.rollback()
        print(f"导入失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

