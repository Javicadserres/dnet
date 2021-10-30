from dnet.layers.recurrent import RNNCell
import numpy as np
import dnet

from dnet.layers import (
    LinearLayer,
    ConstantPad, 
    Conv2D, 
    MaxPooling2D, 
    AveragePooling2D, 
    RNNCell
)
from .test_utils import (
    test_parameters_linearlayer, 
    test_parameters_convolution, 
    test_parameters_rnncell
)


def test_linearlayer():
    """
    Tests the linear layer class.
    """
    weights, bias, A, dZ = test_parameters_linearlayer()

    layer = LinearLayer(3, 2)
    layer.weights = weights
    layer.bias = bias

    expected_Z = np.array([[-13.], [50.5]])
    expected_dA = np.array([[4.5],[3.], [7.6]])

    obtained_Z = layer.forward(A)
    obtained_dA = layer.backward(dZ)

    np.testing.assert_almost_equal(expected_Z, obtained_Z)
    np.testing.assert_almost_equal(expected_dA, obtained_dA)


def test_paddinglayer():
    """
    Tests padding layer class.
    """
    X = np.array([[1, 1, 1], [1, 1, 1]])
    
    expected = np.array(
        [[0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]]
    )
    padding = 1
    dimension = 2
    constant = 0
    padclass = ConstantPad(padding, dimension, constant)
    obtained = padclass.pad(X)

    np.testing.assert_almost_equal(expected, obtained)


def test_conv2d():
    """
    Test Convolutional 2D layer class.
    """
    image, weights, bias = test_parameters_convolution()

    expected_Z = np.array(
        [[[[17]], [[26]], [[11]], [[ 5]]],
        [[[39]], [[32]], [[28]], [[ 8]]],
        [[[29]], [[46]], [[24]], [[17]]],
        [[[43]], [[49]], [[50]], [[29]]]]
    )
    expected_dA = np.array(
        [[[[326.]], [[475.]], [[296.]], [[159.]]],
        [[[488.]], [[555.]], [[491.]], [[201.]]],
        [[[522.]], [[798.]], [[628.]], [[378.]]],
        [[[316.]], [[392.]], [[370.]], [[190.]]]]
    )
    expected_dW = np.array(
        [[[[771, 927, 626], [833, 1200, 739], [529, 749, 569]]]]
    )
    expected_db = np.array([[453]])

    in_channels = 1
    out_channels = 1
    kernel_size = (3, 3)
    stride = 1
    padding = 1
    
    convolution = Conv2D(
        in_channels, out_channels, kernel_size, stride, padding
    )
    convolution.weights = weights
    convolution.bias = bias

    obtained_Z = convolution.forward(image)
    obtained_dA = convolution.backward(obtained_Z)
    obtained_dW = convolution.dW
    obtained_db = convolution.db

    np.testing.assert_almost_equal(expected_Z, obtained_Z)
    np.testing.assert_almost_equal(expected_dA, obtained_dA)
    np.testing.assert_almost_equal(expected_dW, obtained_dW)
    np.testing.assert_almost_equal(expected_db, obtained_db)


def test_maxpooling2d():
    """
    Tests Max pooling layer class.
    """
    image, _, _ = test_parameters_convolution()

    expected_Z = np.array(
        [[[[4]], [[4]]], [[[4]], [[4]]]]
    )
    expected_dA = np.array(
        [[[[ 0.]], [[ 8.]], [[ 0.]], [[ 0.]]],
        [[[ 0.]], [[ 0.]], [[ 0.]], [[ 0.]]],
        [[[ 8.]], [[16.]], [[ 0.]], [[ 0.]]],
        [[[ 4.]], [[ 0.]], [[ 8.]], [[ 0.]]]]
    )

    kernel_size = (3, 3)
    stride = 1
    padding = 0

    convolution = MaxPooling2D(kernel_size, stride, padding)

    obtained_Z = convolution.forward(image)
    obtained_dA = convolution.backward(obtained_Z)

    np.testing.assert_almost_equal(expected_Z, obtained_Z)
    np.testing.assert_almost_equal(expected_dA, obtained_dA)


def test_averagepooling2d():
    """
    Tests Max pooling layer class.
    """
    image, _, _ = test_parameters_convolution()

    expected_Z = np.array([[[[2.11111111]]]])
    expected_dA = np.array(
        [[[[0.2345679]], [[0.2345679]], [[0.2345679]], [[0.]]],
        [[[0.2345679]], [[0.2345679]], [[0.2345679]], [[0.]]],
        [[[0.2345679]], [[0.2345679]], [[0.2345679]], [[0.]]],
        [[[0.]], [[0.]], [[0.]], [[0.]]]]
    )

    kernel_size = (3, 3)
    stride = 2
    padding = 0

    convolution = AveragePooling2D(kernel_size, stride, padding)

    obtained_Z = convolution.forward(image)
    obtained_dA = convolution.backward(obtained_Z)

    np.testing.assert_almost_equal(expected_Z, obtained_Z)
    np.testing.assert_almost_equal(expected_dA, obtained_dA)


def test_rnncell():
    """
    Tests the RNNCell class.
    """
    input = np.array([[0.86540763], [-2.3015387]])
    hidden = np.zeros((2, 1))
    combined = np.concatenate((input, hidden), axis=0)
    weights, dZ = test_parameters_rnncell()

    expected_hidden = np.array([[0.88682355], [0.99527661]])
    expected_d_hidden = np.array([[-0.10465545], [-0.19716043]])

    input_dim = 2
    hidden_dim = 2

    recurrent = RNNCell(input_dim, hidden_dim)
    recurrent.lineal.weights = weights

    obtained_hidden = recurrent.forward(input, hidden)
    obtained_d_hidden = recurrent.backward(
        dZ=dZ, hidden=obtained_hidden, combined=combined
    )

    np.testing.assert_almost_equal(expected_hidden, obtained_hidden)
    np.testing.assert_almost_equal(expected_d_hidden, obtained_d_hidden)   