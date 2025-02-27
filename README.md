# Flask QuickStart

这是一个基于 Flask 的后端项目，提供基础的用户身份验证和 CRUD（创建、读取、更新、删除）功能。

## 目录结构

```
app/
├── api/              # API 蓝图和路由定义
├── commands/         # 自定义命令
├── config/           # 配置文件目录
├── dao/              # 数据访问对象
├── extensions/       # 扩展模块
├── models/           # 数据模型 数据库ORM映射
├── services/         # 服务层
├── templates/        # 模板文件
├── utils/            # 工具函数
├── validators/       # 数据验证
├── views/            # 视图函数
├── __init__.py       # 应用初始化
debug_starter/        # 开发服务器
log/                  # 日志文件目录
web.py                # 应用入口
```

## 系统要求

- Python 3.6+
- MySQL 5.7+
- Memcached (可选)

## 安装步骤

### 1. 克隆项目

```bash
git clone <仓库地址>
cd wjwx-backend
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 设置数据库

1. 创建数据库

```bash
mysql -u root -p
CREATE DATABASE flaskstudy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit
```

2. 导入 SQL 文件

```bash
mysql -u root -p flaskstudy < flaskstudy.sql
```


## 启动项目

环境变量 FLASK_ENV 决定导入的配置文件`app/config/`
- development 导入 development.py 开发用
- production 导入 production.py 生产用

### 开发环境

- 设置环境变量
```shell
# linux
FLASK_APP=debug_starter/web.py 
FLASK_ENV=development

# powershell
$env:FLASK_APP="./debug_starter/web.py"
$env:FLASK_ENV="development"
```

开发环境会导入`app/config/development.py` 配置文件。如果需要，可以根据您的环境修改数据库连接信息和其他配置项。

- 启动
```shell
flask run
```
服务将在 `http://127.0.0.1:5000` 上运行。

- 查看是否启动成功
```shell
http://127.0.0.1:5000/api/v1/test/
```


### 部署环境
部署环境下，请使用 FLASK_ENV=production 并配置相应的`app/config/production.py`
```shell
gunicorn -b 0.0.0.0:8001 uwsgi.web:application

```
## API 使用指南

### 用户认证

#### 登录

```
POST http://127.0.0.1:5000/api/v1/auth/login
```

请求体:
```json
{
  "account":"12345678",
  "secret":"12345678"
}
```

响应:
```json
{
    "data": {
        "access_token": "xx...",
        "refresh_token": "xx..."
    },
    "error_code": 0,
    "msg": "ok",
    "request": "POST /api/v1/auth/login"
}
```

登录后，将返回的 token 添加到后续请求的 authorization 头中：
```
authorization: Bearer xx...
```

测试是否登录成功
```
http://127.0.0.1:5000/api/v1/test/token
```

### 成绩管理CRUD

#### 查询所有成绩

```
POST http://127.0.0.1:5000/api/v1/score/search_all
```

#### 分页查询成绩

```
POST http://127.0.0.1:5000/api/v1/score/search
```

请求体:
```json
{
  "page": 1,
  "per_page": 10,
  "keyword": "数学"
}
```

#### 添加成绩

```
POST http://127.0.0.1:5000/api/v1/score/add
```

请求体:
```json
{
  "student_id": 10,
  "subject": "生物",
  "score_value": 88.5,
  "semester": "2024 春季"
}
```

#### 更新成绩

```
POST http://127.0.0.1:5000/api/v1/score/update
```

请求体:
```json
{
  "score_id": 13,
  "score_value": 94.5
}
```

#### 删除成绩

```
POST http://127.0.0.1:5000/api/v1/score/delete
```

请求体:
```json
{
  "score_id": 15
}
```

## 常见问题

1. **数据库连接错误**
   - 检查数据库服务是否运行
   - 验证配置文件中的数据库连接信息是否正确

2. **接口返回 1002 未授权**
   - 检查是否已登录并获取 token
   - 确认 token 在请求头中正确设置

## 项目开发

### 添加新的 API 端点


1. 在 `app/models` 中创建数据模型
2. 在 `app/dao` 中创建数据访问层
3. 在 `app/api/v1` 中创建对应的 API 文件
4. `app/api/v1/__init__.py` 中注册新的 API 蓝图

### 运行测试

项目目前没有包含自动化测试，可以使用 Postman 或类似工具进行 API 测试。

## License

MIT License
