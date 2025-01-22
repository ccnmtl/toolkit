APP=toolkit
all: jenkins eslint cypress-test jstest js-build

.PHONY: all

include *.mk

integrationserver: $(PY_SENTINAL)
	$(MANAGE) integrationserver --noinput --skip-checks
.PHONY: integrationserver

webpack: $(JS_SENTINAL)
	npm run dev
.PHONY: webpack

js-build: $(JS_SENTINAL)
	rm -rf media/build/*
	npm run build:prod
.PHONY: js-build

dev:
	trap 'kill 0' EXIT; make runserver & make webpack
.PHONY: dev