#!/usr/bin/env python3
"""
gen_html.py - 意大利语5词竖屏教学页面生成器
用法：python gen_html.py --output numbers_01_light.html --audio assets/numbers_01.mp3 --words "Uno,Due,Tre,Quattro,Cinque" --zh "一,二,三,四,五" --en "one,two,three,four,five" --phonetic "乌诺,杜埃,特雷,夸特罗,钦奎" --icons "1️⃣,2️⃣,3️⃣,4️⃣,5️⃣"
"""

import argparse
import sys
import os
import re
from pathlib import Path

# 尝试导入 pydub 获取音频时长
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("⚠️ pydub 未安装，将使用估算时长。建议安装：pip install pydub")


def get_audio_duration(audio_path):
    """获取音频总时长（秒）"""
    if not PYDUB_AVAILABLE:
        return 34.11  # 默认估算值
    try:
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0
    except Exception as e:
        print(f"⚠️ 无法读取音频时长：{e}，使用默认值")
        return 34.11


def build_timeline(words_it, audio_path):
    """
    根据音频实际时长构建精确GSAP时间线
    
    策略：
    1. 获取音频总时长
    2. 均分5张卡片的时间（每张卡片约占 总时长/5）
    3. 每张卡片：入场0.3s + 内容展示 + 出场0.25s + 间隔
    """
    total_duration = get_audio_duration(audio_path)
    card_count = len(words_it)
    time_per_card = total_duration / card_count
    
    # 每张卡片的时间分配：
    # 0 ~ enter_dur: 入场动画
    # enter_dur ~ card_dur - exit_dur: 停留
    # card_dur - exit_dur ~ card_dur: 出场动画
    enter_dur = 0.3
    exit_dur = 0.25
    gap = 0.1  # 卡片切换间隔
    
    timeline = []
    current_time = 0.0
    
    for i in range(card_count):
        card_id = f"#card-{i+1}"
        dot_id = f"#dot-{i+1}"
        next_dot_id = f"#dot-{i+2}" if i < card_count - 1 else None
        
        card_dur = time_per_card
        
        # 入场
        timeline.append(f"  // ===== 第{i+1}词 =====")
        timeline.append(f"  tl.fromTo('{card_id}', {{ opacity:0, scale:0.85 }}, {{ opacity:1, scale:1, duration:{enter_dur}, ease:'back.out(1.5)' }}, {current_time.toFixed(3)});")
        timeline.append(f"  tl.set('{dot_id}', {{ className:'dot current' }}, {current_time.toFixed(3)});")
        
        # 出场
        exit_time = current_time + card_dur - exit_dur
        timeline.append(f"  tl.to('{card_id}', {{ opacity:0, scale:0.95, duration:{exit_dur}, ease:'power2.in' }}, {exit_time.toFixed(3)});")
        timeline.append(f"  tl.set('{dot_id}', {{ className:'dot active' }}, {exit_time.toFixed(3)});")
        
        if next_dot_id:
            next_time = current_time + card_dur + gap
            timeline.append(f"  tl.set('{next_dot_id}', {{ className:'dot current' }}, {next_time.toFixed(3)});")
        
        current_time += card_dur + gap
    
    return timeline, total_duration


def generate_html(words_it, words_zh, words_en, phonetics, icons, audio_path, output_path):
    """生成完整的HTML文件"""
    
    # 构建时间线
    timeline_lines, total_duration = build_timeline(words_it, audio_path)
    timeline_js = "\n".join(timeline_lines)
    
    # 构建5张卡片HTML
    cards_html = []
    for i, (it, zh, en, ph, icon) in enumerate(zip(words_it, words_zh, words_en, phonetics, icons)):
        card = f"""  <div class="card-wrap" id="card-{i+1}">
    <div class="card">
      <div class="card-num">PAROLA {i+1} / 第{i+1}词</div>
      <div class="card-icon">{icon}</div>
      <div class="card-it">{it}</div>
      <div class="card-zh">{zh}</div>
      <div class="card-en">{en}</div>
      <div class="card-phonetic">谐音：{ph}</div>
    </div>
  </div>"""
        cards_html.append(card)
    
    cards_js = "\n".join(cards_html)
    
    # 构建5个圆点
    dots_html = []
    for i in range(len(words_it)):
        dots_html.append(f'    <div class="dot" id="dot-{i+1}"></div>')
    dots_js = "\n".join(dots_html)
    
    # 完整HTML模板
    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>意大利语单词学习</title>
<style>
  * {{ margin:0; padding:0; box-sizing: border-box; }}
  body {{
    width: 1080px; height: 1920px; overflow: hidden;
    background: #f5f0eb;
    font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', sans-serif;
    display: flex; align-items: center; justify-content: center;
  }}
  .stage {{ width: 1080px; height: 1920px; position: relative; display: flex; align-items: center; justify-content: center; }}

  .card-wrap {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; opacity: 0; }}
  .card {{ width: 880px; background: #ffffff; border-radius: 48px; padding: 60px 70px 80px; text-align: center; border:2px solid rgba(206,43,55,0.2); box-shadow: 0 20px 80px rgba(0,0,0,0.08); position: relative; overflow: hidden; }}
  .card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 8px; background: linear-gradient(90deg, #ce2b37, #009246, #ce2b37); border-radius: 48px 48px 0 0; }}
  .card-num {{ font-size: 24px; color: #ce2b37; font-weight: 700; letter-spacing: 6px; margin-bottom: 24px; opacity: 0.6; }}
  .card-icon {{ font-size: 160px; line-height: 1.2; margin-bottom: 28px; filter: drop-shadow(0 8px 20px rgba(0,0,0,0.1)); }}
  .card-it {{ font-size: 72px; font-weight: 800; color: #1a1a2e; letter-spacing: 2px; margin-bottom: 16px; line-height: 1.3; }}
  .card-zh {{ font-size: 44px; color: #ce2b37; margin-bottom: 12px; font-weight: 700; }}
  .card-en {{ font-size: 28px; color: #999; font-style: italic; margin-bottom: 20px; }}
  .card-phonetic {{ font-size: 36px; color: #ce2b37; background: rgba(206,43,55,0.08); display: inline-block; padding: 8px 28px; border-radius: 20px; font-weight: 600; }}

  /* 意大利国旗装饰 */
  .deco-green {{ position: absolute; top: 0; left: 0; width: 12px; height: 100%; background: #009246; opacity: 0.08; }}
  .deco-red {{ position: absolute; top: 0; right: 0; width: 12px; height: 100%; background: #ce2b37; opacity: 0.08; }}
  .corner-deco {{ position: absolute; width: 120px; height: 120px; opacity: 0.07; z-index: 0; pointer-events: none; }}
  .corner-tl {{ top: 0; left: 0; border-top: 6px solid #ce2b37; border-left: 6px solid #ce2b37; }}
  .corner-tr {{ top: 0; right: 0; border-top: 6px solid #009246; border-right: 6px solid #009246; }}

  /* 顶部标题 */
  .top-header {{ position: absolute; top: 238px; left: 0; right: 0; text-align: center; z-index: 10; opacity: 0; }}
  .top-title {{ font-size: 41px; font-weight: 800; color: #1a1a2e; letter-spacing: 4px; }}
  .top-sub {{ font-size: 22px; color: #ce2b37; margin-top: 8px; font-weight: 600; letter-spacing: 2px; }}
  .flag-mini {{ display: inline-block; width: 28px; height: 18px; background: linear-gradient(to right, #009246 33.33%, #fff 33.33%, #fff 66.66%, #ce2b37 66.66%); border-radius: 3px; vertical-align: middle; margin: 0 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.10); }}

  /* 中间品牌logo */
  .middle-brand {{ position: absolute; top: 420px; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 16px; opacity: 0; z-index: 10; }}
  .brand-logo {{ width: 68px; height: 68px; border-radius: 14px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
  .brand-text {{ font-size: 29px; color: rgba(0,0,0,0.2); letter-spacing: 6px; font-weight: 700; }}

  /* 5圆点进度条 */
  .dot-progress {{ position: absolute; bottom: 265px; left: 0; right: 0; display: flex; justify-content: center; gap: 24px; z-index: 10; opacity: 0; }}
  .dot {{ width: 28px; height: 28px; border-radius: 50%; background: rgba(206,43,55,0.15); border: 3px solid rgba(206,43,55,0.25); transition: all 0.4s ease; }}
  .dot.active {{ background: #ce2b37; border-color: #ce2b37; box-shadow: 0 0 12px rgba(206,43,55,0.4); }}
  .dot.current {{ background: #009246; border-color: #009246; box-shadow: 0 0 12px rgba(0,146,70,0.5); transform: scale(1.25); }}

  /* 底部品牌logo */
  .bottom-brand {{ position: absolute; bottom: 405px; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 16px; opacity: 0; z-index: 10; }}

  /* 主进度条 */
  .progress-bar {{ position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: rgba(206,43,55,0.1); }}
  .progress-fill {{ height: 100%; width: 0; background: linear-gradient(90deg, #ce2b37, #009246); border-radius: 2px; }}
</style>
</head>
<body>
<div class="stage">
  <div class="deco-green"></div>
  <div class="deco-red"></div>
  <div class="corner-deco corner-tl"></div>
  <div class="corner-deco corner-tr"></div>

  <!-- 顶部标题 -->
  <div class="top-header" id="top-header">
    <div class="top-title"><span class="flag-mini"></span>每日学习5个意大利语单词<span class="flag-mini"></span></div>
    <div class="top-sub">PAROLE ITALIANE · 5 PAROLE AL GIORNO</div>
  </div>

{cards_js}

  <!-- 5圆点进度条 -->
  <div class="dot-progress" id="dot-progress">
{dots_js}
  </div>

  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  <div class="bottom-brand" id="bottom-brand">
    <img class="brand-logo" src="assets/logo-piano.jpg" alt="涛子办事处">
    <span class="brand-text">涛子办事处 · Ufficio di Taozi</span>
  </div>
  <div class="middle-brand" id="middle-brand">
    <img class="brand-logo" src="assets/logo-piano.jpg" alt="涛子办事处">
    <span class="brand-text">涛子办事处 · Ufficio di Taozi</span>
  </div>
</div>

<audio id="audio" src="{audio_path}" preload="auto"></audio>
<script src="gsap.min.js"></script>
<script>
(function(){{
  var tl = gsap.timeline({{ paused: true }});
  var pf = document.getElementById('progress-fill');
  var audio = document.getElementById('audio');
  var totalDuration = {total_duration:.3f};

{timeline_js}

  // 进度条
  tl.fromTo(pf, {{ width:'0%' }}, {{ width:'100%', duration:totalDuration, ease:'none' }}, 0);

  // 显示标题和logo
  tl.fromTo('#top-header', {{ opacity:0, y:-20 }}, {{ opacity:1, y:0, duration:0.5 }}, 0.2);
  tl.fromTo('#dot-progress', {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.5 }}, 0.3);
  tl.fromTo('#bottom-brand', {{ opacity:0 }}, {{ opacity:1, duration:0.5 }}, 0.5);
  tl.fromTo('#middle-brand', {{ opacity:0 }}, {{ opacity:1, duration:0.5 }}, 0.4);

  // 收尾
  tl.to(['#bottom-brand','#middle-brand','.progress-bar'], {{ opacity:0, duration:0.5 }}, totalDuration - 0.6);

  // 启动
  audio.currentTime = 0;
  audio.play().catch(function(e){{ console.warn('Audio autoplay blocked:', e); }});
  tl.play();

  window.tl = tl;
  window.totalDuration = totalDuration;
}})();
</script>
</body>
</html>"""
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML已生成：{output_path}")
    print(f"   音频时长：{total_duration:.3f}s")
    print(f"   卡片数：{len(words_it)}")


def main():
    parser = argparse.ArgumentParser(description="意大利语5词竖屏教学页面生成器")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--audio", required=True, help="音频文件路径（用于计算时长）")
    parser.add_argument("--words", required=True, help="意大利语单词，逗号分隔")
    parser.add_argument("--zh", required=True, help="中文翻译，逗号分隔")
    parser.add_argument("--en", required=True, help="英文翻译，逗号分隔")
    parser.add_argument("--phonetic", required=True, help="中文谐音，逗号分隔")
    parser.add_argument("--icons", required=True, help="Emoji图标，逗号分隔（用URL编码逗号%2C或分号分隔）")
    args = parser.parse_args()

    words_it = args.words.split(",")
    words_zh = args.zh.split(",")
    words_en = args.en.split(",")
    phonetics = args.phonetic.split(",")
    
    # 处理icons（支持用%2C作为分隔符，因为逗号在emoji中常见）
    if "%2C" in args.icons:
        icons = args.icons.split("%2C")
    else:
        icons = args.icons.split(",")

    if not (len(words_it) == len(words_zh) == len(words_en) == len(phonetics) == len(icons)):
        print("❌ 所有参数必须包含相同数量的单词（5个）")
        sys.exit(1)

    if not os.path.exists(args.audio):
        print(f"❌ 音频文件不存在：{args.audio}")
        sys.exit(1)

    generate_html(words_it, words_zh, words_en, phonetics, icons, args.audio, args.output)


if __name__ == "__main__":
    main()
