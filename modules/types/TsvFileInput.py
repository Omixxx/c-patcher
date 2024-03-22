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
