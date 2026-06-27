# 101 Conversations 数据模型

## conversations.json 结构

```json
{
  "num": 1,                         // 对话编号 (1-101)
  "title": "La chiamata",           // 意大利语标题
  "title_cn": "电话铃声",           // 中文标题
  "file": "Text/index_split_005.html",  // EPUB来源
  "paragraphs": [                   // 意大利语段落数组
    "叙述段落...",
    "角色名:对话内容..."            // 对话行：冒号前为说话人，冒号后为内容
  ],
  "translations": [                 // 中文译文（与paragraphs一一对应）
    "中文译文..."
  ],
  "vocab": [                        // 词汇表
    {"word": "lo squillo", "meaning": "电话铃声 / phone ring"}
  ]
}
```

## audio_para/ 文件格式

文件名: `audio_para/conv_{num}_{pIdx}.json`
```json
{
  "b64": "base64编码的MP3音频数据",
  "voice": "isabella|elsa|diego",
  "speaker": "Matteo|Agostina|...|(空)"
}
```

## vocab_para/ 文件格式

文件名: `vocab_para/vocab_{num}_{idx}.json`
```json
{
  "b64": "base64编码的MP3音频数据",
  "word": "lo squillo",
  "meaning": "电话铃声 / phone ring"
}
```

## 音色分配规则

```python
FEMALE_NAMES = {'Agostina', 'Nina', 'Amalia', 'Teresa', 'Melania', 'Nadia', 'Donna', 'Signora'}
MALE_NAMES = {'Matteo', 'Ignazio', 'Luca', 'Adriano', 'Zamboni', 'Signor', 'Commissario',
              'Perilli', 'Cacace', 'Mancini', 'Ladro', 'Uomo', 'Ufficiale', 'Responsabile', 'Tutti'}

VOICES = {
    'isabella': 'it-IT-IsabellaNeural',   # 旁白/默认 (标准女声)
    'elsa': 'it-IT-ElsaNeural',            # 女性角色 (年长女声)
    'diego': 'it-IT-DiegoNeural',          # 男性角色 (年轻男声)
}
```

## 文件统计

- 101 篇对话 (num 1-101)
- 946 个段落 (平均每篇 ~9.4)
- 426 个词汇
- audio_para/ 目录: 946 个JSON文件
- audio_conv/ 目录: 101个子目录，共946个原始JSON文件
- audio_cache_new/ 目录: 945个MP3缓存文件
- vocab_para/ 目录: ~425个JSON文件
