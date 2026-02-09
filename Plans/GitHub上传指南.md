# GitHub上传指南 - 餐食管理系统

## 前提条件

- 已安装Git
- 拥有GitHub账户
- 项目代码已准备完成

## 第一步：安装Git

### 方法1：使用winget安装（推荐）

```powershell
# 以管理员身份运行PowerShell，执行以下命令
winget install Git.Git
```

### 方法2：手动下载安装

1. 访问 https://git-scm.com/download/win
2. 下载Windows版本的Git安装程序
3. 运行安装程序，按照默认设置完成安装
4. 安装完成后，重新打开终端

### 验证Git安装

```bash
git --version
```

如果显示Git版本号，说明安装成功。

## 第二步：配置Git

首次使用Git需要配置用户信息：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 第三步：创建GitHub仓库

1. 访问 https://github.com 并登录您的账户
2. 点击右上角的"+"按钮，选择"New repository"
3. 填写仓库信息：
   - **Repository name**: `MealManagementSystem`
   - **Description**: `餐食管理系统 - 基于Flask和MySQL的完整餐食管理解决方案，支持多用户并发控制、Excel导入导出、微信小程序等功能`
   - **Public/Private**: 根据您的需求选择
   - **不要勾选**: "Initialize this repository with a README"
4. 点击"Create repository"按钮

创建成功后，GitHub会显示仓库的URL，格式为：
```
https://github.com/YOUR_USERNAME/MealManagementSystem.git
```

## 第四步：初始化Git仓库并上传

### 4.1 进入项目目录

```bash
cd d:\weige\MealManagementSystem
```

### 4.2 初始化Git仓库

```bash
git init
```

### 4.3 添加所有文件到暂存区

```bash
git add .
```

### 4.4 提交更改

```bash
git commit -m "Initial commit: 餐食管理系统完整版本"
```

### 4.5 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）

```bash
git remote add origin https://github.com/YOUR_USERNAME/MealManagementSystem.git
```

### 4.6 推送到GitHub

```bash
git branch -M main
git push -u origin main
```

如果使用旧版本的Git，可能需要使用：

```bash
git push -u origin master
```

## 第五步：验证上传

1. 访问您的GitHub仓库页面
2. 检查所有文件是否已成功上传
3. 确认README.md文件显示正常

## 常见问题

### Q1: 推送时提示身份验证错误

**解决方案**：
1. 使用GitHub个人访问令牌（Personal Access Token）
2. 访问 https://github.com/settings/tokens
3. 点击"Generate new token (classic)"
4. 选择权限范围，至少需要 `repo` 权限
5. 生成令牌并复制
6. 使用令牌进行身份验证：

```bash
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/MealManagementSystem.git
```

### Q2: 推送时提示SSL证书错误

**解决方案**：
```bash
git config --global http.sslVerify false
```

### Q3: .gitignore文件不生效

**解决方案**：
```bash
# 清除Git缓存
git rm -r --cached .
# 重新添加文件
git add .
# 重新提交
git commit -m "Update .gitignore"
```

### Q4: 文件太大无法推送

**解决方案**：
1. 检查.gitignore文件，确保大文件被忽略
2. 使用Git LFS（Large File Storage）处理大文件：

```bash
git lfs install
git lfs track "*.db"
git lfs track "*.xlsx"
git add .gitattributes
git commit -m "Configure Git LFS"
```

## 后续维护

### 更新代码

```bash
# 查看修改状态
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述您的修改"

# 推送到GitHub
git push
```

### 创建新分支

```bash
# 创建并切换到新分支
git checkout -b feature/new-feature

# 在新分支上进行开发...

# 提交修改
git add .
git commit -m "Add new feature"

# 推送新分支
git push -u origin feature/new-feature
```

### 合并分支

```bash
# 切换到主分支
git checkout main

# 合并新分支
git merge feature/new-feature

# 推送合并结果
git push
```

## 项目结构说明

上传到GitHub的项目结构：

```
MealManagementSystem/
├── .gitignore              # Git忽略文件配置
├── README.md               # 项目说明文档
├── backend/               # 后端代码
│   ├── docs/            # 项目文档
│   ├── utils/           # 工具函数
│   ├── app.py           # 应用入口
│   ├── config.py        # 配置文件
│   ├── extensions.py     # 扩展初始化
│   ├── models.py        # 数据库模型
│   ├── routes.py        # API路由
│   └── requirements.txt # Python依赖
├── frontend/              # 前端代码
│   ├── index.html       # 首页
│   └── ui_design.html   # UI设计
└── wechat-miniprogram/    # 微信小程序代码
    ├── images/          # 图片资源
    ├── pages/           # 页面文件
    ├── app.js           # 小程序入口
    └── app.json         # 小程序配置
```

## 安全注意事项

1. **不要上传敏感信息**：
   - 数据库文件（*.db）
   - 配置文件中的密码
   - API密钥
   - 个人访问令牌

2. **使用.gitignore文件**：
   - 确保敏感文件被忽略
   - 检查.gitignore文件内容

3. **定期更新依赖**：
   - 及时更新requirements.txt
   - 修复安全漏洞

4. **代码审查**：
   - 使用Pull Request进行代码审查
   - 确保代码质量

## 项目亮点

上传到GitHub后，您的项目将展示以下亮点：

- ✅ 完整的餐食管理系统
- ✅ 基于Flask和MySQL的后端
- ✅ 支持多用户并发控制（乐观锁）
- ✅ Excel导入导出功能
- ✅ 微信小程序支持
- ✅ 完整的权限管理系统
- ✅ 详细的API文档
- ✅ 清晰的项目结构

## 联系方式

如有问题，请通过以下方式联系：
- GitHub Issues: https://github.com/YOUR_USERNAME/MealManagementSystem/issues
- Email: your.email@example.com

## 许可证

MIT License - 详见项目根目录的LICENSE文件

---

**祝您上传顺利！**
