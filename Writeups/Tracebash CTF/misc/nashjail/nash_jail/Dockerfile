FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        socat && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m Shinobi

WORKDIR /home/Shinobi

COPY jail.sh .
COPY flag.txt .
COPY start.sh .

RUN chmod +x *.sh

USER Shinobi

EXPOSE 1337

CMD ["./start.sh"]