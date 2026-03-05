#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书开放平台 API 调用工具
"""

import json
import requests
import time
from typing import Dict, Any, Optional
import hashlib

def feishu_openapi_call(method: str, 
                       api_path: str, 
                       access_token: Optional[str] = None,
                       app_id: Optional[str] = None,
                       app_secret: Optional[str] = None,
                       json_data: Optional[Dict] = None,
                       query_params: Optional[Dict] = None) -> Dict:
    """
    调用飞书开放平台 API

    Args:
        method: HTTP 请求方法 (GET/POST/PUT/DELETE)
        api_path: API 路径 (如 /auth/v3/tenant_access_token/internal)
        access_token: 访问令牌 (可选)
        app_id: 应用 ID (可选，用于获取访问凭证)
        app_secret: 应用密钥 (可选，用于获取访问凭证)
        json_data: 请求的 JSON 数据 (可选)
        query_params: 查询参数 (可选)

    Returns:
        包含调用结果的字典
    """
    
    base_url = "https://open.feishu.cn/open-apis"
    url = f"{base_url}{api_path}"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    elif app_id and app_secret:
        token_result = _get_tenant_access_token(app_id, app_secret)
        if not token_result["success"]:
            return token_result
        access_token = token_result["data"]["tenant_access_token"]
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        return {
            "success": False,
            "error": "需要提供 access_token 或 app_id + app_secret"
        }
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, 
                                  headers=headers, 
                                  params=query_params,
                                  timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, 
                                   headers=headers, 
                                   params=query_params,
                                   json=json_data,
                                   timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, 
                                  headers=headers, 
                                  params=query_params,
                                  json=json_data,
                                  timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, 
                                     headers=headers, 
                                     params=query_params,
                                     timeout=30)
        else:
            return {
                "success": False,
                "error": f"不支持的 HTTP 方法: {method}"
            }
        
        response_json = response.json()
        
        return {
            "success": response.status_code == 200 and response_json.get("code") == 0,
            "status_code": response.status_code,
            "data": response_json,
            "error": _parse_feishu_error(response_json) if response_json.get("code") != 0 else None
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"响应解析失败: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误: {str(e)}"
        }

def _get_tenant_access_token(app_id: str, app_secret: str) -> Dict:
    """
    获取应用访问凭证 (tenant_access_token)
    """
    try:
        response = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={
                "app_id": app_id,
                "app_secret": app_secret
            },
            timeout=30
        )
        
        response_json = response.json()
        
        if response.status_code == 200 and response_json.get("code") == 0:
            return {
                "success": True,
                "data": response_json.get("tenant_access_token"),
                "expire": response_json.get("expire")
            }
        else:
            return {
                "success": False,
                "error": f"获取访问凭证失败: {_parse_feishu_error(response_json)}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"获取访问凭证失败: {str(e)}"
        }

def _parse_feishu_error(response_json: Dict) -> str:
    """
    解析飞书 API 的错误信息
    """
    code = response_json.get("code", -1)
    msg = response_json.get("msg", "未知错误")
    return f"Code: {code}, 消息: {msg}"

def tool(func):
    import inspect
    sig = inspect.signature(func)
    params = []
    for name, param in sig.parameters.items():
        params.append({
            "name": name,
            "type": str(param.annotation) if param.annotation != inspect._empty else "string",
            "description": "",
            "required": param.default == inspect._empty
        })
    
    return func

@tool
def feishu_openapi_call_tool(
        method: str = "GET",
        api_path: str = "",
        access_token: str = "",
        app_id: str = "",
        app_secret: str = "",
        json_data: str = "{}",
        query_params: str = "{}"
):
    """
    飞书开放平台 API 调用工具（供外部使用）
    """
    
    try:
        if json_data:
            parsed_json = json.loads(json_data)
        else:
            parsed_json = None
            
        if query_params:
            parsed_query = json.loads(query_params)
        else:
            parsed_query = None
            
        result = feishu_openapi_call(
            method=method,
            api_path=api_path,
            access_token=access_token if access_token else None,
            app_id=app_id if app_id else None,
            app_secret=app_secret if app_secret else None,
            json_data=parsed_json,
            query_params=parsed_query
        )
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "error": f"JSON 解析失败: {str(e)}"
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"执行失败: {str(e)}"
        }, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("python tool.py <api_path> [method] [json_data]")
        print()
        print("示例:")
        print("python tool.py /auth/v3/tenant_access_token/internal POST '{\"app_id\": \"xxx\", \"app_secret\": \"xxx\"}'")
        sys.exit(1)
        
    api_path = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "GET"
    json_data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    
    print("调用 API...")
    result = feishu_openapi_call(
        method=method,
        api_path=api_path,
        json_data=json_data
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
