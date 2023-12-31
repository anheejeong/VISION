# -*- coding: utf-8 -*-

# tensorflow library import
import tensorflow as tf

# define initialization W, b(parameter Θ)
# tensorflow에서 parameter를 정의할 때 tf.Varaible 사용
# 선형회귀 모델(Wx + b)을 위한 tf.Variable을 선언합니다.
# random.normal => Gaussian distribution random value
# shape=[1] : 1차원
W = tf.Variable(tf.random.normal(shape=[1]))
b = tf.Variable(tf.random.normal(shape=[1]))

# 1. 가설 정의 -------------------------------------------

@tf.function
def linear_model(x):
  return W*x + b

# 2. 손실 함수 정의 ---------------------------------------

# 손실 함수를 정의합니다.
# MSE 손실함수 \mean{(y' - y)^2}
@tf.function
def mse_loss(y_pred, y):
  return tf.reduce_mean(tf.square(y_pred - y))

# 3. Gradient Descent & Optimizer ---------------------

# 최적화를 위한 그라디언트 디센트 옵티마이저를 정의합니다.
# optimizer class 사용(SGD - mini-batch optimization 사용)
optimizer = tf.optimizers.SGD(0.01) # learning rate - 0.01

# 최적화를 위한 function을 정의합니다.
# step update function을 train_step으로 대부분 사용
@tf.function
def train_step(x, y):
  with tf.GradientTape() as tape:
    y_pred = linear_model(x)
    loss = mse_loss(y_pred, y)
  gradients = tape.gradient(loss, [W, b])
	# zip 함수 -> 두개의 list를 개별요소끼리 묶어줌
  optimizer.apply_gradients(zip(gradients, [W, b]))

# 실제 트레이닝 ------------------------------------------

# 트레이닝을 위한 입력값과 출력값을 준비합니다.
x_train = [1, 2, 3, 4]
y_train = [2, 4, 6, 8]

# 경사하강법을 1000번 수행합니다.
for i in range(1000):
  train_step(x_train, y_train)

# 테스트를 위한 입력값을 준비합니다.
x_test = [3.5, 5, 5.5, 6]
# 테스트 데이터를 이용해 학습된 선형회귀 모델이 데이터의 경향성(y=2x)을 잘 학습했는지 측정합니다.
# 예상되는 참값 : [7, 10, 11, 12]
print(linear_model(x_test).numpy())
# tensor 형태에서 python 형태로 출력하기 위해 numpy() 사용
