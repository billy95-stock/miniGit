.PHONY: run test

run:
	python3 backend/main.py

test:
	python3 -m doctest -v backend/versions.py
