"""
Stworzone przez Radosław Krawiec, Szymon Czudowski

Mądra kuchnia dzięki logice rozmytej

Wymagane biblioteki do zainstalowania:
pip install "numpy<2.0" "scikit-fuzzy<1.14"
pip install matplotlib
pip install networkx


Problem:
Mamy w kuchni 6 grili i nie wiemy ile na raz ma być włączone

Restauracja pomieści 30 osób
W kuchni może pracować 6 osób
Maksymalnie kuchnia może wydać 60 posiłków na godzinę
Wiemy ile zamówień było w ciągu ostatniej godziny

"""


# import libraries
import os
from random import randint
import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt
from skfuzzy import control as ctrl
os.environ["XDG_SESSION_TYPE"] = "xcb"

# define variables - 3 inputs, 1 output
tables = ctrl.Antecedent(np.arange(0, 31, 1), 'tables')
staff = ctrl.Antecedent(np.arange(0, 7, 1), 'staff')
orders = ctrl.Antecedent(np.arange(0, 61, 1), 'orders')

grill = ctrl.Consequent(np.arange(0, 7, 1), 'grill')


# set weights manually
tables['low'] = fuzz.trimf(tables.universe, [0, 0, 15])
tables['medium'] = fuzz.trimf(tables.universe, [5, 15, 25])
tables['high'] = fuzz.trimf(tables.universe, [15, 30, 30])

staff['few'] = fuzz.trimf(staff.universe, [0, 0, 3])
staff['adequate'] = fuzz.trimf(staff.universe, [1, 3, 5])
staff['many'] = fuzz.trimf(staff.universe, [3, 6, 6])

orders['low'] = fuzz.trimf(orders.universe, [0, 0, 30])
orders['medium'] = fuzz.trimf(orders.universe, [15, 30, 45])
orders['high'] = fuzz.trimf(orders.universe, [30, 60, 60])

grill['low'] = fuzz.trimf(grill.universe, [0, 0, 2])
grill['medium'] = fuzz.trimf(grill.universe, [1, 3, 5])
grill['high'] = fuzz.trimf(grill.universe, [4, 6, 6])


# declare rules:
rule1 = ctrl.Rule(orders['low'] & tables['low'], grill['low'])
rule2 = ctrl.Rule(orders['high'] & tables['high'] & staff['few'], grill['high'])
rule3 = ctrl.Rule(orders['high'] & staff['many'], grill['medium'])
rule4 = ctrl.Rule(orders['medium'] & tables['medium'], grill['medium'])
rule5 = ctrl.Rule(orders['medium'] & staff['few'], grill['high'])
rule6 = ctrl.Rule(staff['many'] & orders['low'], grill['low'])
rule7 = ctrl.Rule(tables['high'] & orders['medium'] & staff['few'], grill['high'])
rule8 = ctrl.Rule(orders['medium'] & staff['adequate'], grill['medium'])


# creat control system
grill_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])


# select and create simulation
grilling = ctrl.ControlSystemSimulation(grill_ctrl)


# simulate up to 50 scenarios
for i in range(50):
    # input data
    grilling.input['tables'] = randint(0,30)
    grilling.input['staff'] = randint(0,6)
    grilling.input['orders'] = randint(0,60)

    # compute
    grilling.compute()

    # print results if hit any rule
    result = grilling.output
    if result:
        print(result["grill"])


grill.view(sim=grilling)
plt.savefig('fuzzy_plot.png')
