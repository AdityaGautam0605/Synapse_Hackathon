def fuse_predictions(xgb_prob, lstm_prob, w1=0.6, w2=0.4):
    return (w1 * xgb_prob) + (w2 * lstm_prob)