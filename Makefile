NAME=python-project-template
VERSION=0.1.0
CURRENT_DIRECTORY=$(shell pwd)

prepare-develop-environment:
	@echo "Preparing coding environment"
	@echo "Creating virtual environment"
	@echo "Installing dependencies"
	python3 -m venv .venv && source .venv/bin/activate  && pip install -e .[coding]
	@echo "Coding environment ready"

rename-project:
	@echo "Renaming project"
	@echo "Enter new project name (kebab-case):"
	@read new_project_name_hyphenated; \
	new_project_name_underscored=$$(echo "$$new_project_name_hyphenated" | sed 's/-/_/g'); \
	sed -i "s/python-project-template/$$new_project_name_hyphenated/g" pyproject.toml; \
	sed -i "s/python_project_template/$$new_project_name_underscored/g" pyproject.toml; \
	sed -i "s/python_project_template/$$new_project_name_underscored/g" tests/test_example.py; \
	sed -i "s/NAME=python-project-template/NAME=$$new_project_name_hyphenated/g" Makefile; \
	mv src/python_project_template src/$$new_project_name_underscored
	@echo "Project renamed"


build:
	@echo "Building Docker image"
	cp -r ./src ./docker && cp ./pyproject.toml ./docker && cp ./README.md ./docker; \
	cd docker && docker build -t ${NAME}:${VERSION} .; \
	rm -rf ./src && rm ./pyproject.toml && rm ./README.md
	@echo "Docker image built"

run:
	@if [ `docker container ls -a --filter "name=${NAME}" | wc -l | sed "s/ //g"` -eq 2 ]; then \
		docker container stop ${NAME}; \
		docker container rm ${NAME}; \
		docker container run \
			-it --privileged \
			--gpus all \
			-d \
			-v ${CURRENT_DIRECTORY}:/app \
			-v /var/run/docker.sock:/var/run/docker.sock \
			--name ${NAME} ${NAME}:${VERSION} \
			/bin/bash; \
	else \
		docker container run \
			-it --privileged \
			--gpus all \
			-d \
			-v ${CURRENT_DIRECTORY}:/app \
			-v /var/run/docker.sock:/var/run/docker.sock \
			--name ${NAME} ${NAME}:${VERSION} \
			/bin/bash; \
	fi

log:
	docker container logs -f ${NAME}
