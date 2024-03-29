ACCOUNT=gaf3
IMAGE=python-relations-mysql
INSTALL=python:3.8.5-alpine3.12
VERSION?=0.6.3
NETWORK=relations.io
MYSQL_IMAGE=mysql:8.0.28-oracle
MYSQL_HOST=$(ACCOUNT)-$(IMAGE)-mysql
DEBUG_PORT=5678
TTY=$(shell if tty -s; then echo "-it"; fi)
VOLUMES=-v ${PWD}/lib:/opt/service/lib \
		-v ${PWD}/test:/opt/service/test \
		-v ${PWD}/mysql.sh:/opt/service/mysql.sh \
		-v ${PWD}/.pylintrc:/opt/service/.pylintrc \
		-v ${PWD}/setup.py:/opt/service/setup.py
ENVIRONMENT=-e MYSQL_HOST=$(MYSQL_HOST) \
			-e MYSQL_PORT=3306 \
			-e PYTHONDONTWRITEBYTECODE=1 \
			-e PYTHONUNBUFFERED=1 \
			-e test="python -m unittest -v" \
			-e debug="python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest -v"
PYPI=-v ${PWD}/LICENSE.txt:/opt/service/LICENSE.txt \
	-v ${PWD}/PYPI.md:/opt/service/README.md \
	-v ${HOME}/.pypirc:/opt/service/.pypirc

.PHONY: build network mysql shell debug test lint setup tag untag testpypi pypi

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

network:
	-docker network create $(NETWORK)

mysql: network
	-docker rm --force $(MYSQL_HOST)
	docker run -d --network=$(NETWORK) -h $(MYSQL_HOST) --name=$(MYSQL_HOST) -e MYSQL_ALLOW_EMPTY_PASSWORD='yes' -e MYSQL_ROOT_HOST='%' $(MYSQL_IMAGE)
	docker run $(TTY) --rm --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "./mysql.sh"

shell: mysql
	docker run $(TTY) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh

debug: mysql
	docker run $(TTY) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest discover -v test"

test: mysql
	docker run $(TTY) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include 'lib/*.py'"

lint:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "pylint --rcfile=.pylintrc lib/"

setup:
	docker run $(TTY) $(VOLUMES) $(PYPI) $(INSTALL) sh -c "cp -r /opt/service /opt/install && cd /opt/install/ && \
	python setup.py install && \
	python -m relations_mysql.sql && \
	python -m relations_mysql.expression && \
	python -m relations_mysql.criterion && \
	python -m relations_mysql.criteria && \
	python -m relations_mysql.clause && \
	python -m relations_mysql.query && \
	python -m relations_mysql.ddl && \
	python -m relations_mysql.column && \
	python -m relations_mysql.index && \
	python -m relations_mysql.table"

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"

testpypi:
	docker run $(TTY) $(VOLUMES) $(PYPI) gaf3/pypi sh -c "cd /opt/service && \
	python -m build && \
	python -m twine upload -r testpypi --config-file=.pypirc dist/*"

pypi:
	docker run $(TTY) $(VOLUMES) $(PYPI) gaf3/pypi sh -c "cd /opt/service && \
	python -m build && \
	python -m twine upload --config-file=.pypirc dist/*"
