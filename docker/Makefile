# Переменные
IMAGE_NAME = users-app
CONTAINER_NAME = users-container
PORT = 8118
REMOTE_USER = visvesvaraya@kubsu.tyvik.ru
REMOTE_HOST = 212.192.134.135
REMOTE_PORT = 60080

# Сборка образа (из папки docker)
build:
	docker build -t $(IMAGE_NAME) -f Dockerfile .

# Запуск контейнера
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Остановка контейнера
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Запуск тестов
test:
	docker run --rm $(IMAGE_NAME) pytest tests/ -v

# Очистка
clean: stop
	docker rmi $(IMAGE_NAME) || true

# Перезапуск
restart: stop build run

# Логи
logs:
	docker logs -f $(CONTAINER_NAME)

# Запуск в интерактивном режиме (для отладки)
shell:
	docker run -it --rm $(IMAGE_NAME) /bin/bash

# Проверка работоспособности
check:
	curl -X GET "http://$(REMOTE_HOST):$(REMOTE_PORT)/$(REMOTE_USER)/users/"

# Деплой на сервер
deploy:
	# Сохраняем образ
	docker save $(IMAGE_NAME) | gzip > $(IMAGE_NAME).tar.gz
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

# Полный цикл: сборка, тесты, деплой
all: build test deploy

# Справка по командам
help:
	@echo "Доступные команды:"
	@echo "  make build    - Собрать Docker образ"
	@echo "  make run      - Запустить контейнер"
	@echo "  make stop     - Остановить и удалить контейнер"
	@echo "  make test     - Запустить тесты"
	@echo "  make clean    - Очистить образы"
	@echo "  make restart  - Перезапустить контейнер"
	@echo "  make logs     - Показать логи"
	@echo "  make shell    - Запустить shell в контейнере"
	@echo "  make check    - Проверить работоспособность API"
	@echo "  make deploy   - Деплой на сервер"
	@echo "  make all      - Собрать, протестировать и задеплоить"
