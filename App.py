from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 训练数据：基于游戏时长的训练重点
training_data = {
    100: {
        "title": "🔰 新手期 (0-200小时)",
        "focus": "基础 mechanics",
        "description": "刚接触CS:GO，需要建立最基本的游戏习惯",
        "daily_plan": [
            "30分钟 Deathmatch (练枪)",
            "30分钟 休闲模式 (熟悉地图)",
            "10分钟 看Demo (学习基本走位)"
        ],
        "skills": [
            {"name": "准星摆放", "priority": "⭐极高", "tip": "永远把准星放在头的高度"},
            {"name": "压枪", "priority": "⭐高", "tip": "先从AK-47/M4的前10发开始"},
            {"name": "急停", "priority": "⭐高", "tip": "练会'左右左'的急停节奏"},
            {"name": "地图熟悉", "priority": "⭐中", "tip": "先专注Dust2和Mirage"}
        ],
        "weapons": ["AK-47", "M4A4", "AWP (先别急)", "USP-S"],
        "workshop_maps": [
            "Aim Botz - Training (练枪神图)",
            "Recoil Master (压枪练习)"
        ]
    },
    300: {
        "title": "⚔️ 入门期 (200-500小时)",
        "focus": "基础战术意识",
        "description": "枪法有了雏形，开始理解游戏逻辑",
        "daily_plan": [
            "20分钟 Deathmatch (热身)",
            "40分钟 竞技模式 (实战)",
            "20分钟 看自己Demo (找问题)"
        ],
        "skills": [
            {"name": "预瞄", "priority": "⭐极高", "tip": "练习'干拉'时的准星位置"},
            {"name": "道具使用", "priority": "⭐高", "tip": "学5个常用烟雾弹"},
            {"name": "经济管理", "priority": "⭐高", "tip": "什么时候该eco/force"},
            {"name": "小地图意识", "priority": "⭐中", "tip": "每5秒看一眼小地图"}
        ],
        "weapons": ["AK-47", "M4A4", "AWP (开始尝试)", "Deagle"],
        "workshop_maps": [
            "Yprac Practice (道具练习)",
            "Fast Aim/Reflex Training"
        ]
    },
    500: {
        "title": "🏹 进阶期 (500-800小时)",
        "focus": "位置感与配合",
        "description": "枪法稳定，开始打团队配合",
        "daily_plan": [
            "15分钟 Deathmatch (维持手感)",
            "60分钟 竞技模式",
            "15分钟 职业哥Demo (学思路)"
        ],
        "skills": [
            {"name": "补枪", "priority": "⭐极高", "tip": "永远和队友保持补枪距离"},
            {"name": "默认架枪", "priority": "⭐高", "tip": "知道每个位置该看哪里"},
            {"name": "残局处理", "priority": "⭐高", "tip": "1vX时保持冷静"},
            {"name": "道具配合", "priority": "⭐中", "tip": "闪光弹帮队友进点"}
        ],
        "weapons": ["所有主战武器", "练好2-3把枪足矣"],
        "workshop_maps": [
            "Prefire Practice (预瞄练习)",
            "Retake Servers (回防练习)"
        ]
    },
    800: {
        "title": "🔥 高手期 (800-1200小时)",
        "focus": "阅读比赛",
        "description": "开始理解'为什么'而不是'做什么'",
        "daily_plan": [
            "10分钟 Deathmatch (热身)",
            "90分钟 竞技模式",
            "20分钟 分析输的局"
        ],
        "skills": [
            {"name": "开局判断", "priority": "⭐极高", "tip": "根据对方经济/习惯猜战术"},
            {"name": "指挥能力", "priority": "⭐高", "tip": "主动给信息和指令"},
            {"name": "心理战", "priority": "⭐高", "tip": "fake(假打)和偷包"},
            {"name": "Adaptability", "priority": "⭐中", "tip": "随时调整打法"}
        ],
        "weapons": ["专精2-3把", "但不排斥任何武器"],
        "workshop_maps": [
            "CSGOHUB Training",
            "1v1 Arenas"
        ]
    },
    1000: {
        "title": "💎 精英期 (1200-2000小时)",
        "focus": "游戏智商",
        "description": "枪法已是本能，拼的是决策",
        "daily_plan": [
            "5分钟 Deathmatch (热身)",
            "打高质量局",
            "复盘高质量Demo"
        ],
        "skills": [
            {"name": "时间管理", "priority": "⭐极高", "tip": "每个阶段该做什么"},
            {"name": "队友管理", "priority": "⭐高", "tip": "带动团队气氛"},
            {"name": "反套路", "priority": "⭐高", "tip": "识破对方战术并反制"},
            {"name": "Clutch精神", "priority": "⭐中", "tip": "相信能1v5"}
        ],
        "weapons": ["任何枪都能用", "但知道什么时候该用什么"],
        "workshop_maps": [
            "FACEIT Pro League Demos",
            "ESEA Rank S"
        ]
    },
    1500: {
        "title": "👑 大神期 (2000+小时)",
        "focus": "统治力",
        "description": "你就是那个Carry的人",
        "daily_plan": [
            "随意热身",
            "带队上分",
            "教别人（教学相长）"
        ],
        "skills": [
            {"name": "Carry能力", "priority": "⭐极高", "tip": "关键时刻站出来"},
            {"name": "战术大师", "priority": "⭐高", "tip": "能设计战术"},
            {"name": "心理压制", "priority": "⭐高", "tip": "让对手怕你"},
            {"name": "教学能力", "priority": "⭐中", "tip": "带新人"}
        ],
        "weapons": ["人枪合一"],
        "workshop_maps": [
            "Practice with a team",
            "参加小比赛"
        ]
    }
}

# 建议函数：根据小时数给出建议
def get_training_advice(hours):
    if hours < 200:
        return training_data[100]
    elif hours < 500:
        return training_data[300]
    elif hours < 800:
        return training_data[500]
    elif hours < 1200:
        return training_data[800]
    elif hours < 2000:
        return training_data[1000]
    else:
        return training_data[1500]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    hours = float(request.form['hours'])
    advice = get_training_advice(hours)
    return jsonify(advice)

if __name__ == '__main__':
    app.run(debug=True)