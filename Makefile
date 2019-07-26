IMAGE=pyglicko

build:
	docker build -t ${IMAGE} .

run:
	docker run -ti --rm ${IMAGE}

notebook:
	docker run -ti --rm \
		-v ${PWD}/examples/://examples/ \
		-p 8888:8888 ${IMAGE}
