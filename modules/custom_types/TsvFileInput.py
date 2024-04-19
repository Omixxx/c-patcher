class TsvFileInput:
    def __init__(
        self,
        name: str,
        startLine: int,
        endLine: int,
        classPath: str,
        readabilityScore: float,
        label: str,
        originalMethod: str,
        abstractMethod: str,
        model_prediction: str,
        is_diff: str,
        partially_detokenized_method: str,
        detokenized_method: str,
        predictions_readability_score: str,
        does_test_suite_pass: str,
        does_contain_errors: str,
        manual_readability_score: str,
    ):
        self.name = name
        self.startLine = startLine
        self.endLine = endLine
        self.classPath = classPath
        self.readabilityScore = readabilityScore
        self.label = label
        self.originalMethod = originalMethod
        self.abstractMethod = abstractMethod
        self.model_prediction = model_prediction
        self.is_diff = is_diff
        self.partially_detokenized_method = partially_detokenized_method
        self.detokenized_method = detokenized_method
        self.predictions_readability_score = predictions_readability_score
        self.does_test_suite_pass = does_test_suite_pass
        self.does_contain_errors = does_contain_errors
        self.manual_readability_score = manual_readability_score

    @staticmethod
    def attributes_as_list_of_strings() -> list[str]:
        return [
            "name",
            "startLine",
            "endLine",
            "classPath",
            "readabilityScore",
            "label",
            "originalMethod",
            "abstractMethod",
            "model_prediction",
            "is_diff",
            "partially_detokenized_method",
            "detokenized_method",
            "predictions_readability_score",
            "does_test_suite_pass",
            "does_contain_errors"
            "manual_readability_score"
        ]
