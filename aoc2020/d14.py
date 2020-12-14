import re


class Mask:
    def __init__(self):
        self.set_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    def set_mask(self, code):
        self.zero_mask = 0
        self.one_mask = 0
        little_endian = code[::-1]
        self.code = little_endian
        self.address_masks = None
        for i in range(36):
            if little_endian[i] == "X":
                self.zero_mask = self.zero_mask | (1 << i)
            elif little_endian[i] == "1":
                self.zero_mask = self.zero_mask | (1 << i)
                self.one_mask = self.one_mask | (1 << i)
            elif little_endian[i] == "0":
                pass
            else:
                raise ValueError

    def get_address_masks(self):
        if self.address_masks is None:
            self.address_masks = [(0, ~0)]
            for i in range(36):
                if self.code[i] == "X":
                    updated_addresses = []
                    for old_mask in self.address_masks:
                        enable_mask = ((old_mask[0] | 1 << i), old_mask[1])
                        disable_mask = (old_mask[0], old_mask[1] & ~(1 << i))
                        updated_addresses.append(enable_mask)
                        updated_addresses.append(disable_mask)
                    self.address_masks = updated_addresses
        return self.address_masks

    def get_masked_value(self, value):
        value = value & self.zero_mask
        value = value | self.one_mask
        return value

    def get_masked_addresses(self, address):
        address = address | self.one_mask
        result = []
        for mask in self.get_address_masks():
            result.append((address | mask[0]) & mask[1])
        return result


def load_pogram(path):
    program = []
    mask_pattern = re.compile("mask = ([X01]{36})")
    mem_pattern = re.compile("mem\\[([0-9]+)] = ([0-9]+)")
    with open(path) as file:
        for line in file.read().split("\n"):
            mask_match = mask_pattern.match(line)
            mem_match = mem_pattern.match(line)
            if mask_match:
                program.append((-1, mask_match.group(1)))
            elif mem_match:
                program.append((int(mem_match.group(1)), int(mem_match.group(2))))
            else:
                raise ValueError
    return program


def run_program(program):
    memory = {}
    mask = Mask()
    for address, value in program:
        if address == -1:
            mask.set_mask(value)
        else:
            memory[address] = mask.get_masked_value(value)
    return memory


def run_program_version_2(program):
    memory = {}
    mask = Mask()
    for address, value in program:
        if address == -1:
            mask.set_mask(value)
        else:
            for address_to_update in mask.get_masked_addresses(address):
                memory[address_to_update] = value
    return memory


def checksum_memory(memory):
    total = 0
    for address in memory:
        total += memory[address]
    return total


if __name__ == "__main__":
    def main():
        program = load_pogram("input/d14.txt")
        memory = run_program(program)
        print("Checksum: {0}".format(checksum_memory(memory)))
        memory_v2 = run_program_version_2(program)
        print("Checksum: {0}".format(checksum_memory(memory_v2)))
        pass


    main()
