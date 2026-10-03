# 视频分析接口——请求与响应模型
from urllib.parse import urlsplit

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
	video_url: str = Field(min_length=1)

	@field_validator("video_url")
	@classmethod
	def validate_video_url(cls, value: str) -> str:
		parsed_url = urlsplit(value)
		host = (parsed_url.hostname or "").lower()
		is_bilibili_host = (
			host == "bilibili.com"
			or host.endswith(".bilibili.com")
			or host == "b23.tv"
		)
		if parsed_url.scheme not in {"http", "https"} or not is_bilibili_host:
			raise ValueError("video_url 必须是有效的 B 站视频链接")
		return value


class AnalyzeResult(BaseModel):
	transcript: str
	summary: str


class AnalyzeResponse(BaseModel):
	code: int = 200
	message: str = "success"
	data: AnalyzeResult


class ErrorResponse(BaseModel):
	code: int
	message: str
	data: None = None