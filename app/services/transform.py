from functools import lru_cache
from pathlib import Path

from faster_whisper import WhisperModel


TEMP_DIR = Path(__file__).resolve().parents[2] / "temp"


@lru_cache(maxsize=1)
def _get_model() -> WhisperModel:
	return WhisperModel("base", device="cpu", compute_type="int8")


def transcribe_video(filename: str) -> str:
	video_path = TEMP_DIR / f"{filename}"

	if not video_path.is_file():
		matches = sorted(
			path for path in TEMP_DIR.glob(f"{filename}.*")
			if path.is_file() and path.name.startswith(f"{filename}.")
		)
		if not matches:
			raise FileNotFoundError(f"在 {TEMP_DIR} 中找不到视频文件：{filename}")
		video_path = matches[0]

	segments, _ = _get_model().transcribe(str(video_path))
	return "".join(segment.text for segment in segments).strip()