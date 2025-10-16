  #clean_data{normal , raw , clear , correlation}
'''
Normalize dataframe features and making them to datetime & number depending on the situation
نرمالسازی ویژکی های دیتافریم و تبدیل به زمان و عدد بسته به شرایط
'''
def normal(feature , to=None , fillna_method=None):
    import pandas as pd
    import numpy as np
    if to == 'date': #تبدیل به تاریخ
        feature = feature.astype(str).str.strip().str.replace("'", "").str.replace('"', '')
        def parse_date(val):
            val = val.strip()
            if val.lower() in ['nan', 'none', '', 'null']:
                return pd.NaT
            elif val.isdigit() and len(val) == 8:
                return pd.to_datetime(val, format='%Y%m%d', errors='coerce')
            else:
                return pd.to_datetime(val, errors='coerce')
        feature = feature.apply(parse_date)
        if fillna_method == 'mean':
            timestamps = feature.view(np.int64)
            na_indices = np.where(pd.isna(feature))[0]
            for idx in na_indices:
                prev_idx = idx - 1
                next_idx = idx + 1
                prev_val = None
                next_val = None
                while prev_idx >= 0:
                    if not pd.isna(feature.iloc[prev_idx]):
                        prev_val = feature.iloc[prev_idx]
                        break
                    prev_idx -= 1
                while next_idx < len(feature):
                    if not pd.isna(feature.iloc[next_idx]):
                        next_val = feature.iloc[next_idx]
                        break
                    next_idx += 1
                if prev_val is not None and next_val is not None:
                    prev_num = prev_val.toordinal()
                    next_num = next_val.toordinal()
                    mean_num = int((prev_num + next_num) / 2)
                    feature.iloc[idx] = pd.Timestamp.fromordinal(mean_num)
                elif prev_val is not None:
                    feature.iloc[idx] = prev_val
                elif next_val is not None:
                    feature.iloc[idx] = next_val
                else:
                    pass
        elif fillna_method == 'mode':
            mode = feature.mode()[0]
            feature = feature.fillna(mode)
        return feature
    elif to == 'num': #تبدیل به عدد
        feature = feature.astype(str).str.replace(r'[^0-9\-.]', '', regex=True).replace(['','-'],np.nan).astype(float)
        if fillna_method == 'mean':
            mean_num = feature.mean()
            feature = feature.fillna(mean_num)
        elif fillna_method == 'mode':
            mode = feature.mode()[0]
            feature = feature.fillna(mode)
        elif fillna_method == 'median':
            median = feature.median()
            feature = feature.fillna(median)
        return feature
    elif to==None:
        if fillna_method == 'mean':
            mean_num = feature.mean()
            feature = feature.fillna(mean_num)
        elif fillna_method == 'mode':
            mode = feature.mode()[0]
            feature = feature.fillna(mode)
        elif fillna_method == 'median':
            median = feature.median()
            feature = feature.fillna(median)


'''
normal(feature , to , fillna_method) -> feature: فیچر مدنظر , to: تاریخ یا عدد , fillna_method: با چی پر بشه خالیا
'''
#*********************************************************************************
'''
Showing dataframe features and checking noises
نمایش ویژگی های خام دیتافریم و بررسی نویزها
'''
def raw(df):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    for feature in df.columns:
        sns.boxplot(df[feature])
        sns.swarmplot(df[feature])
        plt.savefig(f'raw_{feature}.png' , dpi=300)
    sns.boxplot(data=df , palette='Set2')
    plt.savefig('raw_features.png' , dpi=300)
'''
raw(df) -> df: دیتافریم مدنظر
'''
#*********************************************************************************
'''
Clearing datas , dropping duplicates , if needed removing missing records , removing noises and showing cleared features
تمیز کردن داده ها، پاک کردن تکراری ها، درصورت نیاز پاک کردن سطرهای خالی، پاک کردن نویزها و نمایش ویژگی های تمیز شده
'''
def clear(df , big_data=None):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    df.drop_duplicates(inplace=True) # پاک کردن تکراری‌ها
    if big_data=='y':
        df.dropna(inplace=True)
    elif big_data==None:
        pass
    ls=[]
    features = df.columns.tolist()
    while True:
        outliers_indices = []
        for feature in features:
            if pd.api.types.is_numeric_dtype(df[feature]):
                q1 = df[feature].quantile(.25)
                q3 = df[feature].quantile(.75)
                iqr = q3 - q1
                lbound = q1 - 1.5 * iqr
                ubound = q3 + 1.5 * iqr
                outliers = df.index[(df[feature] < lbound) | (df[feature] > ubound)].tolist()
                outliers_indices.extend(outliers)
        outliers_indices = sorted(set(outliers_indices))
        if len(outliers_indices) == 0:
            break
        df = df.drop(outliers_indices)
    df.reset_index(drop=True , inplace=True)
    for feature in df.columns:
        plt.figure(figsize=(10, 5))
        sns.boxplot(x=df[feature])
        sns.swarmplot(x=df[feature], color='red', alpha=0.5)
        plt.title(f'Boxplot of {feature}')
        plt.savefig(f'clear_{feature}.png', dpi=300)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, palette='Set2')
    plt.savefig('clear_features.png', dpi=300)
    return df
'''
clear(df , big_data) -> df: دیتافریم مدنظر , big_data: بیگ دیتا هست یا نه؟ اگه هست 'y'!
'''
#*********************************************************************************
'''
Correlation of features of dataframe
رابطه بین ویژگی های دیتافریم
'''
def correlation(df):
    import pandas as pd
    import plotly.express as px
    from prq.file import file_to_excel
    df_num = df.select_dtypes(include='number').corr()
    fig = px.imshow(df , title='HeatMap Correlation')
    fig.write_image('features_correlation.png')
    file_to_excel(df_num , 'features_correlation.xlsx')
'''
correlation(df) -> df: دیتافریم مدنظر
'''
#*********************************************************************************

'''
Github: https://github.com/ahkiyani
Linkedin: https://www.linkedin.com/in/amirhossein-kiyani1381
G-mail: https://amirho3einkiyani.2002@gmail.com
'''
