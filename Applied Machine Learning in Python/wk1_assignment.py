def answer_one():
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures

    # Your code here
    poly3 = PolynomialFeatures(degree=3)
    poly6 = PolynomialFeatures(degree=6)
    poly9 = PolynomialFeatures(degree=9)
    X_train_poly3 = poly3.fit_transform(X_train.reshape(11,-1))
    X_train_poly6 = poly6.fit_transform(X_train.reshape(11,-1))
    X_train_poly9 = poly9.fit_transform(X_train.reshape(11,-1))
    
    LG1 = LinearRegression().fit(X_train.reshape(11,-1), y_train.reshape(11,-1))
    LG3 = LinearRegression().fit(X_train_poly3.reshape(11,-1), y_train.reshape(11,-1))
    LG6 = LinearRegression().fit(X_train_poly6.reshape(11,-1), y_train.reshape(11,-1))
    LG9 = LinearRegression().fit(X_train_poly9.reshape(11,-1), y_train.reshape(11,-1))
    x_axis1 = np.linspace(0,10,100).reshape(100,-1)
    x_axis3 = poly3.fit_transform(x_axis1)
    x_axis6 = poly6.fit_transform(x_axis1)
    x_axis9 = poly9.fit_transform(x_axis1)
    y_axis1 = LG1.predict(x_axis1)
    y_axis3 = LG3.predict(x_axis3)
    y_axis6 = LG6.predict(x_axis6)
    y_axis9 = LG9.predict(x_axis9)
    result = np.concatenate((y_axis1, y_axis3, y_axis6, y_axis9), axis = 1).T
    return result # Return your answer
  
  
def answer_two():
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.metrics.regression import r2_score

    # Your code here
    r2_train = np.array([])
    r2_test = np.array([])
    for i in range(10):
        poly = PolynomialFeatures(degree=i)
        X_train_poly = poly.fit_transform(X_train.reshape(11,-1))
        X_test_poly = poly.fit_transform(X_test.reshape(4,-1))
        LG = LinearRegression().fit(X_train_poly.reshape(11,-1), y_train.reshape(11,-1))
        r2_train = np.append(r2_train, LG.score(X_train_poly.reshape(11,-1), y_train.reshape(11,-1))).reshape(10,-1)
        r2_test = np.append(r2_test, LG.score(X_test_poly.reshape(4,-1), y_test.reshape(4,-1))).reshape(10,-1)
    return (r2_train, r2_test) # Your answer here
