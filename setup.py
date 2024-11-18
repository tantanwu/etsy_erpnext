from setuptools import setup, find_packages

setup(
    name="etsy_erpnext",  # 插件名称
    version="1.0.0",  # 版本号
    description="A local ERPNext module for Etsy order management.",  # 简要描述
    packages=find_packages(),  # 自动查找模块
    include_package_data=True,  # 包括静态文件
    install_requires=[
        "requests>=2.26.0",  # API交互工具
        "pytz>=2021.1"  # 处理时区的工具
    ],
    python_requires='>=3.6',  # Python最低版本要求
)