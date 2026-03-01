#!/bin/bash

# 获取脚本所在目录（兼容性更好的写法）
# Get the directory where the script is located (a more compatible way to write it).
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 切换到脚本所在目录
# Switch to the directory where the script is located.
cd "$SCRIPT_DIR"

# 检查 app_ui.py 文件是否存在
# Check if the app_ui.py file exists.
if [ ! -f "app_ui.py" ]; then
    # echo "错误: app_ui.py 文件未找到"
    echo "Error: app_ui.py file not found"
    exit 1
fi

# 以管理员权限运行 app_ui.py
# Run app_ui.py with administrator privileges.
sudo python app_ui.py