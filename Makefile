.PHONY: test check clean build dist all

TOP_DIR := $(shell pwd)

# ifeq ($(FILE), $(wildcard $(FILE)))
# 	@ echo target file not found
# endif

INFO_MAIN_SCRIPT := temp.py

INFO_PYPI_MIRROR ?= https://pypi.tuna.tsinghua.edu.cn/simple/

init:
	@echo "~> start init this project"
	@if [ -f ".env" ]; then echo "~> .env is exits"; else echo PIPENV_PYPI_MIRROR=$(INFO_PYPI_MIRROR) >.env; fi
	@echo "-> check python version"
	python -V
	@echo "-> check pip version"
	pip -V
	@echo "-> check pipenv version if error just use [ pip install pipenv ]"
	pipenv --version
	@echo "~> you can use [ make help ] see more task"

checkDepends: init
	pipenv check

depGraph:
	@echo "just show depends graph below"
	pipenv graph

depDev:
	@echo "just install dev depends"
	pipenv install --dev

runDev:
	pipenv run python $(INFO_MAIN_SCRIPT) --help --dev

run:
	pipenv run python $(INFO_MAIN_SCRIPT) --help

dep: checkDepends
	@echo "just check depends info below"
	pipenv install
	@echo "if want install new pkg just use [ pipenv install requests ]"

help:
	@echo "make init - check base env of this project"
	@echo "make depDev - check depends of dev version"
	@echo "make runDev - run script $(INFO_MAIN_SCRIPT) in dev version"
	@echo "make dep - check depends of version"
	@echo "make run - run script $(INFO_MAIN_SCRIPT)"