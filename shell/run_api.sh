docker build -t db:latest -f database/Dockerfile .
docker built -t api:latest -f api/Dockerfile .
docker run -d -p 4001:4001 api
docker run -d -p 4000:4000 db