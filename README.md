### 性能压测

```shell
wrk --threads=8 --connections=100 --duration=300s http://localhost:8000/search
```

```text
Running 5m test @ http://localhost:8000/search
  8 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   327.85ms  167.56ms   1.81s    68.44%
    Req/Sec    32.90     14.63   110.00     69.38%
  78308 requests in 5.00m, 6.35GB read
  Socket errors: connect 0, read 78305, write 0, timeout 0
Requests/sec:    260.94
Transfer/sec:     21.67MB

```