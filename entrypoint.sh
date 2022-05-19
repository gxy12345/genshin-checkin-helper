#!/bin/sh
set -e

echo -e "\n ======== \n ${Info} ${GreenBG} 拉取最新项目 ${Font} \n ======== \n"
git pull

echo -e "\n ======== \n ${Info} ${GreenBG} 更新运行依赖 ${Font} \n ======== \n"
pip3 install --no-cache-dir -r requirements.txt

echo -e "\n ======== \n ${Info} ${GreenBG} 读取config文件 ${Font} \n ======== \n"
cp /app/genshincheckinhelper/config.json ./genshincheckinhelper/config/config.json

echo -e "\n ======== \n ${Info} ${GreenBG} 启动小助手 ${Font} \n ======== \n"
python3 ./genshincheckinhelper/main.py