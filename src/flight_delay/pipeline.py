"""
This is a boilerplate pipeline
generated using Kedro 0.18.1
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    predict,
    report_evaluator,
    select_cols,
    feature_engineering,
    make_pyspark_pipeline,
    split_data,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=select_cols,
                inputs=["flights", "parameters"],
                outputs="flights_reduced",
                name="select_cols",
            ),
            node(
                func=feature_engineering,
                inputs=["flights_reduced", "parameters"],
                outputs="flights_extra",
                name="feature_engineering",
            ),
            node(
                func=split_data,
                inputs=["flights_extra", "parameters"],
                outputs=[
                    "data_train",
                    "data_test",
                ],
                name="split",
            ),
            node(
                func=make_pyspark_pipeline,
                inputs=["data_train", "parameters"],
                outputs="pipeline_classifier",
                name="fit_pipeline",
            ),
            node(
                func=predict,
                inputs=["data_test", "pipeline_classifier", "parameters"],
                outputs="test_with_pred",
                name="transform_test",
            ),
            node(
                func=report_evaluator,
                inputs=["test_with_pred", "parameters"],
                outputs=None,
                name="report_accuracy",
            ),
        ]
    )
