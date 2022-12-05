from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from moviespred import get_dataset
from keras.callbacks import ModelCheckpoint


def create_cnn(input_shape=(600, 400, 3),
               n_classes=18,
               n_conv_block=5,
               n_dense=3,
               filters=[8, 16, 32, 64, 128],
               kernels=[5, 4, 4, 3, 3],
               neurons=[128, 64, 32],
               dropout=True,
               drop_rate=[.25, .25, .5]):

  model = Sequential()
  model.add(layers.Input(shape=input_shape))
  for conv, filter, kernel in zip(range(n_conv_block), filters, kernels):
    model.add(layers.Conv2D(filter, kernel))
    model.add(layers.MaxPool2D())
    model.add(layers.Dropout(0.25))

  model.add(layers.Flatten())

  for dense, neuron, rate in zip(range(n_dense), neurons, drop_rate):
    model.add(layers.Dense(neuron))
    if dropout:
      model.add(layers.Dropout(rate))

  model.add(layers.Dense(n_classes, activation='softmax'))

  return model

def compile_cnn(model,
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']):
  model.compile(optimizer=optimizer,
                loss=loss,
                metrics=metrics)
  return model
def train_cnn(model,
              batch_size=32,
              callbacks=EarlyStopping(patience=25, monitor='loss', restore_best_weights=True),
              epochs=200):
    checkpoint_filepath = '../checkpoint'
    model_checkpoint_callback = tensorflow.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

    train = get_dataset()[0]
    val = get_dataset()[1]
    history = model.fit(train,
                    validation_data=val,
                    batch_size=batch_size,
                    epochs=epochs,
                    callbacks=[callbacks,model_checkpoint_callback])
    return history

if __name__ == "__main__":
    model = create_cnn()
    model = compile_cnn(model)
    history = train_cnn(model)
    print (history)
