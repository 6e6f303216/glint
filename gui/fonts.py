import base64
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import QByteArray, QBuffer, QIODeviceBase
from assets.fonts_data import JETBRAINS_MONO

def load_jetbrains_font(size=16):
    try:
        font_data = base64.b64decode(JETBRAINS_MONO)
        byte_array = QByteArray(font_data)
        buffer = QBuffer(byte_array)
        buffer.open(QIODeviceBase.OpenModeFlag.ReadOnly)

        font_id = QFontDatabase.addApplicationFontFromData(buffer.data())
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return QFont(families[0], size)
    except Exception as e:
        print(f"Font load error: {e}")
    return QFont("Arial", size)
