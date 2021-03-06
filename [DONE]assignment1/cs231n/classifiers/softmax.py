import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  for i in xrange(num_train):
    scores = X[i].dot(W)
    scores -= np.max(scores) # solve numeric instability
    scores = np.exp(scores)
    scores_normalized = scores/float(np.sum(scores)) # probabilities
        
    loss += -np.log(scores_normalized[y[i]])
        
    dW_update_term = np.outer(X[i], scores_normalized)
    dW_update_term[:, y[i]] -= 1*X[i]
    dW += dW_update_term
        
  
  # Average loss, gradient over examples
  loss /= num_train 
  dW /= num_train
  # Regularization loss, gradient
  loss += 0.5*reg*np.sum(W*W)
  dW += reg*W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = X.dot(W)
  num_train = X.shape[0]
  scores -= np.row_stack(np.max(scores, 1)) # solve numeric instability
  scores = np.exp(scores)
  scores /= np.row_stack(np.sum(scores, 1)).astype(float)
  
  loss = np.sum(-np.log(scores[xrange(num_train), y]))/float(num_train) + 0.5*reg*np.sum(W*W)
  scores_dW_term = scores; scores_dW_term[xrange(num_train), y] -= 1
  dW = (X.T).dot(scores_dW_term)/float(num_train) + reg*W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

