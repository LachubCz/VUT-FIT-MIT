import numpy as np


def sparse_tuples_from_sequences(sequences, dtype=np.int32):
    """
    Create a sparse representations of inputs.
    Args:
        sequences: a list of lists of type dtype where each element is a sequence
    Returns:
        A tuple with (indices, values, shape)
    """
    indexes = []
    values = []

    for n, sequence in enumerate(sequences):
        indexes.extend(zip([n] * len(sequence), range(len(sequence))))
        values.extend(sequence)

    indexes = np.asarray(indexes, dtype=np.int64)
    values = np.asarray(values, dtype=dtype)
    shape = np.asarray([len(sequences), np.asarray(indexes).max(0)[1] + 1], dtype=np.int64)
    return indexes, values, shape


def pad_sequences_and_get_lengths(sequences, max_label_seq_length):
    padded_sequences = np.zeros((len(sequences), max_label_seq_length), dtype=np.int64)
    lengths = []
    for i in range(len(sequences)):
        sequence_length = len(sequences[i])
        padded_sequences[i][0:sequence_length] = sequences[i]
        lengths.append(sequence_length)
    return padded_sequences, np.asarray(lengths)
