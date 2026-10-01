# 视频分析助手 API 文档 (v1)

## 简介
本文档描述「视频分析助手」的 RESTful API，供前端调用。

- **本地开发 Base URL**: http://127.0.0.1:8000
- **线上环境 Base URL**: https://api.domain.com
- **协议**: HTTPS
- **数据格式**: JSON
- **认证方式**: 请求头 Authorization: Bearer <api_key>

## 通用响应格式

所有接口统一返回以下 JSON 结构：

### 成功
{
  "code": 200,
  "message": "success",
  "data": { }
}

### 失败
{
  "code": 400,
  "message": "错误描述",
  "data": null
}

**状态码说明：**
| code | 含义 |
| :--- | :--- |
| 200 | 请求成功 |
| 400 | 参数校验失败（如视频链接为空） |
| 401 | API Key 无效或未提供 |
| 500 | 服务器内部错误（如视频下载失败） |

---

## 接口列表

### 1. 提交视频分析任务

**功能**：传入 B站视频链接，后端下载音频、转写文本、调用大模型总结，返回总结结果。

**请求**
POST /api/v1/analyze

**请求头 (Headers)**
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| Authorization | string | 是 | Bearer <用户提供的 API Key> |
| Content-Type | string | 是 | application/json |

**请求体 (Body)**
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| video_url | string | 是 | B站视频完整链接，如 https://www.bilibili.com/video/BV1xx... |

**请求示例 (cURL)**
curl -X POST http://127.0.0.1:8000/api/v1/analyze \
  -H "Authorization: Bearer sk-xxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.bilibili.com/video/BV1xx411c7mD"}'

**成功响应示例**
{
  "code": 200,
  "message": "success",
  "data": {
    "transcript": "完整转录文本...",
    "summary": "AI 总结内容..."
  }
}

**成功响应字段说明 (data 内部)**
| 参数名 | 类型 | 说明 |
| :--- | :--- | :--- |
| transcript | string | 视频的完整语音转文字结果 |
| summary | string | AI 生成的视频内容总结 |

**失败响应示例**
{
  "code": 400,
  "message": "视频链接无效或无法访问",
  "data": null
}

---

## 变更日志

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-09-26 | 写MVP的api文档，MVP支持B站视频链接提交并返回AI总结 |