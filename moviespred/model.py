import os
from datetime import datetime
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.callbacks import ModelCheckpoint
from moviespred import paths


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
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model


def train_cnn(model,
              ds_train,
              ds_val,
              batch_size=32,
              callbacks=[EarlyStopping(patience=25,
                                      monitor='loss',
                                      restore_best_weights=True)],
              epochs=200):

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    path_checkpoint = os.path.join(paths['checkpoints'],
                                   f'checkpoint_{timestamp}')

    model_checkpoint_callback = ModelCheckpoint(filepath=path_checkpoint,
                                                save_weights_only=True,
                                                monitor='val_accuracy',
                                                mode='max',
                                                save_best_only=True)

    history = model.fit(ds_train,
                        validation_data=ds_val,
                        batch_size=batch_size,
                        epochs=epochs,
                        callbacks=[model_checkpoint_callback, *callbacks])
    return history


if __name__ == "__main__":
    model = create_cnn()
    model = compile_cnn(model)
    history = train_cnn(model)
    print(history)
