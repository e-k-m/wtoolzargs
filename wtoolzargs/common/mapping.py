import copy


class Mapping(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.next = None
        self.transform = None

    def mappings(self):
        res = [(self.source, self.target)]

        tmp = self
        while tmp.next is not None:
            res.append((tmp.next.source, tmp.next.target))
            tmp = tmp.next
        return res

    def has_next_mapping(self):
        return self.next is not None

    @staticmethod
    def create_from_strings(source, target):
        source_split = Mapping._split(source)

        transform = None
        if isinstance(target, tuple) and len(target) == 1:
            target, transform = (target[0], None)
        elif isinstance(target, tuple) and len(target) == 2:
            target, transform = target

        target_split = Mapping._split(target)

        if len(source_split) != len(target_split):
            raise ValueError(
                "Relationship mappings to not have the same lengths."
            )

        items = list(zip(source_split, target_split))
        res = Mapping(items[0][0], items[0][1])
        last = res
        for a, b in items[1:]:
            last.next = Mapping(a, b)
            last = last.next
        last.transform = transform
        return res

    @staticmethod
    def _split(s):
        if "." in s:
            return s.split(".")
        else:
            return [s]


class Mappings(object):
    def __init__(self, mappings={}):
        self._mappings = mappings

    def get(self, source):
        return self._mappings.get(source).target

    def transform(self, source, value):
        transform = self._mappings.get(source).transform
        if callable(transform):
            return transform(value)
        return value

    def has(self, source):
        return source in self._mappings

    def move_to_next(self, source):
        if not (
            source in self._mappings
            and self._mappings[source].has_next_mapping()
        ):
            return self

        res = self.copy()
        next_ = res._mappings[source].next
        res._mappings[next_.source] = next_
        return res

    def mappings(self):
        return {k: v.mappings() for k, v in self._mappings.items()}

    def copy(self):
        return copy.deepcopy(self)

    @staticmethod
    def create_from_dict(d):
        mappings = {}
        for source, target in d.items():
            mapping = Mapping.create_from_strings(source, target)
            mappings[mapping.source] = mapping
        return Mappings(mappings)
