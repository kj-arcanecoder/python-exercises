import joblib
import logging
import numpy as np
import os
from . import ml_plots
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/')
data_models_path = os.path.join(base_dir, '../data/models/')
data_metrics_path = os.path.join(base_dir, '../data/metrics/')

slr_model_path = f"{data_models_path}linear_regression_model.joblib"
mlr_model_path = f"{data_models_path}mutiple_linear_regression_model.joblib"
dtr_model_path = f"{data_models_path}decision_tree_model.joblib"
knn_model_path = f"{data_models_path}knn_model.joblib"
rf_model_path = f"{data_models_path}rf_model.joblib"
xgb_model_path = f"{data_models_path}xgb_model.joblib"

mlr_scaler_path = f"{data_path}mutiple_linear_regression_scaler.joblib"
knn_scaler_path = f"{data_path}knn_scaler.joblib"

def train_and_predict_simple_lr(df):
    """Trains, predicts, generates metrics, plots and saves the SLR Model.

    Args:
        df (DataFrame): The players full dataset
    """
    try:
        lr_model = joblib.load(slr_model_path)
    except FileNotFoundError:
        logger.info("No linear regression model found, creating new")
        logger.info("Fetching best feature for linear regression model")
        
        corr_features = get_sorted_corr_features(df)
        best_feature = corr_features.index[0]    
        X = df[best_feature].to_numpy().reshape(-1,1)
        y = df['value_eur'].to_numpy()
        
        logger.info("Splitting & training the linear regression")
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42)
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        
        logger.info("Predicting the linear regression model")
        y_pred = lr_model.predict(X_test)
        store_metrics("simple_linear_regression", y_test, y_pred)
        ml_plots.plot_slr_scatter(lr_model, X_test, y_test)
        
        logger.info("Saving the linear regression model")
        joblib.dump(lr_model, slr_model_path)
    else:
        logger.info("Existing linear regression model found!")
        
def train_and_predict_multiple_lr(df):
    """Trains, predicts, generates metrics and saves the MLR Model.

    Args:
        df (DataFrame): The players full dataset
    """
    try:
        mlr_model = joblib.load(mlr_model_path)
    except FileNotFoundError:
        logger.info("No multiple linear regression model found, creating new")
        logger.info("Fetching best feature for multiple linear regression")
        
        best_features = get_best_corr_features(df)
        X = df.loc[:,best_features].to_numpy()
        y = df['value_eur'].to_numpy()
        
        scaler = StandardScaler()
        X_std = scaler.fit_transform(X)
        
        logger.info("Splitting & training the multiple linear regression")
        X_train, X_test, y_train, y_test = train_test_split(
            X_std, 
            y, 
            test_size=0.2, 
            random_state=42)
        mlr_model = LinearRegression()
        mlr_model.feature_names_ = best_features
        mlr_model.fit(X_train, y_train)
        
        logger.info("Predicting the multiple linear regression model")
        y_pred = mlr_model.predict(X_test)
        store_metrics("multiple_linear_regression", y_test, y_pred)
        
        logger.info("Saving the multiple linear regression model")
        joblib.dump(mlr_model, mlr_model_path)
        joblib.dump(scaler, mlr_scaler_path)
    else:
        logger.info("Existing multiple linear regression model found!")
        
def train_and_predict_dtr(df):
    """Trains, predicts, generates metrics, plots and saves the DTR Model.

    Args:
        df (DataFrame): The players full dataset
    """
    try:
        dtr_model = joblib.load(dtr_model_path)
    except FileNotFoundError:
        logger.info("No decision tree regressor model found, creating new")
        logger.info("Fetching best feature for decision tree regressor")
        
        best_features = get_best_corr_features(df)
        X = df.loc[:,best_features].to_numpy()
        y = df['value_eur'].to_numpy()
        
        logger.info("Splitting & training the decision tree regressor")
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42)
        dtr_model = DecisionTreeRegressor(criterion = 'squared_error',
                               max_depth=8,
                               min_samples_leaf=2, 
                               random_state=42)
        dtr_model.feature_names_ = best_features
        dtr_model.fit(X_train, y_train)
        
        logger.info("Predicting the decision tree regressor model")
        y_pred = dtr_model.predict(X_test)
        store_metrics("decision_trees_regression", y_test, y_pred)
        ml_plots.plot_dt_plot_tree(dtr_model)
        
        logger.info("Saving the decision tree regressor model")
        joblib.dump(dtr_model, dtr_model_path)
    else:
        logger.info("Existing decision tree regressor model found!")

def train_and_predict_knn(df):
    """Trains, predicts, generates metrics, plots and saves the KNN Model.

    Args:
        df (DataFrame): The players full dataset
    """
    try:
        knn_model = joblib.load(knn_model_path)
    except FileNotFoundError:
        logger.info("No KNN model found, creating new")
        logger.info("Fetching best feature for KNN regressor")
        
        best_features = get_best_corr_features(df)
        X = df.loc[:,best_features].to_numpy()
        y = df['value_eur'].to_numpy()
        
        scaler = StandardScaler()
        X_std = scaler.fit_transform(X)
        
        logger.info("Splitting & training the KNN regressor")
        X_train, X_test, y_train, y_test = train_test_split(
            X_std, 
            y, 
            test_size=0.2, 
            random_state=42)
        
        k = 10
        knn_model = KNeighborsRegressor(n_neighbors=k)
        knn_model.feature_names_ = best_features
        knn_model.fit(X_train, y_train)
        
        logger.info("Predicting the KNN regressor model")
        y_pred = knn_model.predict(X_test)
        store_metrics("k_nearest_neighbors", y_test, y_pred)
        
        Ks, r2s, r2s_std = generate_plot_data_for_knn(X_train, X_test, y_train, y_test)
        ml_plots.plot_knn(Ks, r2s, r2s_std)
        
        logger.info("Saving the KNN regressor model")
        joblib.dump(knn_model, knn_model_path)
        joblib.dump(scaler, knn_scaler_path)
    else:
        logger.info("Existing KNN regressor model found!")

def generate_plot_data_for_knn(X_train, X_test, y_train, y_test):
    """Generates data needed for plotting KNN.

    Args:
        X_train (np array): Input features training data
        X_test (np array): Input features test data
        y_train (np array): Training target values
        y_test (np array): Test target values

    Returns:
        _type_: _description_
    """
    logger.info("Generating plot data for KNN")
    Ks = 100
    r2s = np.zeros((Ks))
    r2s_std = np.zeros((Ks))
    for n in range(1,Ks+1):
        knn_model_n = KNeighborsRegressor(n_neighbors = n).fit(X_train,y_train)
        yhat = knn_model_n.predict(X_test)
        r2s[n-1] = r2_score(y_test, yhat)
        r2s_std[n-1] = np.std(yhat==y_test)/np.sqrt(yhat.shape[0])
    return Ks,r2s,r2s_std

def train_and_predict_rf(df):
    """Trains, predicts, generates metrics, plots and saves the RF Model.

    Args:
        df (DataFrame): The players full dataset
    """
    try:
        rf_model = joblib.load(rf_model_path)
    except FileNotFoundError:
        logger.info("No RF model found, creating new")
        logger.info("Fetching best feature for random forest")
        
        best_features = get_best_corr_features(df)
        X = df.loc[:,best_features].to_numpy()
        y = df['value_eur'].to_numpy()
        
        logger.info("Splitting & training the random forest")
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42)
        
        n_estimators = 100
        rf_model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        rf_model.feature_names_ = best_features
        rf_model.fit(X_train, y_train)
        
        logger.info("Predicting the random forest model")
        y_pred = rf_model.predict(X_test)
        store_metrics("random_forest", y_test, y_pred)
        ml_plots.plot_random_forest(y_test, y_pred)
        
        logger.info("Saving the random forest model")
        joblib.dump(rf_model, rf_model_path)
    else:
        logger.info("Existing random forest model found!")
        
def train_and_predict_xgb(df):
    """Trains, predicts, generates metrics, plots and saves the XGB Model.

    Args:
        df (DataFrame): The players full dataset
    """
    try:
        xgb_model = joblib.load(xgb_model_path)
    except FileNotFoundError:
        logger.info("No XGBoost model found, creating new")
        logger.info("Fetching best feature for XGBoost")
        
        best_features = get_best_corr_features(df)
        X = df.loc[:,best_features].to_numpy()
        y = df['value_eur'].to_numpy()
        
        logger.info("Splitting & training the XGBoost")
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42)
        
        n_estimators = 100
        xgb_model = XGBRegressor(n_estimators=n_estimators, random_state=42)
        xgb_model.feature_names_ = best_features
        xgb_model.fit(X_train, y_train)
        
        logger.info("Predicting the XGBoost model")
        y_pred = xgb_model.predict(X_test)
        store_metrics("xgboost", y_test, y_pred)
        ml_plots.plot_xgboost(y_test, y_pred)
        
        logger.info("Saving the XGBoost model")
        joblib.dump(xgb_model, xgb_model_path)
    else:
        logger.info("Existing XGBoost model found!")

def get_best_corr_features(df):
    """Gets the best correlated features from the dataframe.

    Args:
        df (DataFrame): The full dataset

    Returns:
        List: best correlated features
    """
    corr_features = get_sorted_corr_features(df)
    best_features = [corr_features.index[i] for i in range(0,len(corr_features)) 
                         if corr_features[i] > 0.2]
    return best_features
        

def get_sorted_corr_features(df):
    """Sorts all features on the basis of corr values

    Args:
        df (DataFrame): The full dataset

    Returns:
        List: sorted correlated features
    """
    corr_series = (
        df.corr()['value_eur']
          .drop('value_eur')
          .sort_values(ascending=False)
    )
    return corr_series

def predict_player_value_slr(overall):
    """Predicts the player's value using SLR

    Args:
        overall (int): overall feature from the dataset
    """
    X_test = np.array([overall]).reshape(-1,1)
    logger.info("Predicting new player's value using linear regression")
    lr_model = joblib.load(slr_model_path)
    y_pred = lr_model.predict(X_test)
    print("Player's predicted transfer value using Linear Regression is " 
          f"{y_pred[0]:,.2f}")
    
def get_mlr_feature_names():
    """Gets the feature name from MLR

    Returns:
        List: input features trained with this model. 
    """
    return joblib.load(mlr_model_path).feature_names_

def get_dtr_feature_names():
    """Gets the feature name from DTR

    Returns:
        List: input features trained with this model. 
    """
    return joblib.load(dtr_model_path).feature_names_

def get_knn_feature_names():
    """Gets the feature name from KNN

    Returns:
        List: input features trained with this model. 
    """
    return joblib.load(knn_model_path).feature_names_

def get_rf_feature_names():
    """Gets the feature name from random forest

    Returns:
        List: input features trained with this model. 
    """
    return joblib.load(rf_model_path).feature_names_

def get_xgb_feature_names():
    """Gets the feature name from XGB

    Returns:
        List: input features trained with this model. 
    """
    return joblib.load(xgb_model_path).feature_names_

def predict_player_value_mlr(X):
    """Predicts the player's value using MLR

    Args:
        X (np array): input features of the player to be tested.
    """
    X_test = np.array(X).reshape(1,-1)
    logger.info("Predicting player's value using multiple linear regression")
    
    mlr_model = joblib.load(mlr_model_path)
    scaler = joblib.load(mlr_scaler_path)
    
    X_test_std = scaler.transform(X_test)
    y_pred = mlr_model.predict(X_test_std)
    print("Player's predicted transfer value using multiple Linear " 
          f"Regression is {y_pred[0]:,.2f}")
    
def predict_player_value_dtr(X):
    """Predicts the player's value using DTR

    Args:
        X (np array): input features of the player to be tested.
    """
    X_test = np.array(X).reshape(1,-1)
    logger.info("Predicting player's value using decision tree regressor")
    
    dtr_model = joblib.load(dtr_model_path)
    
    y_pred = dtr_model.predict(X_test)
    print("Player's predicted transfer value using decision tree " 
          f"regressor is {y_pred[0]:,.2f}")
    
def predict_player_value_knn(X):
    """Predicts the player's value using KNN

    Args:
        X (np array): input features of the player to be tested.
    """
    X_test = np.array(X).reshape(1,-1)
    logger.info("Predicting player's value using KNN regressor")
    
    knn_model = joblib.load(knn_model_path)
    
    scaler = joblib.load(knn_scaler_path)
    X_test_std = scaler.transform(X_test_std)
    y_pred = knn_model.predict(X_test)
    print("Player's predicted transfer value using KNN " 
          f"regressor is {y_pred[0]:,.2f}")
    
def predict_player_value_rf(X):
    """Predicts the player's value using RF

    Args:
        X (np array): input features of the player to be tested.
    """
    X_test = np.array(X).reshape(1,-1)
    logger.info("Predicting player's value using random forest")
    
    rf_model = joblib.load(rf_model_path)
    
    y_pred = rf_model.predict(X_test)
    print("Player's predicted transfer value using random " 
          f"forest is {y_pred[0]:,.2f}")
    
def predict_player_value_xgb(X):
    """Predicts the player's value using XGB

    Args:
        X (np array): input features of the player to be tested.
    """
    X_test = np.array(X).reshape(1,-1)
    logger.info("Predicting player's value using XGBoost")
    
    xgb_model = joblib.load(xgb_model_path)
    
    y_pred = xgb_model.predict(X_test)
    print("Player's predicted transfer value using XGBoost " 
          f"is {y_pred[0]:,.2f}")
    
def store_metrics(ml_model_name, y_test, y_pred):
    """Stores the model scores for a model in a joblib file

    Args:
        ml_model_name (str): name of the model
        y_test (np array): Test target values 
        y_pred (_type_): Predicted target values
    """
    metrics = {
    "model": ml_model_name,
    "r2": "{0:.3f}".format(r2_score(y_test, y_pred)),
    "mae": "{0:.3f}".format(mean_absolute_error(y_test, y_pred)),
    "mse": "{0:.3f}".format(mean_squared_error(y_test, y_pred)),
    "rmse": "{0:.3f}".format(np.sqrt(mean_squared_error(y_test, y_pred)))
    }
    joblib.dump(metrics, f"{data_metrics_path}{metrics['model']}.joblib")

def get_metrics_for_all_models():
    """Gets the metric scores for all the models, stores and returns it
    in a dictionary

    Returns:
        dict: metric scores for all the models
    """
    all_metrics_dict = dict()
    slr_metrics = joblib.load(f'{data_metrics_path}simple_linear_regression.joblib')
    all_metrics_dict[slr_metrics['model']] = slr_metrics
    
    mlr_metrics = joblib.load(f'{data_metrics_path}multiple_linear_regression.joblib')
    all_metrics_dict[mlr_metrics['model']] = mlr_metrics
    
    dtr_metrics = joblib.load(f'{data_metrics_path}decision_trees_regression.joblib')
    all_metrics_dict[dtr_metrics['model']] = dtr_metrics
    
    knn_metrics = joblib.load(f'{data_metrics_path}k_nearest_neighbors.joblib')
    all_metrics_dict[knn_metrics['model']] = knn_metrics
    
    rf_metrics = joblib.load(f'{data_metrics_path}random_forest.joblib')
    all_metrics_dict[rf_metrics['model']] = rf_metrics
    
    xgb_metrics = joblib.load(f'{data_metrics_path}xgboost.joblib')
    all_metrics_dict[xgb_metrics['model']] = xgb_metrics
    
    return all_metrics_dict
    