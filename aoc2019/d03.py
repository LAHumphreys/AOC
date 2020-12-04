from tools.fileLoader import load_lists
from tools.listOps import unsorted_matched_groups, non_sorted_intersection
from tools.paths import make_path_from_vectors, PathPoint


def find_nearest_intersection(path_vectors_a, path_vectors_b):
    path_a = make_path_from_vectors(path_vectors_a)[1:]
    path_b = make_path_from_vectors(path_vectors_b)[1:]

    def key(p):
        return p.get_point()

    intersects = non_sorted_intersection(path_a, path_b, key=key)

    if len(intersects) > 0:
        intersects.sort(key=lambda p: p.get_point().manhattan_distance())
        return intersects[0]
    else:
        return None


def find_shortest_intersection(path_vectors_a, path_vectors_b):
    path_a = make_path_from_vectors(path_vectors_a)[1:]
    path_b = make_path_from_vectors(path_vectors_b)[1:]

    def key(p):
        return p.get_point()

    groups = unsorted_matched_groups(path_a, path_b, key=key)

    if len(groups) > 0:
        def path_len_sort(p):
            return p.pathLen

        class Result:
            def __init__(self, a: PathPoint, b: PathPoint):
                self.pointA = a
                self.pointB = b
                self.pathLen = a.pathLen + b.pathLen

        results = []

        for group in groups:
            intersects_a = group[0]
            intersects_b = group[1]

            intersects_a.sort(key=path_len_sort)
            intersects_b.sort(key=path_len_sort)

            results.append(Result(intersects_a[0], intersects_b[0]))

        results.sort(key=path_len_sort)

        return results[0]

    else:
        return None


if __name__ == "__main__":
    def main():
        [path_vectors_a, path_vectors_b] = load_lists("input/d03.txt")
        print(find_nearest_intersection(path_vectors_a, path_vectors_b))
        print(find_shortest_intersection(path_vectors_a, path_vectors_b).pathLen)

    main()
