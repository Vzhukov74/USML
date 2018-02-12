import pandas as pd
import numpy as np

df = pd.read_csv('data/mlbootcamp5_train.csv', sep=';', index_col='id')

'''
Задание 1
Сколько мужчин и женщин представлено в этом наборе данных? Не было дано расшифровки признака "пол"
(какому полу соответствует 1, а какому – 2 в признаке gender) – это определите, посмотрев также
на рост при разумном предположении, что в среднем мужчины выше (здесь и далее под средним
понимается среднее арифметическое).
'''
result1 = df.groupby(['gender'])['height'].mean()
print(result1)

men = 0
women = 0

tagForMen = 0
tagForWomen = 0

if result1[1] > result1[2]:
    print('gender = 1 это мужчины, а gender = 2 женщины')
    men = df['gender'].value_counts()[1]
    women = df['gender'].value_counts()[2]
    tagForMen = 1
    tagForWomen = 2
else:
    print('gender = 1 это женщины, а gender = 2 мужчины')
    men = df['gender'].value_counts()[2]
    women = df['gender'].value_counts()[1]
    tagForMen = 2
    tagForWomen = 1

print('Задание 1:')
print('всего мужчин - ' + str(men) + ', всего женщин - ' + str(women))

'''
Задание 2
Кто в среднем реже указывает, что употребляет алкоголь – мужчины или женщины?
'''
print('Задание 2:')
if df.query('gender == @tagForMen')['alco'].mean() > df.query('gender == @tagForWomen')['alco'].mean():
    print('мужчины в среднем реже указывают что употребляют алкоголь')
else:
    print('женщины в среднем реже указывают что употребляют алкоголь')

'''
Задание 3
Во сколько раз (округленно, round) процент курящих среди мужчин больше, чем процент
курящих среди женщин (по крайней мере, по этим анкетным данным)?
'''
result2 = df.groupby(['gender'])['smoke'].value_counts()

smokeMens = result2[tagForMen]
smokeWomens = result2[tagForWomen]

percentOfSmokeMens = (smokeMens[1] * 100) / (smokeMens[1] + smokeMens[0])
percentOfSmokeWomens = (smokeWomens[1] * 100) / (smokeWomens[1] + smokeWomens[0])

difference = percentOfSmokeMens / percentOfSmokeWomens

print('Задание 3:')
print('процент курящих среди мужчин больше чем у женщин на:')
print(difference)

'''
Задание 4
Вы наверняка заметили, что значения возраста какие-то странные.
Догадайтесь, в чём здесь измеряется возраст, и ответьте, на сколько
месяцев (примерно) отличаются медианные значения возраста курящих и некурящих.
'''
df['age_in_month'] = (df['age'] / 30)
result3 = df.groupby(['smoke'])['age_in_month'].median()

print('Задание 4:')
print('возраст курящих в среднем больше на:')
print(result3[1] - result3[0])

'''
Задание 5
В статье на Википедии про сердечно-сосудистый риск показана шкала SCORE для расчёта
риска смерти от сердечно-сосудистого заболевания в ближайшие 10 лет.
'''
df['age_years'] = (df['age_in_month'] / 12).astype('int64')

oldPeople = df.query('smoke == 1 & gender == @tagForMen & age_years >= 60 & age_years <= 60')

oldPeopleGroup1 = oldPeople.query('ap_hi < 120 & cholesterol == 1')['cardio'].value_counts()
oldPeopleGroup2 = oldPeople.query('ap_hi < 180 & ap_hi >= 160 & cholesterol == 1')['cardio'].value_counts()

proportionOfPatientsInOldPeopleGroup1 = oldPeopleGroup1[1] / (oldPeopleGroup1[0] + oldPeopleGroup1[1])
proportionOfPatientsInOldPeopleGroup2 = oldPeopleGroup2[1] / (oldPeopleGroup2[0] + oldPeopleGroup2[1])

print('Задание 5:')
print(proportionOfPatientsInOldPeopleGroup2 / proportionOfPatientsInOldPeopleGroup1)

'''
Задание 6
Постройте новый признак – BMI (Body Mass Index). Для этого надо вес в килограммах
поделить на квадрат роста в метрах. Нормальными считаются значения
BMI от 18.5 до 25. Выберите верные утверждения.
'''
print('Задание 6:')
df['bmi'] = (df['weight'] / (df['height'] / 100) ** 2)

print('медианное bmi')
print(df['bmi'].median())

print('среднее bmi для мужчин')
result4 = df.groupby(['gender'])['bmi'].mean()
print(result4[tagForMen])
print('среднее bmi для женщин')
print(result4[tagForWomen])

print('среднее bmi для здоровых')
result5 = df.groupby(['cardio'])['bmi'].mean()
print(result5[0])
print('среднее bmi для больных')
print(result5[1])

print('среднее bmi для здоровых и непьющих мужчин')
result6 = df.query('cardio == 0 & alco == 0').groupby(['gender'])['bmi'].mean()
print(result6[tagForMen])
print('среднее bmi для здоровых и непьющих женщин')
print(result6[tagForWomen])

'''
Задание 7
Можно заметить, что данные не особо-то чистые, много в них всякой "грязи" и неточностей.
Еще лучше мы это увидим, когда обсудим визуализацию данных.
'''

#r = pd.Series(df['height'])
#r.quantile(.025, .975)
#print(r)
