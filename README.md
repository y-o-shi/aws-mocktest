## Mocktest-for-PythonAWS(boto3)

```bash
# build image (Recommend to build at the first time or after modifying Dockerfile or requirements.txt)
$ make build-test-image
or
$ docker build -t aws-mocktest-python .

# execute test by Pytest
$ make test
or
$ docker run --rm -v '${PWD}/src:/app/src' -it aws-mocktest-python
```
