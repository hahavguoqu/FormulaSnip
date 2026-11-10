# FormulaSnip

**中文** | [English](README.en.md)

Windows 本地截图识别工具：长按右键呼出窗口，框选屏幕内容，把数学公式转换为 LaTeX，把中英文文字转换为可编辑文本，也可混合识别为 Markdown。

基于 PySide6、PaddleOCR 和 PaddlePaddle，使用 CPU 推理。完成首次下载后，识别在本机执行，无需配置云端 API Key。

## 功能

- **公式模式**：数学公式截图转 LaTeX。
- **文字模式**：识别中文、英文，保留基本换行。
- **文字＋公式模式**：检测公式区域，合并文字和公式，按阅读顺序输出 Markdown。
- 截图预览、打开图片、编辑和复制结果、置顶窗口及系统托盘。
- 可调整的右键长按呼出、快捷键及可选登录自启动。
- 模型按需加载；窗口打开期间复用模型，关闭窗口或收起到托盘时释放模型内存。

## 安装

需要 Windows x64、Git 和 [uv](https://docs.astral.sh/uv/)。Python 要求 3.11+，实际依赖版本由 `uv.lock` 锁定。推荐使用本机磁盘上的固定目录。

在 PowerShell 中运行：

```powershell
git clone https://github.com/hahavguoqu/FormulaSnip.git
Set-Location FormulaSnip
$env:UV_CACHE_DIR = "$PWD\.uv-cache"
$env:UV_PYTHON_INSTALL_DIR = "$PWD\runtime"
uv sync --frozen
uv run --frozen python download_models.py
```

首次安装需要联网下载 Python（如需要）、依赖和四个模型。权重由下载脚本从 PaddleX 官方 BOS 地址获取，未包含在仓库中。

| 模型 | 用途 |
| --- | --- |
| `PP-FormulaNet_plus-S` | 公式识别 |
| `PP-OCRv5_mobile_det` | 文字检测 |
| `PP-OCRv5_mobile_rec` | 中英文文字识别 |
| `PP-DocLayout_plus-L` | 混合模式的公式区域定位 |

完成安装后，双击 `Start.vbs` 隐藏控制台启动，或在 PowerShell 中运行：

```powershell
.\Start.ps1
# 或
uv run --frozen python launch.py
```

`uv` 需位于 PATH 中，也可把 `uv.exe` 放入项目的 `tools` 目录。

## 使用

1. 启动软件，选择公式、文字或文字＋公式模式。
2. 点击“截图 / 框选区域”，按住左键拖选，松开后自动识别；也可直接打开图片。
3. 核对并编辑结果，再复制到目标应用。
4. 关闭窗口后，后台右键监听继续运行。原地长按右键约 650 毫秒并松开可再次呼出，时长可在界面调整。

| 操作 | 按键 |
| --- | --- |
| 呼出窗口 | `Ctrl + Alt + L`，或长按右键后松开 |
| 取消任务 | `Ctrl + Alt + Esc` |
| 取消框选 | `Esc` 或右键 |

右键监听读取按键状态，不拦截系统鼠标事件，因此部分应用的原有右键菜单可能同时出现。托盘菜单中的“退出软件”会结束整个程序；之后需要重新启动才能呼出。

## 登录自启动

在项目目录中执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\Enable-Autostart.ps1
# 取消自启动
powershell -ExecutionPolicy Bypass -File .\Enable-Autostart.ps1 -Disable
```

自启动仅在后台监听，呼出窗口后才加载模型。手动后台启动可执行 `wscript.exe .\Start.vbs --background`。注册项指向当前目录，移动目录后需重新设置。为兼容早期版本，自启动注册项名称仍为 `SnipScribe`。

## 性能、数据与限制

- 默认 CPU 推理线程数为 `2`，可通过 `FORMULASNIP_THREADS` 环境变量调整。
- 后台空闲不加载模型；打开窗口时加载所选模式所需模型，连续识别复用进程，切换模式按需增加模型。
- 每次重新打开已关闭的窗口需要重新加载。状态栏耗时只计算推理，整体等待还包括加载、截图和进程通信。
- 关闭窗口释放识别进程；截图期间短暂隐藏窗口会保留模型。取消正在执行的识别或遇到错误时会释放或重建识别进程。
- 截图通过内存和 `temp` 下临时文件传递，正常完成或取消后清理；应用识别流程不会把截图上传到云端。
- 小型行内公式、复杂版式和模糊内容可能识别不全。请核对结果，必要时单独框选公式。
- 模型、配置、缓存、日志和临时文件保存在项目目录，已通过 `.gitignore` 排除出版本控制。

## 开发与验证

Python 命令统一使用 uv。Windows 集成检查使用真实模型，以离屏界面覆盖模型生命周期、三种模式、重复识别、关闭释放、取消和错误恢复：

```powershell
uv run --frozen python tests/check_on_demand.py
```

对本地公式图片测量加载和推理时间：

```powershell
uv run --frozen python benchmark.py "path\to\formula.png"
```

结果写入本地 `data/benchmark.json`。

```text
app.py                  主窗口、托盘、右键监听和识别调度
capture.py              屏幕框选
engine.py               独立识别进程与混合结果排序
env.py                  本地路径、模型与线程设置
download_models.py      官方模型下载
proc_utils.py           Windows 子进程生命周期管理
Start.vbs / Start.ps1   启动入口
tests/                  Windows 集成检查
pyproject.toml / uv.lock 依赖声明与锁定
```

模型及相关依赖的使用条件请参阅 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 和 [PaddleX](https://github.com/PaddlePaddle/PaddleX) 的官方说明。
