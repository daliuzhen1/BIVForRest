import tornado.ioloop
import tornado.web
import pymongo
from handler.mlsklearn.model_selection.model_selection_handler import TrainTestSplitHandler
from handler.mlsklearn.regression.linear_regression_handler import *
from handler.data_source_handler import DataSourceHandler
from handler.data_handler import DataObjHandler
from data.persistence import init_dir

def make_app():
    return tornado.web.Application([
        (r"/DataSource", DataSourceHandler),
        (r"/Data", DataObjHandler),
        (r"/sklearn/modelSelection/trainTestSplit", TrainTestSplitHandler),
        (r"/sklearn/regression/linearRegression", LinearRegressionHandler),
        (r"/sklearn/regression/linearRegression/fit", LinearRegressionFitHandler),
        (r"/sklearn/regression/linearRegression/Attributes", LinearRegressionAttributesHandler),
        (r"/sklearn/regression/linearRegression/Parameters", LinearRegressionParametersHandler),
        (r"/sklearn/regression/linearRegression/predict", LinearRegressionPredictHandler),
        (r"/sklearn/regression/linearRegression/score", LinearRegressionScoreHandler),
    ])

if __name__ == "__main__":
    init_dir()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()