# CI-only source fixture; no image is published or deployed.
FROM golang:1.26.10-bookworm AS builder
ENV GOTOOLCHAIN=local
WORKDIR /src
RUN git init . \
    && git remote add origin https://github.com/minio/minio.git \
    && git fetch --depth=1 origin 9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a"
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /minio .
FROM scratch
COPY --from=builder /minio /minio
COPY --from=builder /src/LICENSE /LICENSE
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
ENV MINIO_BROWSER=off MINIO_UPDATE=off
EXPOSE 9000
ENTRYPOINT ["/minio"]
CMD ["server", "/data"]
