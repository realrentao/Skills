---
name: stable-diffusion-image-generation
description: Stable Diffusion 图像生成 — 基于 HuggingFace Diffusers 库，支持文生图、图生图、Inpainting、ControlNet、LoRA 等。触发词：Stable Diffusion、SD生图、AI绘图、文生图、图生图、inpaint、SDXL、Flux、ControlNet。
version: 1.0.0
---

# Stable Diffusion Image Generation

基于 HuggingFace Diffusers 的 Stable Diffusion 全功能图像生成技能。支持从 SD 1.5 到 Flux 全系列模型。

## 环境准备

### 安装依赖

```bash
# 创建独立 Python 环境（推荐 3.10）
python -m venv sd_env
# Windows:
sd_env\Scripts\activate
# Linux/Mac:
source sd_env/bin/activate

# 安装 PyTorch（CUDA 12.1）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 安装核心库
pip install diffusers transformers accelerate safetensors
pip install xformers --index-url https://download.pytorch.org/whl/cu121  # 可选，内存优化
pip install pillow numpy
pip install controlnet_aux  # ControlNet 需要
```

### 权限检查

每张可用的 NVIDIA GPU 及其 VRAM：

```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}'); print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem/1e9:.1f}GB' if torch.cuda.is_available() else '')"
```

## 模型选择指南

| 模型 | VRAM 需求 | HuggingFace ID | 适合 |
|------|----------|---------------|------|
| SD 1.5 | 4GB | `runwayml/stable-diffusion-v1-5` | 通用、快速 |
| SD 2.1 | 4GB | `stabilityai/stable-diffusion-2-1` | 高分辨率 |
| SDXL | 8GB | `stabilityai/stable-diffusion-xl-base-1.0` | 高画质 |
| SD 3.0 Medium | 8GB+ | `stabilityai/stable-diffusion-3-medium-diffusers` | 最新架构 |
| Flux.1 Schnell | 8GB+ | `black-forest-labs/FLUX.1-schnell` | 4步快速生成 |
| Flux.1 Dev | 16GB+ | `black-forest-labs/FLUX.1-dev` | 最高质量 |

**国内用户**：通过 HF 镜像加速下载：
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

## 核心生成模式

### 1. 文生图 (Text-to-Image)

```python
import torch
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    safety_checker=None,  # 跳过安全过滤器（可选）
)
pipe = pipe.to("cuda")

# 启用内存优化
pipe.enable_xformers_memory_efficient_attention()
# 或 pipe.enable_attention_slicing()  # 如果 xformers 不可用

# 生成
prompt = "a serene lake at sunset, mountains in background, photorealistic"
negative_prompt = "blurry, low quality, distorted, watermark"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=25,
    guidance_scale=7.5,
    width=512,
    height=512,
).images[0]

image.save("output.png")
```

### 2. SDXL 文生图

```python
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
)
pipe = pipe.to("cuda")

image = pipe(
    prompt="cinematic photo of a cat astronaut in space, highly detailed, 8k",
    negative_prompt="blurry, low quality",
    num_inference_steps=30,
    guidance_scale=7.5,
    height=1024,
    width=1024,
).images[0]
```

### 3. 图生图 (Image-to-Image)

```python
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

init_image = Image.open("input.jpg").convert("RGB").resize((512, 512))

image = pipe(
    prompt="oil painting style, van gogh",
    image=init_image,
    strength=0.75,  # 0=保持原图, 1=完全重绘。推荐 0.5-0.8
    num_inference_steps=30,
).images[0]
```

**strength 参数速查**：
- `0.3-0.5`：轻微风格化
- `0.5-0.7`：明显风格转换
- `0.7-0.9`：大幅变化，保留构图
- `0.9-1.0`：几乎重新生成

### 4. Inpainting（遮罩修复）

```python
from diffusers import StableDiffusionInpaintPipeline

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

image = Image.open("original.jpg").resize((512, 512))
mask = Image.open("mask.png").convert("RGB").resize((512, 512))
# mask: 白色区域 = 需要重绘的部分

result = pipe(
    prompt="a beautiful garden",
    image=image,
    mask_image=mask,
    num_inference_steps=25,
).images[0]
```

### 5. ControlNet（精确控制）

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
import cv2
import numpy as np
from PIL import Image

# 加载 ControlNet（Canny 边缘检测）
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16,
)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# 准备控制图像
input_image = load_image("reference.jpg")
img = cv2.Canny(np.array(input_image), 100, 200)
canny_image = Image.fromarray(img)

result = pipe(
    prompt="futuristic cityscape",
    image=canny_image,
    num_inference_steps=20,
).images[0]
```

**常用 ControlNet 模型**：

| 用途 | HuggingFace ID |
|------|---------------|
| 边缘检测 | `lllyasviel/sd-controlnet-canny` |
| 姿态控制 | `lllyasviel/sd-controlnet-openpose` |
| 深度图 | `lllyasviel/sd-controlnet-depth` |
| 线稿上色 | `lllyasviel/sd-controlnet-scribble` |
| 语义分割 | `lllyasviel/sd-controlnet-seg` |
| 法线贴图 | `lllyasviel/sd-controlnet-normal` |
| 涂鸦引导 | `lllyasviel/sd-controlnet-mlsd` |

### 6. LoRA 适配器

```python
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

# 加载 LoRA 权重
pipe.load_lora_weights("path/to/lora/weights", weight_name="lora.safetensors")

# 可调节 LoRA 强度
pipe.fuse_lora(lora_scale=0.8)

image = pipe("beautiful landscape, oil painting style").images[0]

# 卸载 LoRA 恢复原模型
pipe.unfuse_lora()
```

## 内存优化策略

根据 GPU VRAM 选择：

| VRAM | 策略 |
|------|------|
| 4GB | CPU offloading + attention slicing |
| 6GB | xFormers + attention slicing |
| 8GB | xFormers（SDXL 可跑） |
| 16GB+ | 无需优化（Flux Dev 可跑） |

### CPU Offloading（最低显存）

```python
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
)
pipe.enable_model_cpu_offload()  # 自动切换 CPU/GPU
# 不需要 pipe.to("cuda")
```

## 批量生成

```python
for i, seed in enumerate([42, 123, 456, 789]):
    generator = torch.Generator("cuda").manual_seed(seed)
    image = pipe(
        prompt=prompt,
        generator=generator,
        num_inference_steps=25,
    ).images[0]
    image.save(f"output_{i}_{seed}.png")
```

## 工作流程

1. **确认需求**：用户想生成什么？（文生图/图生图/inpainting/ControlNet）
2. **检查 GPU**：运行权限检查脚本
3. **选择模型**：根据 VRAM 和画质需求推荐
4. **生成图像**：运行对应代码
5. **保存输出**：PNG 格式保存到工作目录

## 常见问题

- **CUDA out of memory**：减小分辨率或启用 CPU offloading
- **国内下载慢**：设置 `HF_ENDPOINT=https://hf-mirror.com`
- **生成质量差**：增加 inference steps（25-50）或调整 guidance scale（5-12）
- **人物畸形**：添加 negative prompt "bad anatomy, extra limbs, distorted face"
