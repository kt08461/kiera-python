# =============================================================================
# 分析110學年大專院校學生數據
# 3張圖 各自顯示
# =============================================================================
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
from django.shortcuts import render
from io import BytesIO

TitleFont = {'fontsize':16, 'fontweight':'bold'}

def studentsMain(request):

    # 統計國立、私立學校數量
    cntSchools()

    # 統計男、女學生人數
    cntGender()

    # 統計各縣市有多少學校
    cntSchoolsByCity()

    # 統計各縣市男、女學生人數
    cntGenderByCity()

    return render(request, "students.html", context)

def init_data():
    def setImgFont():
        plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
    setImgFont()

    file_path="static/data/110_student.csv"
    df = pd.read_csv(file_path, header=0,dtype={'學校代碼':str})
    df = df.applymap(lambda x: x.replace(',',''))
    df = df.applymap(lambda x: x.replace('-','0'))

    for c in df.columns[4:-2]:
        df[c] = df[c].astype('int')

    return df

# 統計國立、私立學校數量
def cntSchools():
    df = df110.groupby(by='學校名稱', as_index=False).sum(numeric_only=True)
    df_n = df[df['學校名稱'].str.contains('國立')]
    df_p = df[~df['學校名稱'].str.contains('國立')]
    context["sch_pub"] = len(df_n)
    context["sch_pri"] = len(df_p)
    context["sch_total"] = len(df_n)+len(df_p)
    
    imgStudents(df_n, df_p)

def imgStudents(df_n, df_p):
    def img_text(p, x):
        t = int(round(p/100.*sum(x)))
        return f'{p:.1f}%\n( {t:,} 人 )'
    
    pie_radius = 1.2
    pie_size = 0.5
    X = np.array([[df_n['男生計'].sum(), df_n['女生計'].sum()], [df_p['男生計'].sum(), df_p['女生計'].sum()]])
    L1 = ['公立學校', '私立學校']
    L2 = ['男生', '女生']

    fig = plt.figure(figsize=(8,5))
    plt.title('公、私立學生人數比例', weight = 'bold', fontdict=TitleFont)    
    plt.gca().axis("equal")
    ax = plt.gca()

    cmap = plt.get_cmap("tab20")
    outer_colors = cmap(np.array([2, 4]))
    inner_colors = cmap(np.array([1, 13, 1, 13]))
    
    # 外層環狀(第一圈)
    wg1, texts, autotexts = ax.pie(X.sum(axis=1), labels= L1, radius=pie_radius, colors=outer_colors, pctdistance=0.8,
            autopct=lambda i: img_text(i, X.sum(axis=1)),
            textprops=dict(color="k", size="large"), wedgeprops=dict(width=pie_size, edgecolor='w'))
    # 內層環狀(第二圈)
    wg2, texts, autotexts = ax.pie(X.flatten(), radius=pie_radius-pie_size, colors=inner_colors, pctdistance=0.5,
            autopct=lambda i: img_text(i, X.flatten()),
            textprops=dict(color="k", size="smaller"), wedgeprops=dict(width=pie_size, edgecolor='w'))
    plt.legend(wg1+wg2[:2], L1+L2, fontsize = 'large', loc='best')
    context["plot_students"] = imgBase64(fig)

# 統計男、女學生人數
def cntGender():
    context["stud_male"] = df110[df110.columns[5]].sum()
    context["stud_female"] = df110[df110.columns[6]].sum()
    context["stud_total"] = format(context["stud_male"] + context["stud_female"], ',')
    context["stud_male"] = format(context["stud_male"], ',')
    context["stud_female"] = format(context["stud_female"], ',')

# 統計各縣市有多少學校
def cntSchoolsByCity():
    df_city_u = df110.groupby(by=['縣市名稱','學校名稱'],
                            as_index=False).sum(numeric_only=True)
    df_city = df_city_u.groupby(by='縣市名稱').count()
    df_city = pd.DataFrame(df_city['學校名稱'])
    df_city.columns=['學校數量']
    df_city.index = df_city.index.str[3:]

    imgSchoolsByCity(df_city)

# 長條圖: 各縣市學校數量
def imgSchoolsByCity(df):
    X = [i for i in range(len(df))]
    Y = list(df['學校數量'])

    # 長條圖
    fig = plt.figure(figsize=(10,5))
    ax = plt.gca()
    ax.set_title('各縣市學校數量', TitleFont, va='baseline')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # 加文字
    plt.bar(X, Y)
    for x, y in zip(X, Y):
        plt.text(x, y+0.05, '%d' % y, ha='center', va='bottom')

    plt.xticks(X,df.index, rotation=90)
    plt.ylabel('學校數量')
    context["plot_schools"] = imgBase64(fig)

# 統計各縣市男、女學生人數
def cntGenderByCity():
    df_gender = df110.groupby(by=['縣市名稱']).sum(numeric_only=True).loc[:,["總計","男生計","女生計"]]
    df_gender.index = df_gender.index.str[3:]
    
    imgGenderByCity(df_gender)

# 長條圖: 各縣市男、女學生人數
def imgGenderByCity(df):
    bar_width = 0.8
    M = np.arange(0, len(df)*2, 2)
    F = M+bar_width

    # 設定bar的圖型
    fig = plt.figure(figsize=(13,5))
    ax = plt.gca()
    ax.set_title('各縣市男、女學生人數', TitleFont)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    lm = plt.bar(M, df['男生計'], bar_width, fc="#0080FF")
    lf = plt.bar(F, df['女生計'], bar_width, fc='#ff9999')

    # 加文字
    for x, y in zip(M, df['男生計']):
        plt.text(x, y, '{:,}'.format(y), ha='center', va='bottom', rotation=80, 
                  bbox=dict(boxstyle="round",ec='None',fc='#D0D0D0', alpha=0.3))
    for x, y in zip(F, df['女生計']):
        plt.text(x, y, '{:,}'.format(y), ha='left', va='bottom', rotation=80,
                  bbox=dict(boxstyle="round",ec='None',fc='#D0D0D0', alpha=0.3))

    plt.xticks(M+bar_width/2,df.index, rotation=90)
    plt.ylabel('學生人數')
    plt.legend(handles=[lm,lf], labels=['男生','女生'], fontsize = 'large', loc='best')
    plt.grid(True)
    context["plot_city_students"] = imgBase64(fig)

# 圖檔轉Base64
def imgBase64(fig):
    img_fp = BytesIO()
    fig.savefig(img_fp, format='png', bbox_inches='tight')
    img_b64 = base64.encodebytes(img_fp.getvalue()).decode()
    img_b64 = 'data:image/png;base64,' + str(img_b64)

    return img_b64

context = {'plot':{}}
df110 = init_data()