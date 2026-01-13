import logging
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.tree import plot_tree

logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_plots_path = os.path.join(base_dir, '../data/plots/')

slr_scatter_path = f'{data_plots_path}slr_scatter.png'
dt_plot_tree_path = f'{data_plots_path}dt_plot_tree.png'
knn_plot_path = f'{data_plots_path}knn_plot.png'
rf_plot_path = f'{data_plots_path}rf_plot.png'
xgb_plot_path = f'{data_plots_path}xgb_plot.png'

def plot_slr_scatter(lr_model, X_test, y_test):
    """Generates a plot for simple linear regression model result over
    test data.

    Args:
        lr_model (LinearRegression): linear regression model
        X_test (np array): Input test features
        y_test (np array): Test target values
    """
    logger.info("Generating scatter plot for simple linear regression")
    plt.figure()
    plt.scatter(X_test, y_test, color='blue')
    plt.plot(X_test, lr_model.coef_ * X_test + lr_model.intercept_, '-r')
    plt.savefig(slr_scatter_path)
    plt.close()
    
def show_slr_scatter_plot():
    """Gets the existing SLR scatter plot
    """
    logger.info("Fetching existing simple linear regression plot")
    show_existing_plot(slr_scatter_path)
    
def show_existing_plot(plot_path):
    """Generic function to fetch existing plot of any ML model

    Args:
        plot_path (str): path of the saved plot
    """
    img = mpimg.imread(plot_path)
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    
def plot_dt_plot_tree(dt_model):
    """Generates a plot tree for the decision tree

    Args:
        dt_model (DecisionTreeRegressor): DT model
    """
    logger.info("Generating decision tree regressor plot tree")
    plt.figure()
    plot_tree(dt_model)
    plt.savefig(dt_plot_tree_path)
    plt.close()
    
def show_dt_plot_tree():
    """Gets the existing DT scatter plot
    """
    logger.info("Fetching existing decision tree regressor plot tree")
    show_existing_plot(dt_plot_tree_path)
    
def plot_knn(Ks, r2s, r2s_std):
    """Plots the model R2 score corresponding to K value

    Args:
        Ks (int): max range of K value
        r2s (np array): Array of R2 scores for all values of K
        r2s_std (np array): Standard deviation of R2 scores for 
        all values of K
    """
    logger.info("Generating KNN scatter plot")
    plt.figure()
    plt.plot(range(1,Ks+1),r2s,'g')
    plt.fill_between(range(1,Ks+1),r2s - 1 * r2s_std,r2s + 1 * r2s_std, alpha=0.10)
    plt.legend(('R2 value', 'Standard Deviation'))
    plt.ylabel('Model R2')
    plt.xlabel('Number of Neighbors (K)')
    plt.savefig(knn_plot_path)
    plt.close()
    
def show_knn_plot():
    """Gets the existing KNN plot
    """
    logger.info("Fetching existing KNN plot")
    show_existing_plot(knn_plot_path)
    
def plot_random_forest(y_test, y_pred):
    """Generates a random forest scatter plot

    Args:
        y_test (np array): Test target values
        y_pred (np array): Predicted target values
    """
    logger.info("Generating random forest scatter plot")
    plt.figure()
    plt.scatter(y_test, y_pred, alpha=0.5, color="blue",ec='k')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2,label="perfect model")
    plt.title("Random Forest Predictions vs Actual")
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.legend()
    plt.savefig(rf_plot_path)
    plt.close()
    
def show_rf_plot():
    """Gets the existing random forest plot
    """
    logger.info("Fetching existing random forest plot")
    show_existing_plot(rf_plot_path)

def plot_xgboost(y_test, y_pred):
    """Generates a XGBoost scatter plot

    Args:
        y_test (np array): Test target values
        y_pred (np array): Predicted target values
    """
    logger.info("Generating XGBoost scatter plot")
    plt.figure()
    plt.scatter(y_test, y_pred, alpha=0.5, color="blue",ec='k')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2,label="perfect model")
    plt.title("XGBoost Predictions vs Actual")
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.legend()
    plt.savefig(xgb_plot_path) 
    plt.close()   
    
def show_xgb_plot():
    """Gets the existing XGBoost plot
    """
    logger.info("Fetching existing XGBoost plot")
    show_existing_plot(xgb_plot_path)