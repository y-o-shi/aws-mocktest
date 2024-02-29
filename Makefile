# after modifying Dockerfile or requirements.txt
build-test-image:
	docker build -t aws-autotest-python .

# execute test case (Pytest)
test:
	docker run --rm -v '${PWD}/src:/app/src' -it aws-autotest-python