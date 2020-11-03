import pandas as pd

# df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
#                    index=['row 1', 'row 2'],
#                    columns=['col 1', 'col 2'])

# data = pd.read_excel("51jobs.xlsx", sheet_name='51job')
# # print(data.__dict__)
# print(data.loc[0])
# print(data.columns)
# print(data.items)
# print(data.index)
# data.loc[1] = ['a', 'b']
# data.loc[2] = ['c', 'd']
# df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
#                    index=['row 1', 'row 2'],
#                    columns=['col 1', 'col 2'])
df1 = pd.DataFrame([['a', 'b'], ['c', 'd']])
df1.append(['11', '222'])
with pd.ExcelWriter('51jobs_111.xlsx') as writer:  # doctest: +SKIP
    df1.to_excel(writer, sheet_name='51job')
    # df2.to_excel(writer, sheet_name='Sheet_name_2')
