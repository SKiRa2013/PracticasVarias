from Src.adaline import AdalineLayer
import numpy as np
import numpy.typing as npt

class SigmoidLayer(AdalineLayer):
    error: npt.NDArray[np.float16]
    
    def __init__(self, input_size, feature_size, learning_constant, neurons) -> None:
        super().__init__(input_size, feature_size, learning_constant, neurons)
        self.error = np.zeros((input_size, neurons), dtype=np.float16)

    def sigmoid(self, matrix: npt.NDArray[np.float16]) -> npt.NDArray[np.float16]:
        return 1 / 1 + np.exp(-matrix)
    
    def activation(self, inputs: npt.NDArray[np.float16]) -> npt.NDArray[np.float16]:
        return self.sigmoid(np.dot(inputs, self.weight) + self.bias)

    def delta_output(self, error: npt.NDArray[np.float16], result: npt.NDArray[np.float16]) -> npt.NDArray[np.float16]:
        return error * result * (1 - result)

    def calculate_error(self) -> None:
        pass

class SigmoidOutputLayer(SigmoidLayer):
    def __init__(self, input_size, feature_size, learning_constant, neurons):
        super().__init__(input_size, feature_size, learning_constant, neurons)

    def calculate_error(self, expected_result: npt.NDArray[np.float16], result: npt.NDArray[np.float16]):
        return expected_result - result    

class SigmoidHiddenLayer(SigmoidLayer):
    def __init__(self, input_size, feature_size, learning_constant, neurons):
        super().__init__(input_size, feature_size, learning_constant, neurons)

    def calculate_error(self, delta_output: npt.NDArray[np.float16], connected_weights: npt.NDArray[np.float16]):
        return np.outer(delta_output, connected_weights)
        

class MLPerceptron:
    
    def __init__(self):
        pass



if __name__ == "__main__":
    pass