# -*- coding: utf-8 -*-

import tensorflow as tf

# MNIST 데이터를 다운로드 합니다.
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# 이미지들을 float32 데이터 타입으로 변경합니다.
# 원래 Numpy array 형태로 주어짐
x_train, x_test = x_train.astype('float32'), x_test.astype('float32')
# 28*28 형태의 이미지를 784차원으로 flattening 합니다.
# 2 dimension => 1 dimension으로 변경(softmax regression을 위함)
# -1 : magic number, reshape 함수가 알아서 60,000 * 784, 10,000 * 784차원으로 만들어 줌
x_train, x_test = x_train.reshape([-1, 784]), x_test.reshape([-1, 784])
# [0, 255] 사이의 값을 [0, 1]사이의 값으로 Normalize합니다.
# 0~255 -> 0~1
x_train, x_test = x_train / 255., x_test / 255.
# 레이블 데이터에 one-hot encoding을 적용합니다.
# 60,000 * 10 dimension으로 해주면 좋음
y_train, y_test = tf.one_hot(y_train, depth=10), tf.one_hot(y_test, depth=10)

# tf.data API를 이용해서 데이터를 섞고 batch 형태로 가져옵니다.
# mini-batch 단위로 묶음
train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_data = train_data.repeat().shuffle(60000).batch(100) # mini-batch 개수 지정
train_data_iter = iter(train_data) # 순회 가능

# tf.keras.Model을 이용해서 Softmax Regression 모델을 정의합니다.
class SoftmaxRegression(tf.keras.Model):
  def __init__(self):
    super(SoftmaxRegression, self).__init__()
		# 모델 구조 지정
		# kernel-initializer = W, bias-initializer = b
    self.softmax_layer = tf.keras.layers.Dense(10,
                                               activation=None,
                                               kernel_initializer='zeros',
                                               bias_initializer='zeros')

  def call(self, x):
    logits = self.softmax_layer(x)

    return tf.nn.softmax(logits)

# cross-entropy 손실 함수를 정의합니다.
@tf.function
def cross_entropy_loss(y_pred, y):
  return tf.reduce_mean(-tf.reduce_sum(y * tf.math.log(y_pred), axis=[1]))
	# API 제공
  #return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logtis, labels=y)) # tf.nn.softmax_cross_entropy_with_logits API를 이용한 구현

# 최적화를 위한 그라디언트 디센트 옵티마이저를 정의합니다.
optimizer = tf.optimizers.SGD(0.5)

# 최적화를 위한 function을 정의합니다.
@tf.function
def train_step(model, x, y):
  with tf.GradientTape() as tape:
    y_pred = model(x)
    loss = cross_entropy_loss(y_pred, y)
  gradients = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))

# 모델의 정확도를 출력하는 함수를 정의합니다.
@tf.function
def compute_accuracy(y_pred, y):
	# one-hot encoding 사용하기 때문에 argmax 과정 필요
  correct_prediction = tf.equal(tf.argmax(y_pred,1), tf.argmax(y,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  return accuracy # 0~1

# SoftmaxRegression 모델을 선언합니다.
SoftmaxRegression_model = SoftmaxRegression()

# 1000번 반복을 수행하면서 최적화를 수행합니다.
for i in range(1000):
  batch_xs, batch_ys = next(train_data_iter)
  train_step(SoftmaxRegression_model, batch_xs, batch_ys)

# 학습이 끝나면 학습된 모델의 정확도를 출력합니다.
print("정확도(Accuracy): %f" % compute_accuracy(SoftmaxRegression_model(x_test), y_test)) # 정확도 : 약 91%
