import logging
from . import data_loader, ml_models, app_utils, ml_plots
import numpy as np

logger = logging.getLogger(__name__)

def init_all_ml_models():
    """Loads & cleans up the dataset, and then trains and predicts
    the dataset with all the ML models.
    """
    logger.info("Initializing and training all ML models")
    df = data_loader.load_dataset()
    data_loader.cleanup_dataframe(df)
    train_and_predict_models(df)
    
def train_and_predict_models(df):
    """Trains, predicts, and then saves model, its metrics and
    the plot corresponding to it.

    Args:
        df (DataFrame): the full dataset
    """
    logger.info("Creating/Loading all ML Models")
    ml_models.train_and_predict_simple_lr(df)
    ml_models.train_and_predict_multiple_lr(df)
    ml_models.train_and_predict_dtr(df)
    ml_models.train_and_predict_knn(df)
    ml_models.train_and_predict_rf(df)
    ml_models.train_and_predict_xgb(df)
    logger.info("All ML Models ready to use now!")
    
def predict_new_player_value():
    """Starting point of predict new players transfer value.
    """
    logger.info("In Predict Player's Value section")
    app_utils.clear_cli()
    app_utils.clear_and_print_header("PL Transfer Evaluator - Predict Player's Value")
    show_predict_player_menu()
    try:
        choice = int(input("\nEnter input: "))
    except ValueError:
        print("Invalid choice, return to main menu.")
        logger.warning("Invalid choice added in main menu.")
    else:
        match choice:
            case 1:
                predict_new_player_value_slr()
            case 2:
                predict_new_player_value_mlr()
            case 3:
                predict_new_player_value_dtr()
            case 4:
                predict_new_player_value_knn()
            case 5:
                predict_new_player_value_rf()
            case 6:
                predict_new_player_value_xgb()
            case 7:
                pass
    
def show_predict_player_menu():
    """Displays the player prediction menu
    """
    print("1. Predict using simple linear regression")
    print("2. Predict using multiple linear regression")
    print("3. Predict using Decision Tree regressor")
    print("4. Predict using KNN regressor")
    print("5. Predict using random forest")
    print("6. Predict using XGBoost")
    print("7. Return to main menu.")
    
def predict_new_player_value_slr():
    """Predicts new players value via SLR
    """
    logger.info("Predicting new players value using simple "
                "linear regression model")
    while True:
        try:
            overall = int(input("Enter the player overall rating: "))
        except ValueError:
            print("Invalid input, try again.")
        else:
            break
    print("Predicting new player's transfer value...")
    ml_models.predict_player_value_slr(overall)
    input("...")
    
def predict_new_player_value_mlr():
    """Predicts new players value via MLR
    """
    logger.info("Predicting new players value using multiple "
                "linear regression model")
    mlr_feature_names = ml_models.get_mlr_feature_names()
    X = list()  
    for feature_name in mlr_feature_names:
        while True:
            try:
                feature_value = int(input(f"Enter value for {feature_name}: "))
            except ValueError:
                print("Invalid input, try again.")
            else:
                X.append(feature_value)
                break
    ml_models.predict_player_value_mlr(X)
    input("...")
    
def predict_new_player_value_dtr():
    """Predicts new players value via DTR
    """
    logger.info("Predicting new players value using Decision tree"
                "regressor model")
    dtr_feature_names = ml_models.get_dtr_feature_names()
    X = list()  
    for feature_name in dtr_feature_names:
        while True:
            try:
                feature_value = int(input(f"Enter value for {feature_name}: "))
            except ValueError:
                print("Invalid input, try again.")
            else:
                X.append(feature_value)
                break
    ml_models.predict_player_value_dtr(X)
    input("...")
    
def predict_new_player_value_knn():
    """Predicts new players value via KNN
    """
    logger.info("Predicting new players value using KNN model")
    knn_feature_names = ml_models.get_knn_feature_names()
    X = list()  
    for feature_name in knn_feature_names:
        while True:
            try:
                feature_value = int(input(f"Enter value for {feature_name}: "))
            except ValueError:
                print("Invalid input, try again.")
            else:
                X.append(feature_value)
                break
    ml_models.predict_player_value_knn(X)
    input("...")
    
def predict_new_player_value_rf():
    """Predicts new players value via random forest
    """
    logger.info("Predicting new players value using random forest model")
    rf_feature_names = ml_models.get_rf_feature_names()
    X = list()  
    for feature_name in rf_feature_names:
        while True:
            try:
                feature_value = int(input(f"Enter value for {feature_name}: "))
            except ValueError:
                print("Invalid input, try again.")
            else:
                X.append(feature_value)
                break
    ml_models.predict_player_value_rf(X)
    input("...")

def predict_new_player_value_xgb():
    """Predicts new players value via XGB
    """
    logger.info("Predicting new players value using XGBoost model")
    xgb_feature_names = ml_models.get_xgb_feature_names()
    X = list()  
    for feature_name in xgb_feature_names:
        while True:
            try:
                feature_value = int(input(f"Enter value for {feature_name}: "))
            except ValueError:
                print("Invalid input, try again.")
            else:
                X.append(feature_value)
                break
    ml_models.predict_player_value_xgb(X)
    input("...")
    
def display_ml_metrics():
    """Displays the metrics for all the ML models.
    """
    app_utils.clear_cli()
    app_utils.clear_and_print_header("PL Transfer Evaluator - Displaying All Metrics")
    logger.info("Displaying metrics for all the ML models")
    all_metrics_dict = ml_models.get_metrics_for_all_models()
    print(f"{'Model Name':<30} {'MSE':<30} {'RMSE':<25} {'MAE':<25} {'R2 Score':<15}")
    for metrics in all_metrics_dict.values():
        print(f"{metrics['model']:<30} {metrics['mse']:<30} {metrics['rmse']:<25}" 
              f"{metrics['mae']:<25} {metrics['r2']:<15}")
    input("\n...")
    
def show_plots():
    """Starting point of the show plots section
    """
    app_utils.clear_cli()
    app_utils.clear_and_print_header("PL Transfer Evaluator - Show Plot")
    show_plots_menu()
    try:
        choice = int(input("\nEnter input: "))
    except ValueError:
        print("Invalid choice, return to main menu.")
        logger.warning("Invalid choice added in main menu.")
    else:
        match choice:
            case 1:
                ml_plots.show_slr_scatter_plot()
            case 2:
                ml_plots.show_dt_plot_tree()
            case 3:
                ml_plots.show_knn_plot()
            case 4:
                ml_plots.show_rf_plot()
            case 5:
                ml_plots.show_xgb_plot()
            case 6:
                pass

def show_plots_menu():
    """Displays the show plot menu
    """
    print("1. Show simple linear regression scatter plot")
    print("2. Show decision tree plot")
    print("3. Show KNN plot")
    print("4. Show Random Forest plot")
    print("5. Show XGBoost plot")
    print("6. Return to main menu")
    