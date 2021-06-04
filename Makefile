redis_server_exec = ~/redis/redis-6.2.4/src/redis-server
redis_config_file = ~/redis/redis-6.2.4/redis.conf

build: gemm

gemm: la0.cu
	nvcc $^ -lcublas -o $@

clean:
	rm -f gemm

run: build
	$(redis_server_exec) $(redis_config_file) &
	python main.py
