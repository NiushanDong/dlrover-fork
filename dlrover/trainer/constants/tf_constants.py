from dlrover.trainer.constants.constants import Constant
class TFConstants(object):
    """Platform related constants"""

    PlatformName = Constant("Platform")
    EstimatorClassifier = Constant("estimator")
    ClassifierTypeEstimator = Constant("estimator", "estimator")
    EstimatorClassifierType = Constant(
        "classifier_type", ClassifierTypeEstimator()
    )
    EstimatorClassifierClass = Constant(
        "classifier_class", ClassifierTypeEstimator()
    )
    SessionConfig = Constant("session_config")
    RunConfig = Constant("run_config")
    LogSteps = Constant("log_steps", 100)
    BatchSize  = Constant("log_steps", 64)
    EstimatorTrainingChiefHooks = Constant("training_chief_hooks")
    EstimatorTrainingHooks = Constant("training_hooks")
    EstimatorPredictionHooks = Constant("prediction_hooks")
    EstimatorEvaluationHooks = Constant("evaluation_hooks")
    Epoch = Constant("epoch", 1)
    LogSteps = Constant("log_steps", 100)
    SaveSteps = Constant("save_steps", 100)
    EvalSteps = Constant("eval_steps", 100)
    MaxSteps = Constant("max_steps")
    SaveMinSecs = Constant("save_min_secs", 0)
    SaveMaxSecs = Constant("save_max_secs", 3600 * 24 * 5)
    EvalMinSecs = Constant("eval_min_secs", 0)
    EvalMaxSecs = Constant("eval_max_secs", 3600 * 24 * 5)
    ModelDir = Constant("model_dir")
    ANY_NODE_FO_LEVEL = Constant(1)
    EstimatorTrainingChiefHooks = Constant("training_chief_hooks")
    EstimatorTrainingHooks = Constant("training_hooks")
    EstimatorPredictionHooks = Constant("prediction_hooks")
    EstimatorEvaluationHooks = Constant("evaluation_hooks")