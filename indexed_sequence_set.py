class _Terminator:
    """Entity to denote a sequence termination."""
    pass


class IndexedSequenceSet:
    """A set of sequences stored in a recursive structure for fast searching."""
    def __init__(self, *args):
        self._dict = dict()

        if len(args) == 0:
            return
        if len(args) > 1:
            raise TypeError("Constructor only takes 0 or 1 arguments.")

        sequences = args[0]
        for item in sequences:
            self.add_sequence(item)

    def _get_or_add(self, item):
        """Get item or add and get if not present."""
        if not item in self._dict:
            self._dict[item] = IndexedSequenceSet()
        assert isinstance(self._dict[item], IndexedSequenceSet)
        return self._dict[item]

    def _add_terminator(self):
        """Add a sequence terminator to denote end of a sequence."""
        self._dict[_Terminator] = None

    def add_sequence(self, sequence):
        """Add a sequence to the set."""
        if len(sequence) != 0:
            sub_set = self._get_or_add(sequence[0])
            sub_set.add_sequence(sequence[1:])
        else:
            self._add_terminator()

    def query_seq(self, seq):
        """Get sequences starting with seq."""
        subset = self
        matched = []
        for item in seq:
            if item not in subset._dict:
                return (matched, [])
            matched.append(item)
            subset = subset._dict[item]
        return (matched, subset.iterate_all())


    def iterate_all(self):
        for sub_set_item in self._dict.items():
            key = sub_set_item[0]
            sub_set = sub_set_item[1]

            if key is _Terminator:
                yield []
                continue

            _, sub_sequences = sub_set.query_seq([])
            yield from map(lambda x: [key, ] + x, sub_sequences)
