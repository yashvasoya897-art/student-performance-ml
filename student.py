import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

data={
    "Hour": [1,2,3,4,5,6,7,8],
    "Attendance": [55,60,65,70,75,80,85,90],
    "Assignment": [40,45,50,55,65,70,75,85],
    "Pass": [0,0,0,0,1,1,1,1]

}
df=pd.DataFrame(data)

X=df[["Hour","Attendance","Assignment"]]
y=df[["Pass"]]

X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.2
)

model= LogisticRegression()
model.fit(X_train,y_train)

prediction=model.predict(X_test)

accuracy = accuracy_score(y_test,prediction)

print("Accuracy", accuracy)
print("Prediction", prediction)


# New Student Data Add(Prediction)

new_student = [[5,75,70]]
result=model.predict(new_student)

if result[0]==1:
    print("New Student Result: Pass")
else:
    print("New Student Result: fail")