redis_server_exec = ~/redis/redis-6.2.4/src/redis-server
redis_config_file = ~/redis/redis-6.2.4/redis.conf

.PHONY: build clean run debug

build: bin/gemm bin/gemv
	python -m pip install -r requirements.txt -q -q

bin/gemm: bin src/la0.cu
	nvcc src/la0.cu -lcublas -o $@

bin/gemv: bin src/la1.cu
	nvcc src/la1.cu -lcublas -o $@

bin:
	mkdir -p bin

clean:
	rm -f bin/gemm

run: build
	$(redis_server_exec) $(redis_config_file) &
	python server.py

debug:
	python server.py
