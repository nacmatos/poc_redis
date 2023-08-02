#!/usr/bin/env python3

import sys

import mimesis
import mimesis.builtins

p = mimesis.Person(mimesis.Locale.PT_BR)
d = mimesis.Datetime()
p_br = mimesis.builtins.BrazilSpecProvider()

print('cpf,nome,email,idade,ultacesso');
for i in range(0,int(sys.argv[1])): print(f'{p_br.cpf()},{p.full_name()},{p.email()},{p.age()},{d.date()}')
