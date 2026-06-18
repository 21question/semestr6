#Cell 1. Импорты
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings

warnings.filterwarnings('ignore')

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    StratifiedKFold
)

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

#Cell 2. Загрузка данных
df = pd.read_csv('Titanic-Dataset.csv')

df.head()


#Cell 3. Первичный анализ
print(df.shape)

print(df.columns.tolist())

df.info()

df['Survived'].value_counts(dropna=False)


#Cell 4. Визуализация
print('Доля выживших:', df['Survived'].mean())


fig, axes = plt.subplots(1,3, figsize=(18,4))

sns.histplot(df['Age'], bins=30, ax=axes[0])
axes[0].set_title('Age')

sns.histplot(df['Fare'], bins=30, ax=axes[1])
axes[1].set_title('Fare')

sns.histplot(df['Pclass'], bins=3, ax=axes[2])
axes[2].set_title('Passenger class')

plt.tight_layout()
plt.show()


#Сравнение выживаемости
fig, axes = plt.subplots(1,2, figsize=(12,4))

sns.barplot(
    x='Sex',
    y='Survived',
    data=df,
    ax=axes[0]
)

axes[0].set_title('Survival by Sex')


sns.barplot(
    x='Pclass',
    y='Survived',
    data=df,
    ax=axes[1]
)

axes[1].set_title('Survival by Passenger class')

plt.show()


#Cell 5. Подготовка признаков
df_model = df.copy()

drop_cols = [
    'PassengerId',
    'Name',
    'Ticket',
    'Cabin'
]

df_model = df_model.drop(
    columns=[c for c in drop_cols if c in df_model.columns]
)

X = df_model.drop(columns=['Survived'])

y = df_model['Survived']


#Числовые и категориальные признаки
numeric_features = [
    'Age',
    'Fare',
    'SibSp',
    'Parch'
]

categorical_features = [
    'Sex',
    'Embarked',
    'Pclass'
]


#Cell 6. Трансформеры
numeric_transformer = Pipeline(steps=[

    ('imputer',
     SimpleImputer(strategy='median')),

    ('scaler',
     StandardScaler())

])


categorical_transformer = Pipeline(steps=[

    ('imputer',
     SimpleImputer(strategy='most_frequent')),

    ('onehot',
     OneHotEncoder(
         drop='first',
         handle_unknown='ignore'
     ))

])


preprocessor = ColumnTransformer(

    transformers=[

        (
            'num',
            numeric_transformer,
            numeric_features
        ),

        (
            'cat',
            categorical_transformer,
            categorical_features
        )

    ]

)


#Cell 7. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.25,

    random_state=42,

    stratify=y

)

print(X_train.shape)

print(X_test.shape)

print(y_train.mean())

print(y_test.mean())


#Cell 8. Pipeline + GridSearch
pipe = Pipeline(steps=[

    ('preprocessor', preprocessor),

    ('clf',
     LogisticRegression(
         solver='liblinear',
         max_iter=1000
     ))

])


param_grid = {

    'clf__penalty':

        ['l1','l2'],

    'clf__C':

        [0.01,0.1,1,10],

    'clf__class_weight':

        [None,'balanced']

}


cv = StratifiedKFold(

    n_splits=5,

    shuffle=True,

    random_state=42

)


grid = GridSearchCV(

    pipe,

    param_grid,

    cv=cv,

    scoring='roc_auc',

    n_jobs=-1,

    verbose=1

)


grid.fit(X_train,y_train)


print(grid.best_params_)

print(grid.best_score_)


#Cell 9. Оценка модели
best_model = grid.best_estimator_


y_pred = best_model.predict(X_test)

y_proba = best_model.predict_proba(X_test)[:,1]


print('Accuracy:',

      accuracy_score(y_test,y_pred))

print('Precision:',

      precision_score(y_test,y_pred))

print('Recall:',

      recall_score(y_test,y_pred))

print('F1:',

      f1_score(y_test,y_pred))

print('ROC AUC:',

      roc_auc_score(y_test,y_proba))


print(classification_report(
    y_test,
    y_pred
))


#Матрица ошибок
cm = confusion_matrix(
    y_test,
    y_pred
)

plt.figure(figsize=(5,4))

sns.heatmap(

    cm,

    annot=True,

    fmt='d',

    cmap='Blues',

    xticklabels=['Died','Survived'],

    yticklabels=['Died','Survived']

)

plt.xlabel('Predicted')

plt.ylabel('Actual')

plt.title('Confusion Matrix')

plt.show()


#Cell 10. ROC и PR
fpr, tpr, _ = roc_curve(
    y_test,
    y_proba
)

precision, recall, _ = precision_recall_curve(
    y_test,
    y_proba
)

avg_prec = average_precision_score(
    y_test,
    y_proba
)


plt.figure(figsize=(12,5))


plt.subplot(1,2,1)

plt.plot(

    fpr,

    tpr,

    label=f'AUC={roc_auc_score(y_test,y_proba):.3f}'

)

plt.plot([0,1],[0,1],'k--')

plt.legend()

plt.title('ROC Curve')



plt.subplot(1,2,2)

plt.plot(

    recall,

    precision,

    label=f'AP={avg_prec:.3f}'

)

plt.legend()

plt.title('Precision Recall Curve')


plt.tight_layout()

plt.show()


#Cell 11. Коэффициенты модели
preproc = best_model.named_steps['preprocessor']

ohe = preproc.named_transformers_['cat'].named_steps['onehot']

cat_names = ohe.get_feature_names_out(
    categorical_features
)

feature_names = np.concatenate(

    [

        numeric_features,

        cat_names

    ]

)


coefs = best_model.named_steps['clf'].coef_[0]


coef_df = pd.DataFrame({

    'feature': feature_names,

    'coef': coefs

})


coef_df['odds_ratio'] = np.exp(

    coef_df['coef']

)


coef_df = coef_df.sort_values(

    by='coef',

    ascending=False

)


coef_df


#Cell 12. Подбор порога
thresholds = np.linspace(

    0,

    1,

    101

)


f1_scores = [

    f1_score(

        y_test,

        (y_proba>=t).astype(int)

    )

    for t in thresholds

]


best_idx = np.argmax(f1_scores)

best_thresh = thresholds[best_idx]


print(best_thresh)

print(f1_scores[best_idx])


#Cell 13. Вероятности
probas_df = X_test.copy()

probas_df['y_true'] = y_test

probas_df['proba_survive'] = y_proba


probas_df = probas_df.sort_values(

    'proba_survive',

    ascending=False

)

probas_df.head(20)


#Cell 14. Сохранение модели
joblib.dump(

    best_model,

    'logreg_titanic_pipeline.joblib'

)

print('Model saved')
