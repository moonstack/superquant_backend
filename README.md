
superquant_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 启动入口
│   ├── api/                    # 路由接口层
│   │   ├── __init__.py
│   │   ├── factors.py          # 因子模板相关接口
│   │   ├── backtest.py         # 回测相关接口
│   │   ├── trade.py            # 实盘交易接口
│   ├── services/               # 业务逻辑实现层
│   │   ├── __init__.py
│   │   ├── factor_service.py
│   │   ├── backtest_service.py
│   │   ├── trade_service.py
│   ├── models/                 # 数据模型（Pydantic/响应结构）
│   │   ├── __init__.py
│   │   ├── factor_model.py
│   │   ├── backtest_model.py
│   │   ├── trade_model.py
│   ├── core/                   # 核心配置与工具模块
│   │   ├── __init__.py
│   │   ├── config.py           # 配置文件加载
│   │   ├── task_runner.py      # 回测异步任务调度器（如 asyncio、thread）
│   │   ├── file_io.py          # 因子模板的读写（如 JSON、YAML）
│   ├── data/                   # 数据存储（或指向本地数据源）
│   │   ├── factors/            # 自定义因子模板文件夹
│   │   ├── backtest/           # 回测结果文件（如 HDF5、图像、JSON）
│   │   ├── trade_logs/         # 实盘日志
├── requirements.txt
├── README.md
└── run.py                      # 入口脚本（可选 uvicorn 启动）
