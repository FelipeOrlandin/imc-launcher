import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, 'src')
if not os.path.exists(src_path):
    src_path = base_path

if src_path not in sys.path:
    sys.path.insert(0, src_path)

from main import main
main()