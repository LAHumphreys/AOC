from tools.file_loader import load_lists
from tools.list_ops import unsorted_matched_groups, non_sorted_intersection
from tools.paths import make_path_from_vectors


def find_nearest_intersection(path_vectors_a, path_vectors_b):
    path_a = make_path_from_vectors(path_vectors_a)[1:]
    path_b = make_path_from_vectors(path_vectors_b)[1:]

    def key(point):
        return point.get_point()

    intersects = non_sorted_intersection(path_a, path_b, key=key)
    result = None

    if len(intersects) > 0:
        intersects.sort(key=lambda p: p.get_point().manhattan_distance())
        result = intersects[0]

    return result


def find_shortest_intersection(path_vectors_a, path_vectors_b):
    path_a = make_path_from_vectors(path_vectors_a)[1:]
    path_b = make_path_from_vectors(path_vectors_b)[1:]

    def key(point):
        return point.get_point()

    groups = unsorted_matched_groups(path_a, path_b, key=key)

    result = None

    if len(groups) > 0:
        def path_len_sort(point):
            return point.path_len

        results = []

        for group in groups:
            intersects_a = group[0]
            intersects_b = group[1]

            intersects_a.sort(key=path_len_sort)
            intersects_b.sort(key=path_len_sort)

            results.append(intersects_a[0].path_len + intersects_b[0].path_len)

        results.sort()
        result = results[0]

    return result


class InvalidInputFile(Exception):
    pass

if __name__ == "__main__":
    def main():
        vectors = load_lists("input/d03.txt")
        if len(vectors) != 2:
            raise InvalidInputFile
        print(find_nearest_intersection(vectors[0], vectors[1]))
        print(find_shortest_intersection(vectors[0], vectors[1]))

    main()
