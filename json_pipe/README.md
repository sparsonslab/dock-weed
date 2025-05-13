

## Build images

```

docker build -t process_b -f process_b.dockerfile .
```

## Run as an end-to-end pipe, in one go

```
docker run process_a | docker run -i process_b
```

## Run container with input

The container must have an entry point command that:
- Receives JSON input through std::in
- Provides JSON output through std:out
- When it receives a blank/empty input, outputs a template of input and output JSON as:
> `{'input': {....}, 'output': {...}}`

Inspect to get the container's entry point command.
```
docker inspect --type=image --format={{.Config.Entrypoint}} process_b 

>> [python run.py]
```

```
echo -n | docker run --name test_eda278bebfb4 -i eda278bebfb4 
```

Start the container.
```
docker run --name process_b_1 -i -d process_b
```

Get default inputs.
```
echo -n | docker exec -i process_b_1 python run.py

>> {"x": 1.0, "y": 1.0}

or ...
echo -n | docker exec -i process_b_1 python run.py > process_b_defaults.json
```

Call the running container with input.
```
docker run process_a | docker exec -i process_b_1 python run.py

>> x + y = 124.76769

echo '{"x": 11.98769, "y": 186.78}' | docker exec -i process_b_1 python run.py

>> x + y = 198.76769000000002
```

Check what containers are running.
```
docker ps
```

Stop and remove the container.
```
docker stop process_b_1
docker rm process_b_

or ...
docker rm process_b_1 -f
```


https://docs.docker.com/reference/dockerfile
https://docs.docker.com/reference/cli/docker/

https://docker-py.readthedocs.io/en/stable/
