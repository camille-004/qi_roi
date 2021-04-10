#%%
import pandas as pd

fp = 'data/ucsd/UCSDCoursedata.csv'
drop_cols = ['Unnamed: 0', 'instr', 'evals', 'time']

df = pd.read_csv(fp)
df = df.drop(columns=drop_cols)

eng_courses = ['AESE', 'BENG', 'CENG', 'CSE', 'DSC', 'ECE', 'ENG', 'NANO',
               'SE', 'WES']

eng_df = df[df['course'].str.contains('|'.join(eng_courses))]
