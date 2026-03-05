功能概述
提供飞书开放平台 API 的通用调用接口，支持发送 HTTP 请求、处理响应数据和管理应用授权。

使用场景
适用于需要直接调用飞书开放平台 API 的场景，包括：

获取应用访问凭证
调用飞书各业务接口（通讯录、IM、日历、云文档等）
处理飞书 API 的响应和错误
工具方法
feishu_openapi_call
通用的飞书开放平台 API 调用工具。

参数：

method: HTTP 请求方法（GET/POST/PUT/DELETE）
api_path: 飞书开放平台 API 路径
access_token: 访问令牌（可选）
app_id: 应用 ID（可选，用于获取应用访问凭证）
app_secret: 应用密钥（可选，用于获取应用访问凭证）
json_data: 请求的 JSON 数据（可选）
query_params: 查询参数（可选）
返回：

success: 调用是否成功
status_code: HTTP 状态码
data: API 响应数据（解析后的 JSON）
error: 错误信息（如果有）
安全说明
敏感信息（如 app_secret）会进行安全处理
API 调用会记录必要的日志，但不暴露敏感数据
支持获取企业自建应用的 access_token 和 tenant_access_token
示例使用
# 调用获取应用访问凭证
result = feishu_openapi_call(
    method='POST',
    api_path='/auth/v3/tenant_access_token/internal',
    app_id='your_app_id',
    app_secret='your_app_secret'
)

# 调用获取用户信息
result = feishu_openapi_call(
    method='GET',
    api_path='/contact/v3/users/batch_get_id',
    access_token='your_access_token',
    query_params={'mobiles': '["13800138000"]'}
)

依赖说明
需要 Python 3.6+ 版本
需要安装 requests 库：pip install requests
权限说明
使用本技能需要以下权限：

网络访问权限（用于发送 API 请求）
文件读取权限（用于读取配置文件）
