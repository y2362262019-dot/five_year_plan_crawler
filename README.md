# 中国地级市五年规划文件爬虫

多线程爬取中国地级市五年规划（十一五至十四五）相关文件，包括 HTML 网页正文提取和 PDF/DOC/DOCX/WPS 等附件下载。

## 功能

- **多线程并发爬取** — 可配置并发数，默认 5 线程
- **网页正文提取** — 自动去除 script/style/nav 等噪音，提取干净文本
- **附件自动下载** — 识别页面中的 PDF/DOC/DOCX/WPS 链接并下载
- **断点续传** — 中断后可从上次进度继续，避免重复抓取
- **频率控制** — 内置请求间隔，避免对目标服务器造成压力
- **多编码支持** — 自动检测 UTF-8/GBK/GB2312/GB18030/BIG5 等编码
- **结果回写** — 将抓取状态和本地路径写回 Excel

## 快速开始

```bash
# 全量爬取（5 线程）
python -m main

# 指定城市
python -m main --city 北京市

# 断点续传
python -m main --resume

# 自定义并发数
python -m main --workers 8

# 测试模式（限制条数）
python -m main --limit 10
```

## 数据来源

Excel 数据文件需放置在 `data/` 目录下，包含以下字段：
- 链接序号、省份、城市、所属时期、新网址、备注

## 输出结构

```
output/
├── 省份-城市/
│   ├── 序号-省份-城市-标题.txt    # 提取的网页正文
│   └── files/                      # 下载的附件
│       └── 序号-省份-城市-标题.pdf
├── checkpoints/
│   └── progress.json               # 断点续传进度
└── *_已爬取.xlsx                   # 回写结果
```

## 项目结构

| 文件 | 说明 |
|------|------|
| `main.py` | 主入口，多线程调度 |
| `fetcher.py` | HTTP 请求与重试 |
| `extractor.py` | HTML 正文提取与文件链接发现 |
| `downloader.py` | PDF/DOC 等文件下载 |
| `organizer.py` | 本地文件命名与目录组织 |
| `config.py` | 全局配置（UA、超时、域名过滤等） |
| `checkpoint.py` | 断点续传进度管理 |
| `rate_limiter.py` | 请求频率控制 |
| `excel_writer.py` | Excel 结果回写 |
