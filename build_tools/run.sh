function cleanup() {
  docker stop lemmy-nhl-gdt-bot
  docker container rm --force lemmy-nhl-gdt-bot
  echo "cleanup complete"
}

trap cleanup EXIT

docker build --tag lemmy-nhl-gdt-bot .
docker run --add-host statsapi.web.nhl.com:18.66.2.22 --rm --name lemmy-nhl-gdt-bot -v ./.env:/app/.env -v ./out:/app/out localhost/lemmy-nhl-gdt-bot:latest
