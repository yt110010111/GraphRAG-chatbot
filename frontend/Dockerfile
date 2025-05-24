# frontend/Dockerfile

FROM node:18-alpine

WORKDIR /app

# 複製依賴定義檔
COPY package*.json ./

# 安裝依賴
RUN npm install

# 複製專案其他檔案
COPY . .

# 啟動 React 開發伺服器
CMD ["npm", "start"]
