all: test

test:
	bash test.sh

spelling:
	sphinx-build -b spelling docs/source/ docs/build/spelling

doc:
	sphinx-build -b html docs/source docs/build
