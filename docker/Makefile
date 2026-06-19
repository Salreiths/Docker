.PHONY: build run test clean deploy

# Переменные
IMAGE_NAME = users-app
CONTAINER_NAME = users-container
PORT = 8118
REMOTE_USER = visvesvaraya@kubsu.tyvik.ru
REMOTE_HOST = 212.192.134.135
REMOTE_PORT = 60080

# Сборка образа
build:
	podman build -t $(IMAGE_NAME) .

# Запуск контейнера
run:
	podman run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Остановка и удаление контейнера
stop:
	podman stop $(CONTAINER_NAME) || true
	podman rm $(CONTAINER_NAME) || true

# Запуск тестов
test:
	podman run --rm $(IMAGE_NAME) pytest tests/ -v

# Очистка
clean: stop
	podman rmi $(IMAGE_NAME) || true

# Запуск в фоновом режиме с логами
start: build stop run
	podman logs -f $(CONTAINER_NAME)

# Деплой на сервер
deploy:
	# Сохраняем образ
	podman save $(IMAGE_NAME) | gzip > $(IMAGE_NAME).tar.gz
	# Копируем на сервер
	scp -P $(REMOTE_PORT) $(IMAGE_NAME).tar.gz $(REMOTE_USER)@$(REMOTE_HOST):/tmp/
	# Загружаем и запускаем на сервере
	ssh -p $(REMOTE_PORT) $(REMOTE_USER)@$(REMOTE_HOST) \
		"podman load < /tmp/$(IMAGE_NAME).tar.gz && \
		 podman stop $(CONTAINER_NAME) || true && \
		 podman rm $(CONTAINER_NAME) || true && \
		 podman run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) --restart=always $(IMAGE_NAME) && \
		 rm /tmp/$(IMAGE_NAME).tar.gz"
	# Удаляем локальный архив
	rm $(IMAGE_NAME).tar.gz

# Проверка работоспособности
check:
	curl -X GET "http://$(REMOTE_HOST):$(REMOTE_PORT)/visvesvaraya@kubsu.tyvik.ru/users/"
