#dTree{dTree}
'''
Making a Decision Tree model of data
ساخت یک درخت تصمیم از داده
'''
def dTree(df , X , classifier ,  meghias , tree_depth):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px
    import warnings
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.tree import plot_tree
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn import metrics
    warnings.filterwarnings('ignore')
    X_trainset , X_testset , y_trainset , y_testset = train_test_split(X , classifier , test_size=0.3 , random_state=3)
    classifierTree = DecisionTreeClassifier(criterion=meghias , max_depth=tree_depth)
    classifierTree.fit(X_trainset , y_trainset)
    predTree = classifierTree.predict(X_testset)
    accuracy = metrics.accuracy_score(y_testset ,predTree)
    featureNames = df.columns
    fig = plt.figure(figsize=(10 ,20))
    out = plot_tree(classifierTree , feature_names=featureNames , class_names=np.unique(y_trainset) , filled=True , rounded=True,)
    plt.title(f'Decision Tree of data with {accuracy} accuracy!')
    plt.savefig('Decision_Tree.png' , dpi=300)
    plt.show()
'''
dTree(df , X , classifier , meghias , depth_tree) -> df: کل دیتاریم مدنظ , X: قسمت ورودی و کم اهمیت تره دیتا , classifier: کلسیفایر* ,
meghias: مقیاس *entropy/gini , depth_tree: ارتفاع درخت که معمولا یکی کمتر از فیچرها میگیریم
'''
#*********************************************************************************
'''
Github: https://github.com/ahkiyani
Linkedin: https://www.linkedin.com/in/amirhossein-kiyani1381
G-mail: https://amirho3einkiyani.2002@gmail.com
'''
