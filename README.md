# Traffic Sign Classification Model

## URL
https://youtu.be/9TWygyE1vZY

## Design Choice
2 convolutional layers
- The image size is small, 30x30, so any more convolutional + pooling layers would over-reduce the area size to capture meaningful shapes.
- 2 layer convolutions would be able to capture more complex shapes than just a single layer.

2 wide hidden layers
- The hidden layers are a multiple of the number of categories, to be able to better classify each category.
- The depth of the hidden layers is kept shallow to only 2, to reduce the number of training parameters, since the number of categories is large.

Output layer
- The output layer has the same number of nodes as the number of categories.
- This allows a SOFTMAX() activation to be applied to compute classification probabilities.

Dropout
- Dropout not applied on the convolutional layers, so that shape information is not lost in training, given that the sample size is small.
- High (50%) dropout is applied on the dense layers to regularise the large number of parameters.

Activation
- RELU() activation is chosen for computational efficiency.

Weight initialisation
- He Kai Ming weight initialisations are used given the choice of RELU() activations.  

Train metrics
- Categorical accuracy is used given the multi-categorical classification nature of the problem.

## Convolutional Neural Network Summary

```sh
=================================================================
conv2d (Conv2D)              (None, 28, 28, 32)        896       
_________________________________________________________________
activation (Activation)      (None, 28, 28, 32)        0         
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 14, 14, 32)        0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 12, 12, 32)        9248      
_________________________________________________________________
activation_1 (Activation)    (None, 12, 12, 32)        0         
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 6, 6, 32)          0         
_________________________________________________________________
flatten (Flatten)            (None, 1152)              0         
_________________________________________________________________
dense (Dense)                (None, 688)               793264    
_________________________________________________________________
activation_2 (Activation)    (None, 688)               0         
_________________________________________________________________
dropout (Dropout)            (None, 688)               0         
_________________________________________________________________
dense_1 (Dense)              (None, 344)               237016    
_________________________________________________________________
activation_3 (Activation)    (None, 344)               0         
_________________________________________________________________
dropout_1 (Dropout)          (None, 344)               0         
_________________________________________________________________
dense_2 (Dense)              (None, 43)                14835     
_________________________________________________________________
activation_4 (Activation)    (None, 43)                0         
=================================================================
Total params: 1,055,259
Trainable params: 1,055,259
Non-trainable params: 0
_________________________________________________________________
```