#!/bin/bash
docker rm -f forenings_medlemmer
docker build -t codingpirates/forenings_medlemmer .

docker run -ti --name="forenings_medlemmer" -p 8000:8000 -v $PWD:/usr/app codingpirates/forenings_medlemmer
