
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

## Preparando o virtual env do Python e instalando os módulos necessários
```
 $ python3 -m venv --prompt redis .pyenv
 $ source ./.pyenv/bin/activate
 
 $ pip install --upgrade pip
 $ pip install -r requirements.txt

 $ ln -sf $VIRTUAL_ENV/../redis-6.2.13/src/redis-server $VIRTUAL_ENV/bin/redis-server
 $ ln -sf $VIRTUAL_ENV/../redis-6.2.13/src/redis-cli    $VIRTUAL_ENV/bin/redis-cli
```

## Iniciando o servidor 
```
$ redis-server
```

## Gerando o CSV
```
 $ python3 gera_usuarios.py 500000 >usuarios500K.csv
 
 $ wc -l
 500001 usuarios500K.csv

 $ du -sh usuarios500K.csv
 33M usuarios500K.csv

 $ awk -F, '{print $1}' <usuarios500K.csv | sort | uniq | wc -l
 499876

```

## Carregando os dados no Redis
Todos os scripts que fazem acesso ao Redis consideram que por default ele está em 127.0.0.1:6379 e 0 como database number.  
```
 $ python3 load_usuarios.py usuarios.csv --redis_host=127.0.0.1 --redis_port=6379 --redis_db=0
 ...
 
``` 

## Carregando os dados via bulk-load usando redis-cli sem arquivos intermediários
```
 $ python3 gera_usuarios.py 500000 | python3 csv2pipe.py | redis-cli --pipe
 All data transferred. Waiting for the last reply...
 Last reply received from server.
 errors: 0, replies: 500000

```

## Testando
```
 $ python3 ./get_usuarios.py 
 2023-08-05 19:50:31 | INFO | Retriving keys...
 2023-08-05 19:50:31 | INFO | ...10 keys.
 2023-08-05 19:50:31 | INFO | Elapse 0.001275s
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | ... XML ...
 2023-08-05 19:50:31 | INFO | Elapse 0.001686s


 $ python3 ./get_usuarios2.py 
 ... fica continuamente fazendo GETs em CPFs aleatórios até se pressionar CTRL-C
```

## Estratégia para carregar novos dados sem afetar a base atual e fazer a troca a "quente"
```
 -- Carga é feita em outro database, diagamos o 1
 -- Note que estou passando o database no parâmetro -n
 $ python3 gera_usuarios.py 500000 | python3 csv2pipe.py | redis-cli -n 1 --pipe

 -- Uma vez feita com sucesso, se troca a "0" pela "1"
 $ redis-cli swapdb 0 1

 -- Pode-se então remover a base 1 (antiga 0) 
 $ redis-cli -n 1 flushdb
```

## Usando o cli do Redis
```
 $ ./redis-6.2.13/src/redis-cli

 127.0.0.1:6379> dbsize
 (integer) 499875

 127.0.0.1:6379> get 918.809.127-91
 ... XML ...

```
