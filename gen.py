import covid_stack as stk

def people_gen(population):
    for i in range(population):
        person = stk.person()
        stk.people.append(person)

def enviro_gen(floors, **rooms):
    pass