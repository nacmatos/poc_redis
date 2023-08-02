
# Teste básico com o Redis

## Instalando os modulos
```
 $ python3 -m venv --prompt redis .pyenv
 $ source ./.pyenv/bin/activate
 $ pip3 install --upgrade pip
 $ pip install redis mimesis
```

## Instalando e compilando
```
 $ curl https://download.redis.io/releases/redis-6.2.13.tar.gz -O 
 $ tar -zxvf redis-6.2.13.tar.gz
 $ cd redis-6.2.13/
 $ make 
 $ make test
```

## Iniciando o servidor 

$ ./redis-6.2.13/src/redis-server
...
               Running in standalone mode
               Port: 6379
               PID: 25562
...


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

## Carregando no Redis
```
 $ /usr/bin/time -v python3 ./load_usuarios2.py usuarios500K.csv 127.0.0.1 6379 0
 ...
 Elapsed (wall clock) time (h:mm:ss or m:ss): 0:38.63
``` 

## Testando
```
 $ python3 ./get_usuarios.py usuarios500K.csv 127.0.0.1 6379 0
 <data><item><cpf>742.833.330-00</cpf><nome>Aníbal Kirmse</nome><email>widescreen1827@protonmail.com</email><idade>24</idade><ultacesso>2016-06-29</ultacesso></item></data>
 <data><item><cpf>552.033.395-54</cpf><nome>Lidiana Debona</nome><email>flights2097@protonmail.com</email><idade>54</idade><ultacesso>2006-05-24</ultacesso></item></data>
 <data><item><cpf>611.103.308-55</cpf><nome>Virgolina Serata</nome><email>nearby2008@yahoo.com</email><idade>25</idade><ultacesso>2012-01-18</ultacesso></item></data>
 <data><item><cpf>339.359.717-53</cpf><nome>Laertes Vilar</nome><email>ontario2058@gmail.com</email><idade>42</idade><ultacesso>2018-06-22</ultacesso></item></data>
 <data><item><cpf>812.502.501-45</cpf><nome>Juna Barone</nome><email>residents1958@duck.com</email><idade>65</idade><ultacesso>2011-07-06</ultacesso></item></data>
 <data><item><cpf>918.809.127-91</cpf><nome>Pompeu Fillinger</nome><email>fix1807@example.org</email><idade>17</idade><ultacesso>2019-06-20</ultacesso></item></data>
 <data><item><cpf>247.578.267-61</cpf><nome>Fulgêncio Larsen</nome><email>heather1900@protonmail.com</email><idade>32</idade><ultacesso>2002-08-01</ultacesso></item></data>
 <data><item><cpf>926.677.705-60</cpf><nome>Fantina Domene</nome><email>homework1909@live.com</email><idade>64</idade><ultacesso>2012-07-01</ultacesso></item></data>
 <data><item><cpf>293.605.946-10</cpf><nome>Marcelo Fabro</nome><email>wit2003@gmail.com</email><idade>42</idade><ultacesso>2006-08-27</ultacesso></item></data>
 <data><item><cpf>354.637.210-76</cpf><nome>Christian Simoes</nome><email>checking1971@example.com</email><idade>36</idade><ultacesso>2015-10-19</ultacesso></item></data>
 Elapse 0.0024454169997625286s
```

## Usando o cli do Redis

```
 $ ./redis-6.2.13/src/redis-cli -n 0

 127.0.0.1:6379> dbsize
 (integer) 499875

127.0.0.1:6379> get 918.809.127-91
"<data><item><cpf>918.809.127-91</cpf><nome>Pompeu Fillinger</nome><email>fix1807@example.org</email><idade>17</idade><ultacesso>2019-06-20</ultacesso></item></data>"
```





