# 第一阶段：编译环境
FROM node:20-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装（使用阿里源加速）
COPY package*.json ./
RUN npm install --registry=https://registry.npmmirror.com

# 复制所有源代码并执行打包
COPY . .
RUN npm run build

# 第二阶段：运行环境（使用轻量级 Nginx）
FROM nginx:stable-alpine as production-stage

# 从编译阶段复制打包后的文件到 Nginx 目录
# 注意：Vite 默认打包目录是 dist
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义 Nginx 配置（解决单页应用路由刷新 404 问题）
# 如果你没有特殊配置，可以用下面这个简单的替换命令
RUN sed -i 's/index  index.html index.htm;/try_files $uri $uri\/ \/index.html;/g' /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]