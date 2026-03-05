#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
飞书开放平台 API 调用技能

提供飞书开放平台 API 的通用调用接口，支持发送 HTTP 请求到飞书开放平台，
处理飞书 API 的响应数据，以及管理飞书应用的授权和凭证。
"""

from .tool import feishu_openapi_call, feishu_openapi_call_tool

__version__ = "1.0.0"
__description__ = "飞书开放平台 API 调用技能"
__author__ = "OpenClaw"

__all__ = [
    "feishu_openapi_call",
    "feishu_openapi_call_tool"
]
