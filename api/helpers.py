from tensorflow import greater, float32, reduce_mean, math, cast

def macro_f1(y, y_hat, thresh=0.5):

    """
    Compute the macro F1-score on a batch of observations (average F1 across labels)

    Args:
        y (int32 Tensor): labels array of shape (BATCH_SIZE, N_LABELS)
        y_hat (float32 Tensor): probability matrix from forward propagation of shape (BATCH_SIZE, N_LABELS)
        thresh: probability value above which we predict positive

    Returns:
        macro_f1 (scalar Tensor): value of macro F1 for the batch
    """

    y_pred = cast(greater(y_hat, thresh), float32)
    tp = cast(math.count_nonzero(y_pred * y, axis=0), float32)
    fp = cast(math.count_nonzero(y_pred * (1 - y), axis=0), float32)
    fn = cast(math.count_nonzero((1 - y_pred) * y, axis=0), float32)
    f1 = 2*tp / (2*tp + fn + fp + 1e-16)
    macro_f1 = reduce_mean(f1)
    return macro_f1
