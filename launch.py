import sys
import traceback
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parent
(root / 'logs').mkdir(exist_ok=True)
with (root / 'logs/startup.log').open('a', encoding='utf-8', buffering=1) as log:
    sys.stdout = log; sys.stderr = log
    print(f'{datetime.now().isoformat()} launch: {sys.argv!r}', file=log)
    try:
        import env
        from app import main
        main()
    except Exception:
        traceback.print_exc(file=log)
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, '启动失败。详情见 D:\\FormulaSnip\\logs\\startup.log', 'FormulaSnip', 0x10)
    finally:
        print(f'{datetime.now().isoformat()} launcher exiting', file=log)
