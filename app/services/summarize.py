# ai总结功能
from app.config import DEEPSEEK_API_KEY
from openai import OpenAI

def summarize_text(text: str) -> str:
	if not text.strip():
		return ""

	if not DEEPSEEK_API_KEY:
		raise ValueError("未配置 DEEPSEEK_API_KEY")

	client = OpenAI(
		api_key=DEEPSEEK_API_KEY,
		base_url="https://api.deepseek.com",
	)
	response = client.chat.completions.create(
		model="deepseek-chat",
		messages=[
			{
				"role": "system",
				"content": "请用中文准确、简洁地总结用户提供的内容，保留核心观点和重要信息。",
			},
			{"role": "user", "content": text},
		],
	)

	summary = response.choices[0].message.content
	if not summary:
		raise RuntimeError("AI 未返回总结内容")
	return summary.strip()