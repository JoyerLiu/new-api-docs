# 邮箱身份验证模块

!!! info "功能说明"
    接口前缀统一为 http(s)://`<your-domain>`

    实现邮箱验证和密码重置功能，集成限流和 Turnstile 防护 。支持自动生成随机密码和邮件模板定制。在用户注册、账户绑定等场景中广泛使用。

## 🔐 无需鉴权

### 发送邮箱验证邮件

- **接口名称**：发送邮箱验证邮件
- **HTTP 方法**：GET
- **路径**：`/api/verification`
- **鉴权要求**：公开 （限流）
- **功能简介**：发送邮箱验证码到指定邮箱地址，用于邮箱绑定或验证操作

💡 请求示例：

```
const response = await fetch(`/api/verification?email=${email}&turnstile=${turnstileToken}`, {  
  method: 'GET',  
  headers: {  
    'Content-Type': 'application/json'  
  }  
});  
const data = await response.json();
```

✅ 成功响应示例：

```
{  
  "success": true,  
  "message": ""  
}
```

❗ 失败响应示例：

```
{  
  "success": false,  
  "message": "无效的参数"  
}
```

🧾 字段说明：

- `email` （字符串）: 接收验证码的邮箱地址，必须是有效的邮箱格式
- `turnstile` （字符串）: Turnstile 验证令牌，用于防止机器人攻击

### 发送重置密码邮件

- **接口名称**：发送重置密码邮件
- **HTTP 方法**：GET
- **路径**：`/api/reset_password`
- **鉴权要求**：公开 （限流）
- **功能简介**：向已注册邮箱发送密码重置链接，用于用户找回密码

💡 请求示例：

```
const response = await fetch(`/api/reset_password?email=${email}&turnstile=${turnstileToken}`, {  
  method: 'GET',  
  headers: {  
    'Content-Type': 'application/json'  
  }  
});  
const data = await response.json();
```

✅ 成功响应示例：

```
{  
  "success": true,  
  "message": ""  
}
```

❗ 失败响应示例：

```
{  
  "success": false,  
  "message": "该邮箱地址未注册"  
}
```

🧾 字段说明：

- `email` （字符串）: 需要重置密码的邮箱地址，必须是已注册的邮箱
- `turnstile` （字符串）: Turnstile 验证令牌，用于防止恶意请求

### 提交重置密码请求

- **接口名称**：提交重置密码请求
- **HTTP 方法**：POST
- **路径**：`/api/user/reset`
- **鉴权要求**：公开
- **功能简介**：通过邮件中的重置链接完成密码重置，系统会生成新密码并返回

💡 请求示例：

```
const response = await fetch('/api/user/reset', {  
  method: 'POST',  
  headers: {  
    'Content-Type': 'application/json'  
  },  
  body: JSON.stringify({  
    email: "user@example.com",  
    token: "verification_token_from_email"  
  })  
});  
const data = await response.json();
```

✅ 成功响应示例：

```
{  
  "success": true,  
  "message": "",  
  "data": "newPassword123"  
}
```

❗ 失败响应示例：

```
{  
  "success": false,  
  "message": "重置链接非法或已过期"  
}
```

🧾 字段说明：

- `email` （字符串）: 要重置密码的邮箱地址
- `token` （字符串）: 从重置邮件中获取的验证令牌
- `data` （字符串）: 成功时返回的新密码，系统自动生成 12 位随机密码 

