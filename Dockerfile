FROM python:3.10

LABEL maintainer="gordonchanfz@ainote.cloudns.biz"

WORKDIR /app
COPY . .

#定义时区参数
ENV TZ=Asia/Shanghai

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.12/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=048b95b48b708983effb2e5c935a1ef8483d9e3e
#设置时区
RUN apt-get update && apt-get install -y curl tzdata \
    &&  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone \
    #python相关
    &&python -m pip install --no-cache-dir --upgrade pip \
    && pip install -U aligo \
	&& pip install git+https://github.com/foyoux/aligo.git \
	&& pip install --no-cache-dir -r requirements.txt \
    #任务管理
    && curl -fsSLO "$SUPERCRONIC_URL" \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "$SUPERCRONIC" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# RUN cron job
CMD ["/usr/local/bin/supercronic", "/app/data/my-cron"]