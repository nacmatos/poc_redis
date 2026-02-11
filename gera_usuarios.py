#!/usr/bin/env python3

import random
import sys

import mimesis
import mimesis.builtins
from mimesis.locales import Locale

p = mimesis.Person(locale=mimesis.Locale.PT_BR)
d = mimesis.Datetime()
p_br = mimesis.builtins.BrazilSpecProvider()
age = lambda: int(random.gauss(37,14))

print('cpf,nome,email,idade,ultacesso');
for i in range(0,int(sys.argv[1])): print(f'{p_br.cpf()},{p.full_name()},{p.email()},{age()},{d.date()}', flush=True)
