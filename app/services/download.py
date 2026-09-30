# 视频下载功能
import subprocess
from app.config import COOKIES_PATH, DOWNLOAD_DIR

# 获取函数参数：视频链接
def download_video(url: str, filename: str = "video"):
    if not COOKIES_PATH or not DOWNLOAD_DIR:
        raise RuntimeError("COOKIES_PATH 和 DOWNLOAD_DIR 必须在环境变量中配置")

    # 执行yt-dlp命令，把视频下载到服务器的指定文件夹下（生产环境下）/下载到本地（开发环境下）
    try:
        subprocess.run(
            [
                "yt-dlp",
                "--cookies",
                COOKIES_PATH,
                "-P",
                DOWNLOAD_DIR,
                "-o",
                f"{filename}.%(ext)s",
                url,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("找不到 yt-dlp，请确认已安装并且命令在 PATH 中") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "没有提供错误详情").strip()
        raise RuntimeError(f"视频下载失败：{detail}") from exc