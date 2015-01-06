from __future__ import absolute_import, print_function, division


# fieldmap()
############

from petl import fieldmap, look
table1 = [['id', 'sex', 'age', 'height', 'weight'],
          [1, 'male', 16, 1.45, 62.0],
          [2, 'female', 19, 1.34, 55.4],
          [3, 'female', 17, 1.78, 74.4],
          [4, 'male', 21, 1.33, 45.2],
          [5, '-', 25, 1.65, 51.9]]
from collections import OrderedDict
mappings = OrderedDict()
# rename a field
mappings['subject_id'] = 'id'
# translate a field
mappings['gender'] = 'sex', {'male': 'M', 'female': 'F'}
# apply a calculation to a field
mappings['age_months'] = 'age', lambda v: v * 12
# apply a calculation to a combination of fields
mappings['bmi'] = lambda rec: rec['weight'] / rec['height']**2
# transform and inspect the output
table2 = fieldmap(table1, mappings)
look(table2)


# rowmap()
##########


from petl import rowmap, look
table1 = [['id', 'sex', 'age', 'height', 'weight'],
          [1, 'male', 16, 1.45, 62.0],
          [2, 'female', 19, 1.34, 55.4],
          [3, 'female', 17, 1.78, 74.4],
          [4, 'male', 21, 1.33, 45.2],
          [5, '-', 25, 1.65, 51.9]]
def rowmapper(row):
    transmf = {'male': 'M', 'female': 'F'}
    return [row[0],
            transmf[row['sex']] if row['sex'] in transmf else None,
            row.age * 12,
            row.height / row.weight ** 2]

table2 = rowmap(table1, rowmapper,
                fields=['subject_id', 'gender', 'age_months', 'bmi'])
look(table2)


# rowmapmany()
##############

from petl import rowmapmany, lookall
table1 = [['id', 'sex', 'age', 'height', 'weight'],
          [1, 'male', 16, 1.45, 62.0],
          [2, 'female', 19, 1.34, 55.4],
          [3, '-', 17, 1.78, 74.4],
          [4, 'male', 21, 1.33]]
def rowgenerator(row):
    transmf = {'male': 'M', 'female': 'F'}
    yield [row[0], 'gender',
           transmf[row['sex']] if row['sex'] in transmf else None]
    yield [row[0], 'age_months', row.age * 12]
    yield [row[0], 'bmi', row.height / row.weight ** 2]

table2 = rowmapmany(table1, rowgenerator,
                    fields=['subject_id', 'variable', 'value'])
lookall(table2)


