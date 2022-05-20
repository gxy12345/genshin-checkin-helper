#!/bin/sh
set -e

echo -e "\n ======== \n ${Info} ${GreenBG} 拉取最新项目 ${Font} \n ======== \n"
git pull

echo -e "\n ======== \n ${Info} ${GreenBG} 更新运行依赖 ${Font} \n ======== \n"
pip3 install -r requirements.txt

echo -e "\n ======== \n ${Info} ${GreenBG} 读取旧config文件 ${Font} \n ======== \n"
if [ -f "/app/genshincheckinhelper/config/config.json" ]; then
  echo -e "发现旧路径下的配置文件，进行复制..."
  cp /app/genshincheckinhelper/config/config.json ./genshincheckinhelper/config/config.json
else
  echo -e "旧版配置目录未发现配置文件，使用新版配置路径"
fi

echo -e "\n ======== \n ${Info} ${GreenBG} 启动原神小助手 ${Font} \n ======== \n"
python3 ./genshincheckinhelper/main.py