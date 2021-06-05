redis_server_exec = ~/redis/redis-6.2.4/src/redis-server
redis_config_file = ~/redis/redis-6.2.4/redis.conf

build: bin/gemm
	python -m pip install -r requirements.txt -q -q

bin/gemm: src/la0.cu
	nvcc $^ -lcublas -o $@

clean:
	rm -f gemm

run: build
	$(redis_server_exec) $(redis_config_file) &
	python server.py
