# Dockerfile im stock-publisher Verzeichnis
FROM golang:1.20-alpine AS builder

# Wechsle ins Arbeitsverzeichnis
WORKDIR /app

# Kopiere Go modules und install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Kopiere den restlichen Code und baue das Binary
COPY . .
RUN go build -o stock-publisher

# ----------------------------------------------
# Produktions-Image
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/stock-publisher /app/

# Exponiere Port 8080, da der Healthcheck im Publisher hinterlegt ist
EXPOSE 8080

ENTRYPOINT ["/app/stock-publisher"]
