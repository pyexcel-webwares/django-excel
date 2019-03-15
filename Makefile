all: test

test:
	bash test.sh

spelling:
	sphinx-build -b spelling docs/source/ docs/build/spelling

doc:
	sphinx-build -b html docs/source docs/build

format:
	isort -y $(find pyexcel -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
	black -l 79 pyexcel
	black -l 79 tests

lint:
	bash lint.sh
