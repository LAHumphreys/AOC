from unittest import TestCase

from aoc2021.d23 import load_cave, AmphipodType, Amphipod, is_complete, auto_shunt
from aoc2021.d23 import get_amber, get_bronze, get_copper, get_desert, clone_cave
from aoc2021.d23 import get_valid_room_exits, get_valid_corridor_exits, get_cave_hash
from aoc2021.d23 import SortedCaveList, find_completion_cost, get_idealised_completion_cost
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class Loader(TestCase):
    def test_ctors(self):
        self.assertEqual(get_amber().type, AmphipodType.AMBER)
        self.assertEqual(get_amber().unit_cost, 1)

        self.assertEqual(get_bronze().type, AmphipodType.BRONZE)
        self.assertEqual(get_bronze().unit_cost, 10)

        self.assertEqual(get_copper().type, AmphipodType.COPPER)
        self.assertEqual(get_copper().unit_cost, 100)

        self.assertEqual(get_desert().type, AmphipodType.DESERT)
        self.assertEqual(get_desert().unit_cost, 1000)

    def test_start(self):
        cave = load_cave(get_test_file_path("samples/d23/example1.txt"))
        self.assertEqual(cave.total_cost, 0)
        self.assertListEqual(cave.corridor, [None]*11)
        self.assertEqual(cave.rooms[0].type, AmphipodType.AMBER)
        self.assertEqual(cave.rooms[1].type, AmphipodType.BRONZE)
        self.assertEqual(cave.rooms[2].type, AmphipodType.COPPER)
        self.assertEqual(cave.rooms[3].type, AmphipodType.DESERT)

        self.assertEqual(cave.rooms[0].join_index, 2)
        self.assertEqual(cave.rooms[1].join_index, 4)
        self.assertEqual(cave.rooms[2].join_index, 6)
        self.assertEqual(cave.rooms[3].join_index, 8)

        self.assertListEqual(cave.rooms[0].spaces, [get_amber(), get_bronze()])
        self.assertListEqual(cave.rooms[1].spaces, [get_desert(), get_copper()])
        self.assertListEqual(cave.rooms[2].spaces, [get_copper(), get_bronze()])
        self.assertListEqual(cave.rooms[3].spaces, [get_amber(), get_desert()])

    def test_corridor(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        self.assertEqual(cave.total_cost, 0)
        self.assertListEqual(cave.corridor, [None, None, None, None, None, get_desert(), None, get_desert(), None, get_amber(), None])
        self.assertEqual(cave.rooms[0].type, AmphipodType.AMBER)
        self.assertEqual(cave.rooms[1].type, AmphipodType.BRONZE)
        self.assertEqual(cave.rooms[2].type, AmphipodType.COPPER)
        self.assertEqual(cave.rooms[3].type, AmphipodType.DESERT)

        self.assertEqual(cave.rooms[0].join_index, 2)
        self.assertEqual(cave.rooms[1].join_index, 4)
        self.assertEqual(cave.rooms[2].join_index, 6)
        self.assertEqual(cave.rooms[3].join_index, 8)

        self.assertListEqual(cave.rooms[0].spaces, [get_amber(), None])
        self.assertListEqual(cave.rooms[1].spaces, [get_bronze(), get_bronze()])
        self.assertListEqual(cave.rooms[2].spaces, [get_copper(), get_copper()])
        self.assertListEqual(cave.rooms[3].spaces, [None, None])


class RoomMoves(TestCase):
    def test_empty_corridor(self):
        cave = load_cave(get_test_file_path("samples/d23/example1.txt"))
        room = cave.rooms[2]
        possible_caves = get_valid_room_exits(cave, room)
        self.assertEqual(len(possible_caves), 7)

        self.assertListEqual(possible_caves[0].corridor, [get_bronze()] + [None]*10)
        self.assertListEqual(possible_caves[1].corridor, [None, get_bronze()] + [None]*9)
        self.assertListEqual(possible_caves[2].corridor, [None, None, None, get_bronze()] + [None]*7)
        self.assertEqual(possible_caves[2].total_cost, 40)

    def test_empty_room(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        empty_room = cave.rooms[3]
        possible_caves = get_valid_room_exits(cave, empty_room)
        self.assertEqual(len(possible_caves), 0)

    def test_blocked_room(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        blocked_room = cave.rooms[2]
        possible_caves = get_valid_room_exits(cave, blocked_room)
        self.assertEqual(len(possible_caves), 0)


class CorridorMoves(TestCase):
    def test_empty_corridor(self):
        cave = load_cave(get_test_file_path("samples/d23/example1.txt"))
        possible_caves = get_valid_corridor_exits(cave)
        self.assertEqual(len(possible_caves), 0)

    def test_valid_exits(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        possible_caves = get_valid_corridor_exits(cave)
        self.assertEqual(len(possible_caves), 1)

        self.assertListEqual(possible_caves[0].corridor, [None]*5 + [get_desert(), None, None, None, get_amber(), None])
        self.assertListEqual(possible_caves[0].rooms[3].spaces, [get_desert(), None])
        self.assertEqual(possible_caves[0].total_cost, 3000)

    def test_valid_exit_completion(self):
        cave = load_cave(get_test_file_path("samples/d23/one_step.txt"))
        sorted_caves = SortedCaveList()
        sorted_caves.add(cave)
        possible_caves = get_valid_corridor_exits(sorted_caves.pop())
        self.assertEqual(len(possible_caves), 1)
        self.assertEqual(is_complete(possible_caves[0]), True)
        sorted_caves.add(possible_caves[0])
        self.assertEqual(sorted_caves.has_completion(), True)

    def test_valid_exit_folded_completion(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/one_step.txt"))
        sorted_caves = SortedCaveList()
        sorted_caves.add(cave)
        possible_caves = get_valid_corridor_exits(sorted_caves.pop())
        self.assertEqual(possible_caves[0].total_cost, 3*1000)
        self.assertEqual(len(possible_caves), 1)
        self.assertEqual(is_complete(possible_caves[0]), True)
        sorted_caves.add(possible_caves[0])
        self.assertEqual(sorted_caves.has_completion(), True)

    def test_valid_exit_completion_algo(self):
        cave = load_cave(get_test_file_path("samples/d23/one_step.txt"))
        sorted_caves = SortedCaveList()
        sorted_caves.add(cave)
        for room in cave.rooms:
            for possible_cave in get_valid_room_exits(cave, room):
                sorted_caves.add(possible_cave)
        for possible_cave in get_valid_corridor_exits(cave):
            sorted_caves.add(possible_cave)
        self.assertEqual(sorted_caves.has_completion(), True)

    def test_valid_from_above(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        cave.rooms[3].type = AmphipodType.AMBER
        possible_caves = get_valid_corridor_exits(cave)
        self.assertEqual(len(possible_caves), 1)

        self.assertListEqual(possible_caves[0].corridor, [None]*5 + [get_desert(), None, get_desert(), None, None, None])
        self.assertListEqual(possible_caves[0].rooms[3].spaces, [get_amber(), None])
        self.assertEqual(possible_caves[0].total_cost, 3)


class IsComplete(TestCase):
    def test_complete(self):
        cave = load_cave(get_test_file_path("samples/d23/complete.txt"))
        self.assertEqual(is_complete(cave), True)

    def test_folded_complete(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/complete.txt"))
        self.assertEqual(is_complete(cave), True)

    def test_not_complete(self):
        cave = load_cave(get_test_file_path("samples/d23/example1.txt"))
        self.assertEqual(is_complete(cave), False)


class Hash(TestCase):
    def test_complete(self):
        cave = load_cave(get_test_file_path("samples/d23/complete.txt"))
        self.assertEqual(get_cave_hash(cave), "...........AABBCCDD")

    def test_folded_complete(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/complete.txt"))
        self.assertEqual(get_cave_hash(cave), "...........AAAABBBBCCCCDDDD")

    def test_corridor(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        self.assertEqual(get_cave_hash(cave), ".....D.D.A.A.BBCC..")


class SortedCaveTest(TestCase):
    def setUp(self) -> None:
        self.complete = load_cave(get_test_file_path("samples/d23/complete.txt"))
        self.example = load_cave(get_test_file_path("samples/d23/example1.txt"))
        self.corridor = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        self.complete.idealised_cost = 1000
        self.complete.total_cost = 1000
        self.corridor.idealised_cost = 100
        self.corridor.total_cost = 100
        self.example.idealised_cost = 10
        self.example.total_cost = 10

    def test_unique_caves(self):
        sorted_caves = SortedCaveList()
        sorted_caves.add(self.example)
        sorted_caves.add(self.complete)
        sorted_caves.add(self.corridor)
        self.assertEqual(sorted_caves.pop().idealised_cost, 10)
        self.assertEqual(sorted_caves.pop().idealised_cost, 100)
        self.assertEqual(sorted_caves.pop().idealised_cost, 1000)
        self.assertEqual(sorted_caves.has_more(), False)

    def test_duplicates(self):
        sorted_caves = SortedCaveList()
        sorted_caves.add(self.example)
        sorted_caves.add(self.complete)
        sorted_caves.add(self.corridor)
        corridor_clone = clone_cave(self.corridor)
        corridor_clone.idealised_cost = 5
        corridor_clone.total_cost = 5
        sorted_caves.add(corridor_clone)
        self.assertEqual(sorted_caves.pop().idealised_cost, 5)
        self.assertEqual(sorted_caves.pop().idealised_cost, 10)
        self.assertEqual(sorted_caves.pop().idealised_cost, 1000)
        self.assertEqual(sorted_caves.has_more(), False)

    def test_completions(self):
        sorted_caves = SortedCaveList()
        sorted_caves.add(self.example)
        self.assertEqual(sorted_caves.has_completion(), False)
        complete_clone = clone_cave(self.complete)
        complete_clone.idealised_cost = 5
        complete_clone.total_cost = 5
        sorted_caves.add(complete_clone)
        self.assertEqual(sorted_caves.has_completion(), True)
        sorted_caves.add(self.corridor)
        self.assertEqual(sorted_caves.has_completion(), True)

        self.assertEqual(sorted_caves.has_more(), True)

        self.assertEqual(sorted_caves.pop().idealised_cost, 5)
        self.assertEqual(sorted_caves.has_more(), False)


class IdealisedCompletion(TestCase):
    def test_completed(self):
        cave = load_cave(get_test_file_path("samples/d23/complete.txt"))
        self.assertEqual(get_idealised_completion_cost(cave), 0)
        cave.total_cost = 30
        self.assertEqual(get_idealised_completion_cost(cave), 30)

    def test_one_step(self):
        cave = load_cave(get_test_file_path("samples/d23/one_step.txt"))
        self.assertEqual(get_idealised_completion_cost(cave), 8)

    def test_exmaple_corridor(self):
        cave = load_cave(get_test_file_path("samples/d23/example_corridor.txt"))
        self.assertEqual(get_idealised_completion_cost(cave), 7008)

    def test_exmaple(self):
        cave = load_cave(get_test_file_path("samples/d23/example1.txt"))
        """
        #############
        #...........#
        ###B#C#B#D###
          #A#D#C#A#
          #########
        """
        cost = 4*10 + 0*1
        cost += 4*100 + 7*1000
        cost += 4*10 + 0*1000
        cost += 0*1000 + 9*1

        cost += 0 + 10 + 0 + 1000
        self.assertEqual(get_idealised_completion_cost(cave), cost)


class CompletionCost(TestCase):
    def test_one_step(self):
        cave = load_cave(get_test_file_path("samples/d23/one_step.txt"))
        self.assertEqual(find_completion_cost(cave), 8)

    def test_one_folded_step(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/one_step.txt"))
        self.assertEqual(find_completion_cost(cave), 3000)

    def test_three_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/three_steps.txt"))
        self.assertEqual(find_completion_cost(cave), 7008)

    def test_example(self):
        cave = load_cave(get_test_file_path("samples/d23/example1.txt"))#############
#AA.......AD#
###D#B#C#.###
  #D#B#C#D#
  #A#B#C#.#
  #.#B#C#.#
  #########
        self.assertEqual(find_completion_cost(cave), 12521)
        #self.assertEqual(0, 12521)
        pass

    def test_folded_example(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/example.txt"))
        self.assertEqual(find_completion_cost(cave), 44169)
        pass

    def test_folded_three_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/three_steps.txt"))
        cost = 7000 + 8 + 3000
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_five_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/five_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_six_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/six_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_eight_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/eight_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_ten_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/ten_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_twelve_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/twelve_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        cost += 70 + 600
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_fourteen_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/fourteen_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        cost += 70 + 600 + 50 + 60
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_sixteen_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/sixteen_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        cost += 70 + 600 + 50 + 60 + 40 + 5000
        print (cost)
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_eighteen_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/eighteen_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        cost += 70 + 600 + 50 + 60 + 40 + 5000 + 600 + 600
        print (cost)
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_nineteen_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/nineteen_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        cost += 70 + 600 + 50 + 60 + 40 + 5000 + 600 + 600 + 8
        print (cost)
        self.assertEqual(find_completion_cost(cave), cost)

    def test_folded_twenty_steps(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/twenty_steps.txt"))
        cost = 7000 + 8 + 3000 + 4 + 4 + 4000 + 40 + 11*1000 + 5 + 9000
        cost += 70 + 600 + 50 + 60 + 40 + 5000 + 600 + 600 + 30 + 8
        print (cost)
        self.assertEqual(find_completion_cost(cave), cost)


class AutoShunt(TestCase):
    def test_nothing_to_shunt(self):
        cave = load_cave(get_test_file_path("samples/d23/unfolded/mid_example.txt"))
        shunted = load_cave(get_test_file_path("samples/d23/unfolded/mid_example.txt"))
        auto_shunt(shunted)
        self.assertEqual(get_cave_hash(cave), get_cave_hash(shunted))
        self.assertEqual(cave.total_cost, shunted.total_cost)

    def test_intra_room_shunts(self):
        expected_shunted = load_cave(get_test_file_path("samples/d23/unfolded/shunted.txt"))
        cave = load_cave(get_test_file_path("samples/d23/unfolded/to_shunt.txt"))
        auto_shunt(cave)
        self.assertEqual(get_cave_hash(cave), get_cave_hash(expected_shunted))
        self.assertEqual(cave.total_cost, 2001)

    def test_corridor_shunt(self):
        expected_shunted = load_cave(get_test_file_path("samples/d23/unfolded/corridor_shunted.txt"))
        cave = load_cave(get_test_file_path("samples/d23/unfolded/to_corridor_shunt.txt"))
        auto_shunt(cave)
        self.assertEqual(get_cave_hash(cave), get_cave_hash(expected_shunted))
        cost = 1 + 2000 + 4000 + 9000
        self.assertEqual(cave.total_cost, cost)
