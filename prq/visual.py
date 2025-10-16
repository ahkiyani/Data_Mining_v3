#visual{chart , feature_charts}
'''
Chart of dataframe and chosen feature
نمودار دیتافریم و ویژگی های انتخابی
'''
def chart(df, a=None, aname=None, b=None, bname=None):
    import matplotlib.pyplot as plt
    import pandas as pd
    if a is None and b is None:
        df.plot()
        plt.title('data_chart')
        plt.savefig('data_chart.png', dpi=300)
        plt.show()
    else:
        x = df[a] if a in df.columns else a
        y = df[b] if b in df.columns else b
        if isinstance(x, pd.Series) and isinstance(y, pd.Series):
            grouped = df.groupby(a)[b].sum().reset_index()
            x = grouped[a]
            y = grouped[b]
        plt.figure(figsize=(12,5))
        ax1 = plt.subplot(2, 2, 1)
        df.plot(ax=ax1)
        plt.title('Data_Chart')
        plt.subplot(2, 2, 2)
        plt.bar(x, y)
        plt.xlabel(aname if aname else a)
        plt.ylabel(bname if bname else b)
        plt.title('Bar Chart')
        plt.subplot(2, 2, 3)
        plt.pie(y, labels=x, autopct='%1.1f%%')
        plt.title('Pie Chart')
        plt.subplot(2,2,4)
        plt.plot(x , y , marker='*' ,c="#F10000" , ms=4 , ls='' , lw=1) #نمودار بصورت نقطه چین و با رنگ قرمز
        plt.title('c')
        plt.xlabel(aname if aname else a)
        plt.ylabel(bname if bname else b)
        plt.tight_layout()
        plt.savefig(f'{aname}_{bname}_diagram.png',dpi=300)

'''
chart(df,a,aname,b,bname) -> df: دیتافریم مدنظر , a: فیچر اول , aname: نام فیچر اول , b: فیچر دوم , bname: نام فیچر دوم
'''
#*********************************************************************************
'''
Three charts of each feature to analysis
سه نمودار از هر ویژگی برای تحلیل
'''
def feature_charts(df):
    import plotly.express as px
    from plotly.subplots import make_subplots
    for feature in df.columns:
        fig = make_subplots(rows=1, cols=3, subplot_titles=[
            f"{feature} Frequency",
            f"{feature} Box Plot",
            f"{feature} Index frequency"
        ])
        hist = px.histogram(df, x=feature)
        for trace in hist.data:
            fig.add_trace(trace, row=1, col=1)
        box = px.box(df, y=feature)
        for trace in box.data:
            fig.add_trace(trace, row=1, col=2)
        kde = px.histogram(df, x=feature, marginal="rug", histnorm='density', nbins=30)
        for trace in kde.data:
            fig.add_trace(trace, row=1, col=3)
        fig.update_layout(
            width=1200,
            height=400,
            title_text=f"Three charts for feature: {feature}"
        )
        fig.write_image(f"{feature}_three_charts.png")
'''
feature_charts(df) -> df: دیتافریم مدنظر
'''
#*********************************************************************************
'''
Github: https://github.com/ahkiyani
Linkedin: https://www.linkedin.com/in/amirhossein-kiyani1381
G-mail: https://amirho3einkiyani.2002@gmail.com
'''
