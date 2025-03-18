import tensorflow as tf

class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):  # ✅ Accept kwargs like 'trainable'
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(
            shape=(input_shape[-1], 1),
            initializer="random_normal",
            trainable=True,
            name="attention_weight"
        )
        self.b = self.add_weight(
            shape=(1,),
            initializer="zeros",
            trainable=True,
            name="attention_bias"
        )
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        scores = tf.nn.tanh(tf.matmul(inputs, self.W) + self.b)
        attention_weights = tf.nn.softmax(scores, axis=1)
        context_vector = attention_weights * inputs
        return tf.reduce_sum(context_vector, axis=1)

    def get_config(self):
        config = super(AttentionLayer, self).get_config()
        # If you have custom attributes, add them here!
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
