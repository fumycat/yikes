redis_server_exec = ~/redis/redis-6.2.4/src/redis-server
redis_config_file = ~/redis/redis-6.2.4/redis.conf

.PHONY: build clean run

build: bin bin/gemm bin/gemv
	python -m pip install -r requirements.txt -q -q

bin/gemm: src/la0.cu
	nvcc src/la0.cu -lcublas -o $@

bin/gemv: src/la1.cu
	nvcc src/la1.cu -lcublas -o $@

bin:
	mkdir -p bin

clean:
	rm -rf bin

run: build
	$(redis_server_exec) $(redis_config_file) &
	python server.py
