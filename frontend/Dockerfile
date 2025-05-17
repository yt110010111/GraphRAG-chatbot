# 建構階段
FROM node:18-alpine AS build

WORKDIR /app

# 複製 package.json & lock，先安裝依賴（有 cache）
COPY package*.json ./
RUN npm install

# 複製剩餘所有檔案（此時包含 tailwind.config.js, src/, public/ 等）
COPY . .

# 初始化 tailwind（如果還沒初始化）
# 建議只做一次，不要每次 build 都做；或檢查有沒有 tailwind.config.js 再決定
# RUN npx tailwindcss init -p

# 打包 React App（會觸發 Tailwind 編譯）
RUN npm run build

# 正式階段：使用 nginx
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
