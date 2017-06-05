all: test

test:
	bash test.sh

spelling:
	sphinx-build -b spelling doc/source/ doc/build/spelling
