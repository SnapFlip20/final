import string, random

abc_set = string.ascii_letters*4

fin = open("data.md", 'w')

fin.write('# TestData\n')
for i in range(random.randrange(4, 10)):
    s = random.sample(abc_set, random.randrange(13, 26))
    fin.write(f'## {i+1}. {"".join(s)}\n')
    s = random.sample(abc_set, random.randrange(26, 52))
    fin.write(f'### {i+1} description: {"".join(s)}\n')
    for j in range(random.randrange(2, 7)):
        t = random.sample(abc_set, random.randrange(13, 26))
        fin.write(f'#### {i+1}-{j+1}. {"".join(t)}\n')
        t = random.sample(abc_set, random.randrange(26, 52))
        fin.write(f'##### {i+1}-{j+1} description: {"".join(t)}\n')


fin.close()