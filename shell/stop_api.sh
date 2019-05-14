docker rm -f $(docker ps -a -q --filter ancestor=api) $(docker ps -a -q --filter ancestor=db)
