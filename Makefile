# after modifying Dockerfile or requirements.txt
build-test-image:
	docker build -t aws-autotest-python .

# execute test case (Pytest)
test:
	docker run --rm -v "${PWD}:/app" -it aws-autotest-python