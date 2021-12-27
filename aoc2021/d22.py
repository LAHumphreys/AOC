from dataclasses import dataclass, field
from typing import List, Tuple, Type
from enum import Enum


class SwitchMode(Enum):
    ON = "on"
    OFF = "off"


class Unhandled(Exception):
    pass


@dataclass(frozen=True, order=True)
class Cube:
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int


@dataclass(frozen=True, order=True)
class SwitchCube(Cube):
    mode: SwitchMode
    holes: List[Type['SwitchCube']] = field(default_factory=list)


def split_out_z_cubes(primary: SwitchCube, secondary: SwitchCube) -> List[SwitchCube]:
    if primary.mode != secondary.mode:
        raise Unhandled

    if not cubes_overlap(primary, secondary):
        raise Unhandled

    cubes = []
    if secondary.max_z > primary.max_z:
        cubes.append(SwitchCube(
            mode=secondary.mode,
            min_x=max(primary.min_x, secondary.min_x),
            min_y=max(primary.min_y, secondary.min_y),
            max_x=min(primary.max_x, secondary.max_x),
            max_y=min(primary.max_y, secondary.max_y),
            min_z=primary.max_z + 1,
            max_z=secondary.max_z
        ))

    if secondary.min_z < primary.min_z:
        cubes.append(SwitchCube(
            mode=secondary.mode,
            min_x=max(primary.min_x, secondary.min_x),
            min_y=max(primary.min_y, secondary.min_y),
            max_x=min(primary.max_x, secondary.max_x),
            max_y=min(primary.max_y, secondary.max_y),
            min_z=secondary.min_z,
            max_z=primary.min_z - 1,
        ))

    return cubes


def split_out_y_cubes(primary: SwitchCube, secondary: SwitchCube) -> List[SwitchCube]:
    if primary.mode != secondary.mode:
        raise Unhandled

    if not cubes_overlap(primary, secondary):
        raise Unhandled

    cubes = []
    if secondary.max_y > primary.max_y:
        cubes.append(SwitchCube(
            mode=secondary.mode,
            min_x=max(primary.min_x, secondary.min_x),
            max_x=min(primary.max_x, secondary.max_x),
            min_z=secondary.min_z,
            max_z=secondary.max_z,
            min_y=primary.max_y + 1,
            max_y=secondary.max_y
        ))

    if secondary.min_y < primary.min_y:
        cubes.append(SwitchCube(
            mode=secondary.mode,
            min_x=max(primary.min_x, secondary.min_x),
            max_x=min(primary.max_x, secondary.max_x),
            min_z=secondary.min_z,
            max_z=secondary.max_z,
            min_y=secondary.min_y,
            max_y=primary.min_y - 1,
        ))

    return cubes


# Split Priority:
#  z: always stays within x, y bounds
#  y: consumes z, but treats x as a hard boundary
#  x: consumes z both x and y
def split_out_x_cubes(primary: SwitchCube, secondary: SwitchCube) -> List[SwitchCube]:
    if primary.mode != secondary.mode:
        raise Unhandled

    if not cubes_overlap(primary, secondary):
        raise Unhandled

    cubes = []
    if secondary.max_x > primary.max_x:
        cubes.append(SwitchCube(
            mode=secondary.mode,
            min_z=secondary.min_z,
            min_y=secondary.min_y,
            max_z=secondary.max_z,
            max_y=secondary.max_y,
            min_x=primary.max_x + 1,
            max_x=secondary.max_x
        ))

    if secondary.min_x < primary.min_x:
        cubes.append(SwitchCube(
            mode=secondary.mode,
            min_z=secondary.min_z,
            min_y=secondary.min_y,
            max_z=secondary.max_z,
            max_y=secondary.max_y,
            min_x=secondary.min_x,
            max_x=primary.min_x - 1,
        ))

    return cubes


def split_out_external_cubes(primary: SwitchCube, secondary: SwitchCube) -> List[SwitchCube]:
    if cubes_contains(primary, secondary):
        return []

    if cubes_contains(secondary, primary):
        raise Unhandled

    if cubes_overlap(primary, secondary):
        return split_out_z_cubes(primary, secondary) + \
               split_out_y_cubes(primary, secondary) + \
               split_out_x_cubes(primary, secondary)

    return [secondary]


def split_composite_to_cubes(first: SwitchCube, second: SwitchCube) -> List[SwitchCube]:
    cubes = sorted(zip(map(get_volume_cube, (first, second)), [first, second]))
    primary = cubes[1][1]
    secondary = cubes[0][1]
    return [primary] + split_out_external_cubes(primary, secondary)


def get_volume_cube(cube: SwitchCube) -> int:
    outer_volume = (1 + cube.max_x - cube.min_x) * \
                   (1 + cube.max_y - cube.min_y) * \
                   (1 + cube.max_z - cube.min_z)

    return outer_volume - get_total_volume(cube.holes)


def get_total_volume(cubes: List[SwitchCube]) -> int:
    return sum((get_volume_cube(cube) for cube in cubes))


def merge_cubes(lhs: SwitchCube, rhs: SwitchCube) -> Tuple[SwitchCube, SwitchCube]:
    if lhs.mode == rhs.mode == SwitchMode.ON:
        rhs_remainder, lhs = remove_overlap(rhs, lhs)
        return lhs, rhs_remainder

    if lhs.mode == SwitchMode.ON and rhs.mode == SwitchMode.OFF:
        lhs_remainder = make_hole(lhs, rhs)
        return lhs_remainder, rhs

    raise Unhandled


def consolidate_cubes(cube_list: List[SwitchCube], new_cube: SwitchCube):
    if new_cube.mode == SwitchMode.ON:
        consolidated_list = []
        on_list = [new_cube]
        for cube in cube_list:
            new_on_list = []
            while on_list and cube is not None:
                this_on = on_list.pop()
                if this_on.holes:
                    raise Unhandled
                if cubes_contains(this_on, cube):
                    new_on_list += [this_on]
                    cube = None
                elif cubes_contains(cube, this_on):
                    cube, _ = merge_cubes(cube, this_on)
                elif not cubes_overlap(cube, this_on):
                    new_on_list += [this_on]
                else:
                    new_on_list += split_out_external_cubes(cube, this_on)
                    cube, _ = merge_cubes(cube, this_on)
            if cube:
                consolidated_list += [cube]
            on_list = new_on_list
        consolidated_list += on_list
    elif new_cube.mode == SwitchMode.OFF:
        consolidated_list = []
        for cube in cube_list:
            cube, _ = merge_cubes(cube, new_cube)
            if get_volume_cube(cube) > 0:
                consolidated_list += [cube]

    return consolidated_list


def apply_bounds(bounds: SwitchCube, cube: SwitchCube) -> SwitchCube:
    if cubes_overlap(bounds, cube):
        return SwitchCube(
            mode=cube.mode,
            min_x=max(bounds.min_x, cube.min_x),
            min_y=max(bounds.min_y, cube.min_y),
            min_z=max(bounds.min_z, cube.min_z),
            max_x=min(bounds.max_x, cube.max_x),
            max_y=min(bounds.max_y, cube.max_y),
            max_z=min(bounds.max_z, cube.max_z),
            holes=[apply_bounds(bounds, sub_hole)
                   for sub_hole in cube.holes if cubes_overlap(bounds, sub_hole)]
        )
    raise Unhandled


def remove_overlap(target_cube: SwitchCube,
                   source_cube: SwitchCube) -> Tuple[SwitchCube, SwitchCube]:
    updated_target = target_cube
    updated_source = source_cube

    if target_cube.mode != source_cube.mode:
        raise Unhandled
    if target_cube.mode != SwitchMode.ON:
        raise Unhandled

    if cubes_overlap(target_cube, source_cube):
        overlap = SwitchCube(
            mode=SwitchMode.OFF,
            min_x=max(target_cube.min_x, source_cube.min_x),
            min_y=max(target_cube.min_y, source_cube.min_y),
            min_z=max(target_cube.min_z, source_cube.min_z),
            max_x=min(target_cube.max_x, source_cube.max_x),
            max_y=min(target_cube.max_y, source_cube.max_y),
            max_z=min(target_cube.max_z, source_cube.max_z),
            holes=[]
        )

        for hole in target_cube.holes:
            if cubes_overlap(hole, overlap):
                raise Unhandled

        updated_source_holes = []
        for hole in source_cube.holes:
            if cubes_contains(overlap, hole):
                pass
            elif cubes_overlap(overlap, hole):
                updated_source_holes += split_out_external_cubes(overlap, hole)
            else:
                updated_source_holes.append(hole)

        updated_target = SwitchCube(
            mode=target_cube.mode,
            min_x=target_cube.min_x,
            min_y=target_cube.min_y,
            min_z=target_cube.min_z,
            max_x=target_cube.max_x,
            max_y=target_cube.max_y,
            max_z=target_cube.max_z,
            holes=target_cube.holes + [overlap]
        )

        updated_source = SwitchCube(
            mode=source_cube.mode,
            min_x=source_cube.min_x,
            min_y=source_cube.min_y,
            min_z=source_cube.min_z,
            max_x=source_cube.max_x,
            max_y=source_cube.max_y,
            max_z=source_cube.max_z,
            holes=updated_source_holes
        )

    return updated_target, updated_source


def make_hole(target_cube: SwitchCube, hole: SwitchCube) -> SwitchCube:
    if target_cube.mode != SwitchMode.ON:
        raise Unhandled

    if hole.mode != SwitchMode.OFF:
        raise Unhandled

    if hole.holes:
        raise Unhandled

    if cubes_overlap(target_cube, hole):
        internal_hole = SwitchCube(
            mode=SwitchMode.OFF,
            min_x=max(target_cube.min_x, hole.min_x),
            min_y=max(target_cube.min_y, hole.min_y),
            min_z=max(target_cube.min_z, hole.min_z),
            max_x=min(target_cube.max_x, hole.max_x),
            max_y=min(target_cube.max_y, hole.max_y),
            max_z=min(target_cube.max_z, hole.max_z),
            holes=[]
        )

        unique_holes = []
        while internal_hole and target_cube.holes:
            hole = target_cube.holes.pop()
            if cubes_contains(internal_hole, hole):
                pass
            elif cubes_contains(hole, internal_hole):
                internal_hole = None
                unique_holes += [hole]
            elif cubes_overlap(hole, internal_hole):
                unique_holes += split_out_external_cubes(internal_hole, hole)
            else:
                unique_holes += [hole]
        if internal_hole:
            unique_holes += [internal_hole]

        return SwitchCube(
            mode=target_cube.mode,
            min_x=target_cube.min_x,
            min_y=target_cube.min_y,
            min_z=target_cube.min_z,
            max_x=target_cube.max_x,
            max_y=target_cube.max_y,
            max_z=target_cube.max_z,
            holes=unique_holes
        )
    return target_cube


def parse_cube_defn(defn: str) -> SwitchCube:
    on_off, spatial_defn = defn.split(" ")
    x_defn, y_defn, z_defn = (defn.split("=")[1].split("..") for defn in spatial_defn.split(","))
    return SwitchCube(mode=SwitchMode(on_off),
                      min_x=int(x_defn[0]),
                      max_x=int(x_defn[1]),
                      min_y=int(y_defn[0]),
                      max_y=int(y_defn[1]),
                      min_z=int(z_defn[0]),
                      max_z=int(z_defn[1]),
                      holes=[])


def load_cubes(path: str) -> List[SwitchCube]:
    with open(path, encoding="ascii") as file:
        cubes = [parse_cube_defn(line.rstrip()) for line in file.readlines()]
    return cubes


def cubes_overlap(ref_cube: SwitchCube, other_cube: SwitchCube) -> bool:
    overlap = True
    if ref_cube.max_x < other_cube.min_x or ref_cube.min_x > other_cube.max_x:
        overlap = False
    elif ref_cube.max_y < other_cube.min_y or ref_cube.min_y > other_cube.max_y:
        overlap = False
    elif ref_cube.max_z < other_cube.min_z or ref_cube.min_z > other_cube.max_z:
        overlap = False
    return overlap


def cubes_contains(outter: SwitchCube, inner: SwitchCube) -> bool:
    overlap = outter.min_x < inner.min_x and \
              outter.max_x > inner.max_x and \
              outter.min_y < inner.min_y and \
              outter.max_y > inner.max_y and \
              outter.min_z < inner.min_z and \
              outter.max_z > inner.max_z
    return overlap


def get_ref_cube() -> SwitchCube:
    return SwitchCube(mode=SwitchMode.ON,
                      min_x=-50,
                      max_x=50,
                      min_y=-50,
                      max_y=50,
                      min_z=-50,
                      max_z=50)


def count_points(cubes: List[SwitchCube]):
    consolidated_cubes = []
    ref_window = get_ref_cube()
    for cube in cubes:
        if cubes_overlap(ref_window, cube):
            consolidated_cubes = consolidate_cubes(consolidated_cubes, cube)
    return get_total_volume(consolidated_cubes)


def count_all_points(cubes: List[SwitchCube]):
    consolidated_cubes = []
    for cube in cubes:
        consolidated_cubes = consolidate_cubes(consolidated_cubes, cube)
    return get_total_volume(consolidated_cubes)


if __name__ == "__main__":
    def main():
        cubes = load_cubes("input/d22.txt")
        print(count_points(cubes))
        print(count_all_points(cubes))


    main()
