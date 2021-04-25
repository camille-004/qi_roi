#%%
import pandas as pd
import plotly.express as px
import plotly.io as pio

fp = 'data/ucsd/UCSDCoursedata.csv'
drop_cols = ['Unnamed: 0', 'instr', 'evals', 'time']

df = pd.read_csv(fp)
df = df.drop(columns=drop_cols)

eng_courses = ['AESE', 'BENG', 'CENG', 'CSE', 'DSC', 'ECE', 'ENG', 'NANO',
               'SE', 'WES']

eng_df = df[df['course'].str.contains('|'.join(eng_courses))]
#%%
all_course_names = eng_df['course'].str.split().str[0]
hist = px.histogram(all_course_names)
hist.show()
#%%
traces = list()
for course in all_course_names.unique():
    curr = eng_df[eng_df['course'].str.contains(course)]
    traces.append(px.Box(data=curr, y=curr['rcmnd_class']))

