# 视频分析接口
import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from openai import AuthenticationError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from app.config import DOWNLOAD_DIR
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse, AnalyzeResult, ErrorResponse
from app.services.download import download_video
from app.services.summarize import summarize_text
from app.services.transform import transcribe_video

router = APIRouter(prefix="/v1/analyze", tags=["视频分析接口"])
logger = logging.getLogger(__name__)


def _error_response(status_code: int, message: str) -> JSONResponse:
	response = ErrorResponse(code=status_code, message=message)
	return JSONResponse(status_code=status_code, content=response.model_dump())


def _get_bearer_token(authorization: str | None = Header(default=None)) -> str | None:
	if not authorization:
		return None

	scheme, separator, token = authorization.partition(" ")
	if not separator or scheme.lower() != "bearer" or not token.strip():
		return None
	return token.strip()


@router.post("", response_model=AnalyzeResponse)
def analyze_video(request: AnalyzeRequest, api_key: str | None = Depends(_get_bearer_token)):
	if not api_key:
		return _error_response(HTTP_401_UNAUTHORIZED, "缺少有效的 Bearer API Key")

	filename = f"video_{uuid4().hex}"
	try:
		download_video(request.video_url, filename)
		transcript = transcribe_video(filename)
		if not transcript:
			return _error_response(HTTP_500_INTERNAL_SERVER_ERROR, "未能从视频中识别出语音")
		summary = summarize_text(transcript, api_key=api_key)
		return AnalyzeResponse(data=AnalyzeResult(transcript=transcript, summary=summary))
	except AuthenticationError:
		return _error_response(HTTP_401_UNAUTHORIZED, "API Key 无效")
	except Exception:
		logger.exception("视频分析失败")
		return _error_response(HTTP_500_INTERNAL_SERVER_ERROR, "视频分析失败，请稍后重试")
