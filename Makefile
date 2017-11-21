NAME=pyspider
TAG = latest

build:
	echo building ${NAME}:${TAG}
	docker build -t ${NAME}:${TAG} .

test:
	docker run -d --name pyspider --restart=always \
	-p 5000:5000 \
	-v $(CURDIR)/config:/data \
	${NAME}:${TAG}
