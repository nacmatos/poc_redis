
# Teste básico com o Redis

## Redis : instalando e compilando 
```
 -- Se estiver rodando no Ubuntu, pode ser necessário instalar estas packages antes
 $ sudo apt install make gcc tcl
 --
 $ curl https://download.redis.io/releases/redis-6.2.13.tar.gz -O 
 $ tar -zxvf redis-6.2.13.tar.gz
 $ cd redis-6.2.13/
 $ make && make test
 ... aguarde a mensagem...
 \o/ All tests passed without errors!
```

## Iniciando o servidor 
```
$ ./redis-6.2.13/src/redis-server
...
               Running in standalone mode
               Port: 6379
...
```

## Preparando o virtual env do Python e instalando os módulos necessários
```
 $ python3 -m venv --prompt redis .pyenv
 $ source ./.pyenv/bin/activate
 $ pip3 install --upgrade pip
 $ pip install redis mimesis
```


## Gerando o CSV
```
 $ /usr/bin/time -v python3 ./gera_usuarios.py 500000 >usuarios500K.csv
 ...
 Elapsed (wall clock) time (h:mm:ss or m:ss): 0:12.88
 ...

 $ wc -l
 500001 usuarios500K.csv

 $ awk -F, '{print $1}' <usuarios500K.csv | sort | uniq | wc -l
 499876

 $ du -sh usuarios500K.csv
 33M usuarios500K.csv
```

## Carregando os dados no Redis
```
 $ /usr/bin/time -v python3 ./load_usuarios2.py usuarios500K.csv 127.0.0.1 6379 0
 ...
 Elapsed (wall clock) time (h:mm:ss or m:ss): 0:38.63
``` 

## Testando
```
 $ python3 ./get_usuarios.py usuarios500K.csv 127.0.0.1 6379 0
 ... 10 XMLs deve ser consultados
 Elapse 0.0024454169997625286s

 $ python3 ./get_usuarios2.py usuarios500K.csv 127.0.0.1 6379 0
 ... fica continuamente fazendo GETs em CPFs aleatórios ...
```

## Usando o cli do Redis
```
 $ ./redis-6.2.13/src/redis-cli -n 0

 127.0.0.1:6379> dbsize
 (integer) 499875

 127.0.0.1:6379> get 918.809.127-91
 ... XML ...

```