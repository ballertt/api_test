# 接口自动化测试框架

基于 Python + pytest + requests 的分层接口自动化测试框架。

## 技术栈
- Python 3.x / pytest / requests / pytest-html / Allure（后续）
- 分层架构：common（公共层）/ api（接口对象层）/ testcase（用例层）

## 目录结构
common/      公共层：配置、日志、请求客户端封装
api/         接口对象层：每个接口一个类
testcase/    用例层：测试用例
testdata/    数据层：测试数据文件
reports/     测试报告

## 快速开始
1. 创建虚拟环境：`python -m venv venv`
2. 激活：Windows `venv\Scripts\activate`
3. 安装依赖：`pip install -r requirements.txt`
4. 运行测试：`pytest testcase/ -v`
5. 生成报告：`pytest testcase/ --html=reports/report.html --self-contained-html`

## 功能特性
- 多环境切换（dev/test，通过 TEST_ENV 环境变量）
- 请求客户端封装（统一 headers、超时、日志）
- 登录 token 自动注入
- 数据驱动（后续）