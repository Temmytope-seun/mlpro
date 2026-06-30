import os
import sys
from src.exception import CustomException
from src.logger import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    transformed_train_path: str=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()
    def get_transformer(self):
        try:
            num_features = ['reading_score', 'writing_score']
            cat_features = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
           
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info('Categorical encoding completed')
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, num_features),
                    ("cat_pipeline", cat_pipeline, cat_features),        
                ])
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
            
    def initiate_data_transformation(self,train_path,test_path):
        logging.info('Data Transformation Begins')
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and data completed")
            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_transformer()

            target_col_name="math_score"
            num_cols = ['reading_score', 'writing_score']

            input_feature_train_df=train_df.drop(columns=[target_col_name],axis=1)
            target_feature_train_df=train_df[target_col_name]

            input_feature_test_df=test_df.drop(columns=[target_col_name],axis=1)
            target_feature_test_df=test_df[target_col_name]

            logging.info('Applying preprocessing on train and test sets')

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info('Saved preprocessing object')

            save_object(self.transformation_config.transformed_train_path, preprocessing_obj)

            return(train_arr, test_arr, self.transformation_config.transformed_train_path )

        except Exception as e:
            raise CustomException(e,sys)

