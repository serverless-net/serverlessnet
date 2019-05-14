# run the container
docker run --name containernet -it --rm --privileged --pid='host' \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v "$(pwd)":/containernet/serverlessnet  \
	containernet/containernet /bin/bash

