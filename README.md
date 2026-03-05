项目介绍
feishu-openapi 是一个用于直接调用飞书开放平台 API 的技能模块。它提供了安全、便捷的方式来与飞书开放平台进行通信，并处理各种 API 响应和错误情况。

功能特性
核心功能
通用 API 调用：支持 GET、POST、PUT、DELETE 等 HTTP 请求方法
自动访问令牌管理：可以直接传入访问令牌，或通过应用凭证自动获取
响应处理：标准化响应格式，包含成功状态、状态码、数据和错误信息
错误处理：详细的错误信息解析和友好的错误提示
安全传输：使用 HTTPS 进行 API 通信，敏感信息安全处理
主要优点
简化了与飞书开放平台的交互流程
提供了统一的 API 调用接口
自动处理访问令牌的获取和管理
详细的错误处理和调试信息
支持多种认证方式
安装与配置
前置要求
Python 3.6 或更高版本
requests 库（用于 HTTP 请求）
安装方法
bash
复制
# 安装 requests 库
pip install requests

# 获取技能文件（复制以下文件到技能目录）
# - __init__.py
# - MANIFEST.json
# - SKILL.md
# - tool.py
技能目录结构
text
复制
feishu-openapi/
├── __init__.py       # 模块初始化文件，暴露公共接口
├── MANIFEST.json     # 技能清单文件，包含技能元数据和依赖信息
├── README.md         # 项目说明文档（此文件）
├── SKILL.md          # 技能使用文档，详细说明了功能、使用场景、工具方法
└── tool.py           # 实现文件，包含核心的 API 调用功能和错误处理逻辑
使用方法
基础使用
1. 直接导入模块
python
复制
from skills.feishu-openapi import feishu_openapi_call
2. 调用 API 方法
python
复制
# 获取应用访问凭证
result = feishu_openapi_call(
    method='POST',
    api_path='/auth/v3/tenant_access_token/internal',
    app_id='your_app_id',
    app_secret='your_app_secret'
)

if result['success']:
    print('获取访问凭证成功')
    print(f"Token: {result['data']['tenant_access_token']}")
    print(f"有效期: {result['data']['expire']} 秒")
else:
    print(f"获取访问凭证失败: {result['error']}")
3. 使用访问令牌调用其他 API
python
复制
# 先获取访问凭证
token_result = feishu_openapi_call(
    method='POST',
    api_path='/auth/v3/tenant_access_token/internal',
    app_id='your_app_id',
    app_secret='your_app_secret'
)

if token_result['success']:
    access_token = token_result['data']['tenant_access_token']
    
    # 调用获取用户信息 API
    user_result = feishu_openapi_call(
        method='GET',
        api_path='/contact/v3/users/batch_get_id',
        access_token=access_token,
        query_params={'mobiles': '["13800138000"]'}
    )
    
    if user_result['success']:
        print('获取用户信息成功')
        print(f"用户信息: {user_result['data']}")
    else:
        print(f"获取用户信息失败: {user_result['error']}")
4. 发送 JSON 数据的 POST 请求
python
复制
token_result = feishu_openapi_call(
    method='POST',
    api_path='/auth/v3/tenant_access_token/internal',
    app_id='your_app_id',
    app_secret='your_app_secret'
)

if token_result['success']:
    access_token = token_result['data']['tenant_access_token']
    
    # 发送消息到群聊
    send_result = feishu_openapi_call(
        method='POST',
        api_path='/im/v1/messages',
        access_token=access_token,
        json_data={
            "receive_id": "oc_xxxxxx",
            "msg_type": "text",
            "content": '{"text": "这是一条测试消息"}'
        },
        query_params={"receive_id_type": "open_id"}
    )
    
    if send_result['success']:
        print('消息发送成功')
        print(f"消息 ID: {send_result['data']['message_id']}")
    else:
        print(f"消息发送失败: {send_result['error']}")
参数说明
feishu_openapi_call 函数参数
参数名	类型	描述	必填
method	str	HTTP 请求方法（GET/POST/PUT/DELETE）	是
api_path	str	飞书开放平台 API 路径（如 /auth/v3/tenant_access_token/internal）	是
access_token	str	访问令牌（可选，不提供时会尝试获取）	否
app_id	str	应用 ID（可选，用于获取应用访问凭证）	否
app_secret	str	应用密钥（可选，用于获取应用访问凭证）	否
json_data	dict	请求的 JSON 数据（可选）	否
query_params	dict	查询参数（可选）	否
返回值说明
python
复制
{
    "success": True,              # 调用是否成功
    "status_code": 200,           # HTTP 状态码
    "data": {},                   # API 响应数据（解析后的 JSON）
    "error": None                 # 错误信息（如果有）
}
支持的 API 接口
该技能支持调用飞书开放平台的所有 API，例如：

认证接口
/auth/v3/tenant_access_token/internal - 获取应用访问凭证
/auth/v3/user_access_token/internal - 获取用户访问凭证
通讯录接口
/contact/v3/users/batch_get_id - 通过手机号获取用户 ID
/contact/v3/users/get - 获取用户信息
/contact/v3/departments/list - 获取部门列表
即时通讯接口
/im/v1/messages - 发送消息
/im/v1/messages/{message_id} - 获取消息详情
/im/v1/chat/members - 获取群成员列表
日历接口
/calendar/v4/calendars - 获取用户日历列表
/calendar/v4/events - 获取日历事件列表
文件接口
/drive/v1/files - 上传文件
/drive/v1/files/{file_token} - 下载文件
错误处理
常见错误类型
1. 认证错误
python
复制
{
    "success": False,
    "error": "需要提供 access_token 或 app_id + app_secret"
}
解决方案： 确保提供了有效的访问令牌或应用凭证

2. API 错误
python
复制
{
    "success": False,
    "status_code": 400,
    "error": "Code: 10013, 消息: 用户不存在"
}
解决方案： 根据错误码和消息调整请求参数

3. 网络错误
python
复制
{
    "success": False,
    "error": "请求失败: [Errno -2] Name or service not known"
}
解决方案： 检查网络连接或飞书开放平台服务状态

4. 超时错误
python
复制
{
    "success": False,
    "error": "请求失败: HTTPSConnectionPool(host='open.feishu.cn', port=443): Read timed out. (read timeout=30)"
}
解决方案： 检查网络状况，或考虑优化请求

最佳实践
1. 访问凭证管理
python
复制
# 存储访问凭证的方式（示例）
class TokenManager:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token_info = None
        
    def get_access_token(self):
        if self.token_info:
            # 检查令牌是否即将过期
            if time.time() < self.token_info['expire_time'] - 60:
                return self.token_info['token']
                
        # 获取新的访问凭证
        result = feishu_openapi_call(
            method='POST',
            api_path='/auth/v3/tenant_access_token/internal',
            app_id=self.app_id,
            app_secret=self.app_secret
        )
        
        if result['success']:
            self.token_info = {
                'token': result['data']['tenant_access_token'],
                'expire_time': time.time() + result['data']['expire']
            }
            return self.token_info['token']
            
        return None
2. 重试机制
python
复制
def retry_api_call(func, max_retries=3, delay=1):
    """带有重试机制的 API 调用"""
    for i in range(max_retries):
        try:
            result = func()
            if result['success']:
                return result
            print(f"API 调用失败 (尝试 {i+1}/{max_retries}): {result['error']}")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            print(f"API 调用异常 (尝试 {i+1}/{max_retries}): {str(e)}")
            time.sleep(delay)
            delay *= 2
            
    return None
3. 日志记录
python
复制
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_api_call(api_path, success, status_code, error=None):
    """记录 API 调用日志"""
    log_msg = f"API 调用: {api_path}"
    log_msg += f" 成功: {success}"
    log_msg += f" 状态码: {status_code}"
    if error:
        log_msg += f" 错误: {error}"
        
    if success:
        logger.info(log_msg)
    else:
        logger.error(log_msg)
API 参考
技能方法
feishu_openapi_call
python
复制
def feishu_openapi_call(
    method: str,
    api_path: str,
    access_token: Optional[str] = None,
    app_id: Optional[str] = None,
    app_secret: Optional[str] = None,
    json_data: Optional[Dict] = None,
    query_params: Optional[Dict] = None
) -> Dict:
功能描述： 调用飞书开放平台 API 的通用方法

参数说明：

参数名	类型	描述
method	str	HTTP 请求方法（GET/POST/PUT/DELETE）
api_path	str	API 路径（如 /auth/v3/tenant_access_token/internal）
access_token	str	访问令牌（可选，不提供时会尝试获取）
app_id	str	应用 ID（可选，用于获取应用访问凭证）
app_secret	str	应用密钥（可选，用于获取应用访问凭证）
json_data	dict	请求的 JSON 数据（可选）
query_params	dict	查询参数（可选）
返回值：

python
复制
{
    "success": bool,              # 调用是否成功
    "status_code": int,           # HTTP 状态码
    "data": dict,                 # API 响应数据（解析后的 JSON）
    "error": str                  # 错误信息（如果有）
}
常见问题
Q1: 如何获取应用 ID 和密钥？
登录飞书开放平台 (https://open.feishu.cn)
创建应用或选择已有的应用
在应用管理页面找到 "凭证与基础信息" 部分
可以找到 App ID 和 App Secret
Q2: 访问凭证的有效期是多久？
Tenant Access Token: 通常为 2 小时
User Access Token: 通常为 1 天
建议在使用过程中定期检查访问凭证的有效期。

Q3: API 调用失败时如何排查问题？
检查参数是否正确
检查访问凭证是否有效
查看详细的错误信息
确认网络连接正常
检查 API 权限是否已开启
Q4: 如何提高 API 调用的成功率？
实现访问凭证的缓存和自动刷新
添加重试机制
优化请求参数
监控 API 调用频率
安全说明
敏感信息处理
App ID 和 App Secret：这些信息非常敏感，不应在代码中硬编码或公开分享
Access Token：访问令牌具有较高的权限，应妥善保管
API 响应：包含用户信息的响应应谨慎处理
最佳安全实践
不在代码中硬编码敏感信息
使用环境变量或配置文件存储敏感信息
限制访问凭证的权限范围
定期轮换访问凭证
使用 HTTPS 进行 API 通信
更新日志
版本 1.0.0 (2026-03-06)
初版发布
实现了基础的 API 调用功能
支持通过应用凭证自动获取访问令牌
详细的错误处理和响应解析
安全的 API 通信方式
技术支持
获取帮助
查看 SKILL.md 文件获取详细的技能使用文档
检查 tool.py 文件中的实现细节和错误处理逻辑
在使用过程中遇到问题，可以通过以下方式寻求帮助：
查看飞书开放平台官方文档：https://open.feishu.cn/document/
参考技能使用文档中的示例代码
在相关技术社区提问和交流
贡献与反馈
如果您在使用过程中发现了任何问题或有改进建议，欢迎：

提交 Issue 描述问题
发送反馈信息
提供改进建议
许可证
本项目采用 MIT 许可证，详细信息请参见 LICENSE 文件。

注意： 使用本技能时，需要遵守飞书开放平台的使用条款和隐私政策。
