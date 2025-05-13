
```
docker build -t process_alpha -f process_alpha.dockerfile .
```

```
docker run --name process_alpha_1 -i -d process_alpha
```

```
echo '{"x": 11.98769, "y": 186.78}' | docker exec -i process_alpha_1 ./process_alpha
```

```
docker rm process_alpha_1 -f
```

https://hub.docker.com/

https://github.com/dockersamples/c-plus-plus-docker/blob/main/Dockerfile