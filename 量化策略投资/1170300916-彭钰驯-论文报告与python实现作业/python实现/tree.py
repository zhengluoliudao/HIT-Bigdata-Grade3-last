# 实战数据
# 导入数据
import pandas as pd
df = pd.read_excel('./客户信息及违约表现.xlsx')

# 提取特征变量和目标变量
X = df.drop(columns='是否违约')
# X = df.drop('是否违约', axis=1)
y = df['是否违约']

# 模型搭建
# 将数据集拆分为训练数据和测试数据
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# 实例化模型对象
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=3)

# 训练：将模型对象与训练数据拟合
clf = clf.fit(X_train, y_train)
print(clf)  

# 模型预测
# 测试：根据测试数据预测分类
y_pred = clf.predict(X_test)
print(y_pred)

# 预测不违约&违约结果比较
a = pd.DataFrame()  
a['预测值'] = list(y_pred)
a['实际值'] = list(y_test)
print(a.tail())

from sklearn.metrics import accuracy_score
score = accuracy_score(y_pred, y_test)

# 预测不违约&违约概率
y_pred_proba = clf.predict_proba(X_test)

print(y_pred_proba[:5,:])  
print(y_pred_proba[:5, 0])
print(y_pred_proba[:5, 1])

# 模型预测效果评估
# ROC曲线
from sklearn.metrics import roc_curve
fpr, tpr, thres = roc_curve(y_test.values, y_pred_proba[:, 1])

a = pd.DataFrame()
a['阈值'] = list(thres)
a['假警报率'] = list(fpr)
a['命中率'] = list(tpr)
print(a)

# 绘制ROC曲线
import matplotlib.pyplot as plt
plt.plot(fpr, tpr)
plt.show()

# AUC值
from sklearn.metrics import roc_auc_score
score = roc_auc_score(y_test.values, y_pred_proba[:, 1])
print(score)
