# FormulaSnip

[中文](README.md) | **English**

A local screenshot recognition utility for Windows. Hold and release the right mouse button to open the panel, select a screen region, and convert equations to LaTeX, Chinese/English text to editable text, or mixed content to Markdown.

Built with PySide6, PaddleOCR, and PaddlePaddle, using CPU inference. Recognition runs locally after the initial downloads and requires no cloud API key.

## Features

- **Formula mode:** convert equation screenshots to LaTeX.
- **Text mode:** recognize Chinese and English with basic line breaks.
- **Mixed mode:** locate formulas, recognize text and equations, and combine them into Markdown in reading order.
- Screenshot preview, image import, editable results, copy, an always-on-top panel, and a system tray.
- Configurable right-button hold, keyboard shortcuts, and optional startup at sign-in.
- On-demand models: reuse loaded models while the panel is open and release them when it closes or returns to the tray.

## Installation

Requires Windows x64, Git, and [uv](https://docs.astral.sh/uv/). The project requires Python 3.11+; dependency versions are pinned in `uv.lock`. Use a stable directory on a local disk.

Run in PowerShell:

```powershell
git clone https://github.com/hahavguoqu/FormulaSnip.git
Set-Location FormulaSnip
$env:UV_CACHE_DIR = "$PWD\.uv-cache"
$env:UV_PYTHON_INSTALL_DIR = "$PWD\runtime"
uv sync --frozen
uv run --frozen python download_models.py
```

Initial setup downloads Python if needed, dependencies, and four models. The download script obtains weights from PaddleX's official BOS host. Weights are excluded from this repository.

| Model | Purpose |
| --- | --- |
| `PP-FormulaNet_plus-S` | Formula recognition |
| `PP-OCRv5_mobile_det` | Text detection |
| `PP-OCRv5_mobile_rec` | Chinese/English text recognition |
| `PP-DocLayout_plus-L` | Formula-region detection in mixed mode |

After setup, double-click `Start.vbs` to launch without a console, or run:

```powershell
.\Start.ps1
# Alternatively
uv run --frozen python launch.py
```

Make `uv` available on PATH, or place `uv.exe` in the project's `tools` directory.

## Usage

1. Start the application and choose formula, text, or mixed mode.
2. Click the capture button and drag with the left mouse button. Recognition begins when you release it. You can also open an image file.
3. Review, edit, and copy the result.
4. Closing the panel leaves the background wake listener active. Hold the right mouse button in place for about 650 ms, then release it to reopen. The duration is configurable.

| Action | Shortcut |
| --- | --- |
| Open panel | `Ctrl + Alt + L`, or hold and release the right mouse button |
| Cancel task | `Ctrl + Alt + Esc` |
| Cancel region selection | `Esc` or right-click |

The right-button listener reads button state without blocking system mouse events, so another application's context menu may appear as well. Selecting Exit from the tray menu stops the whole program; launch it again to re-enable the listener.

## Start at sign-in

Run from the project directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\Enable-Autostart.ps1
# Disable
powershell -ExecutionPolicy Bypass -File .\Enable-Autostart.ps1 -Disable
```

Startup keeps only the wake listener active; models load when the panel opens. For a manual background launch, run `wscript.exe .\Start.vbs --background`. The registration points to the current directory, so reconfigure it after moving the project. The registry value retains the earlier name `SnipScribe` for compatibility.

## Performance, data, and limitations

- CPU inference uses `2` threads by default. Override with the `FORMULASNIP_THREADS` environment variable.
- No models load while idle in background mode. Opening the panel loads the selected mode, repeated recognition reuses the process, and switching modes loads additional models as needed.
- Reopening a closed panel reloads models. The status timer measures inference only; total latency also includes loading, capture, and interprocess communication.
- Closing the panel releases the recognition process. Temporary hiding for capture retains it. Cancelling active recognition or encountering errors releases or rebuilds the recognition process.
- Screenshots pass through memory and temporary files under `temp`, which are cleaned after normal completion or cancellation. The application's recognition flow does not upload screenshots to a cloud service.
- Small inline equations, complex layouts, and blurry inputs can be missed. Review results and capture individual formulas when necessary.
- Models, settings, caches, logs, and temporary files stay under the project directory and are excluded by `.gitignore`.

## Development and verification

Use uv for Python commands. The Windows integration check uses real models with an offscreen UI to exercise model lifecycle, all three modes, repeated recognition, release on close, cancellation, and error recovery:

```powershell
uv run --frozen python tests/check_on_demand.py
```

Benchmark loading and inference on a local formula image:

```powershell
uv run --frozen python benchmark.py "path\to\formula.png"
```

The report is saved locally to `data/benchmark.json`.

```text
app.py                  Main panel, tray, wake listener, scheduling
capture.py              Screen-region selection
engine.py               Recognition process and mixed-content ordering
env.py                  Local paths, model setup, thread settings
download_models.py      Official model downloads
proc_utils.py           Windows child-process lifecycle management
Start.vbs / Start.ps1   Launchers
tests/                  Windows integration check
pyproject.toml / uv.lock Dependency definitions and lockfile
```

See [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) and [PaddleX](https://github.com/PaddlePaddle/PaddleX) for the terms applicable to their models and dependencies.
