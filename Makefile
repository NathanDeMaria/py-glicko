NAME=py-glicko

build:
	docker build -t ${NAME} .

run: build
	docker run -ti --rm ${NAME}

notebook: build
	docker run -ti --rm \
		-v ${PWD}/examples/://examples/ \
		-p 8888:8888 ${NAME}

environment:
	conda env create -f environment.yaml -n ${NAME} || conda env update -f environment.yaml -n ${NAME}
	conda activate ${NAME} && pip install -e .

.DEFAULT: build
	docker run -ti --rm ${NAME} $@
