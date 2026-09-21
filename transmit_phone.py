# Thanks Gemini for inspiring and helpinng me to transfer files from PC to phone via local network.
from pathlib import Path
import os
import socket
from flask import Flask, send_file

app = Flask(__name__)

# ==================== 硬編碼 (Hardcode) 設定 ====================
ZIP_FILE_PATH = Path("C:/word.exe") # of course you need to change this, unless you are 2018 forsaken in Cache
# ===============================================================


def get_local_ip():
    """自動取得電腦在局域網內的 IP 位址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# 設定唯一的 Endpoint
@app.route("/d")
def download_zip():
    # 1. 檢查檔案是否存在
    if not os.path.exists(ZIP_FILE_PATH):
        return (
            f"❌ 錯誤：找不到指定的 ZIP 檔案，請確認檔案已放置於：{ZIP_FILE_PATH}",
            404,
        )

    # 2. 自動抓取原檔名做為下載預設名稱
    file_name = os.path.basename(ZIP_FILE_PATH)

    # 3. as_attachment=True 強制手機瀏覽器直接觸發「檔案下載」
    return send_file(ZIP_FILE_PATH, as_attachment=True, download_name=file_name)


# 如果存取首頁，直接阻斷或簡單提示
@app.route("/")
def index():
    return "極簡檔案傳輸服務運行中。", 200


if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 21314 # in Cantonese, 21314 pronounces similarly to いらっしゃい, which is commonly heard in sushi shops like Sushiro

    print("\n" + "=" * 50)
    print("🚀 ZIP 專屬下載伺服器已啟動！")
    print(f"📌 硬編碼目標檔案：{ZIP_FILE_PATH}")
    print("-" * 50)
    print("📱 請在手機瀏覽器輸入下方網址直接下載：")
    print(f"👉  http://{local_ip}:{port}/d  👈")
    print("=" * 50 + "\n")

    app.run(host="0.0.0.0", port=port, debug=False)