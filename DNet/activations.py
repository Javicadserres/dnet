import numpy as np 
from module import Base


class ReLU(Base):
    """
    Class for the ReLU activation function.
    """
    def __init__(self):
        self.type = 'ReLU'

    def forward(self, Z):
        """
        Computes the forward propagation.

        Parameters
        ----------
        Z : numpy.array
            Input of the ReLU function.

        Returns
        -------
        A : numpy.array
            Output of the ReLU function.
        """
        self.A = np.maximum(0, Z)

        return self.A

    def backward(self, dA):
        """
        Computes the backward propagation.

        Parameters
        ----------
        dA : numpy.array
            Gradients of the activation function output.

        Returns
        -------
        dZ : numpy.array
            Gradients of the activation function input.
        """
        dZ = dA * np.where(self.A <= 0, 0, 1)

        return dZ


class Sigmoid(Base):
    """
    Class for the Sigmoid activation function.
    """
    def __init__(self):
        self.type = 'Sigmoid'

    def forward(self, Z):
        """
        Computes the forward propagation.

        Parameters
        ----------
        Z : numpy.array
            Input of the ReLU function.

        Returns
        -------
        A : numpy.array
            Output of the ReLU function.
        """
        self.A = 1 / (1 + np.exp(- Z))

        return self.A

    def backward(self, dA):
        """
        Computes the backward propagation.

        Parameters
        ----------
        dA : numpy.array
            Gradients of the activation function output.

        Returns
        -------
        dZ : numpy.array
            Gradients of the activation function input.
        """
        dZ = dA * self.A * (1 - self.A)

        return dZ


class Tanh(Base):
    """
    Class for the Hyperbolic tangent activation function.
    """
    def __init__(self):
        self.type = 'Tanh'

    def forward(self, Z):
        """
        Computes the forward propagation.

        Parameters
        ----------
        Z : numpy.array
            Input of the ReLU function.

        Returns
        -------
        A : numpy.array
            Output of the ReLU function.
        """
        self.A = np.tanh(Z)

        return self.A

    def backward(self, dA):
        """
        Computes the backward propagation.

        Parameters
        ----------
        dA : numpy.array
            Gradients of the activation function output.

        Returns
        -------
        dZ : numpy.array
            Gradients of the activation function input.
        """
        dZ = dA * (1 - np.power(self.A, 2))

        return dZ


class LeakyReLU(Base):
    """
    Class for the LeakyReLU activation function.
    """
    def __init__(self):
        self.type = 'LeakyReLU'

    def forward(self, Z):
        """
        Computes the forward propagation.

        Parameters
        ----------
        Z : numpy.array
            Input of the ReLU function.

        Returns
        -------
        A : numpy.array
            Output of the ReLU function.
        """
        self.A = np.maximum(0, Z)

        return self.A

    def backward(self, dA):
        """
        Computes the backward propagation.

        Parameters
        ----------
        dA : numpy.array
            Gradients of the activation function output.

        Returns
        -------
        dZ : numpy.array
            Gradients of the activation function input.
        """
        dZ = dA * np.where(self.A <= 0, 0.01, 1)

        return dZ


class Softmax(Base):
    """
    Class for the Softmax activation function.
    """
    def __init__(self):
        self.type = 'Softmax'
        self.eps = 1e-15

    def forward(self, Z):
        """
        Computes the forward propagation.

        Parameters
        ----------
        Z : numpy.array
            Input of the ReLU function.

        Returns
        -------
        A : numpy.array
            Output of the ReLU function.
        """
        self.Z = Z

        t = np.exp(Z - np.max(Z, axis=0))
        self.A =  t / np.sum(t, axis=0, keepdims=True)

        return self.A

    def backward(self, dA):
        """
        Computes the backward propagation.

        Parameters
        ----------
        dA : numpy.array
            Gradients of the activation function output.

        Returns
        -------
        dZ : numpy.array
            Gradients of the activation function input.
        """
        n, m = self.A.shape

        matrix1 = np.einsum('ji,ki->jki', self.A, self.A) 
        matrix2 = np.einsum('ji,jk->jki', self.A, np.eye(n, n))

        dSoftmax = matrix2 - matrix1
        dZ = np.einsum('jki,ki->ji', dSoftmax, dA)
        
        return dZ