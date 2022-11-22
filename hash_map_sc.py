# Name: Matthew Tinnel
# OSU Email: tinnelm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: June 3, 2022
# Description: An implementation of a HashMap with Chaining for collision resolution.
# Utilizes a Dynamic Array containing SLNodes of LinkedLists for the underlying
# storage type.
# The following methods are added by the author:
#   put()
#   empty_buckets()
#   table_load()
#   clear()
#   resize_table()
#   get()
#   contains_key()
#   remove()
#   get_keys()
#   find_mode()


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2, hash_function_3)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key
        already exists in the hash map, its associated value is replaced
        with the new value. If the given key is not in the hash map, a key/value
        pair is added.

        Parameters:
            key: str
            value: object

        Returns:
            None
        """

        # Get the hashed index of the map
        hash = self._hash_function(key)
        index = hash % self._capacity
        linked_node = self._buckets[index]

        # If that bucket is empty.
        if linked_node.length() == 0:
            linked_node.insert(key, value)
            self._size += 1

        # If the value for the key is getting replaced.
        elif linked_node.contains(key):
            linked_node.remove(key)
            linked_node.insert(key, value)

        # Else add a link in the LinkedList for that index.
        else:
            linked_node.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        Parameters:

        Returns:
            int
        """

        num_empty_buckets = 0

        for i in range(0, self._capacity):
            if self._buckets[i].length() == 0:
                num_empty_buckets += 1

        return num_empty_buckets

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.

        Parameters:

        Returns:
            float
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying
        hash table capacity.

        Parameters:

        Returns:
            None
        """
        new_buckets = DynamicArray()
        for i in range(0, self._capacity):
            new_buckets.append(LinkedList())

        self._size = 0
        self._buckets = new_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing
        key/value pairs remain in the new hash map, and all the hash
        table links are rehashed. If new_capacity is less than 1, the method
        does nothing.

        Parameters:
            new_capacity: int

        Returns:
            None
        """

        if new_capacity < 1:
            return

        # Copy current bucket to temp_bucket array to save data.
        temp_buckets = DynamicArray()
        for i in range(0, self._capacity):
            temp_buckets.append(self._buckets[i])

        new_buckets = DynamicArray()
        for i in range(0, new_capacity):
            new_buckets.append(LinkedList())

        # Save old capacity and update to new capacity and buckets.
        old_capacity = self._capacity
        self._capacity = new_capacity
        self._buckets = new_buckets
        self._size = 0

        for i in range(0, old_capacity):
            linked_list = temp_buckets[i]
            for node in linked_list:
                self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.

        Parameters:
            key: str

        Returns:
            object
        """

        # Get the hashed index of the map
        hash = self._hash_function(key)
        index = hash % self._capacity
        linked_node = self._buckets[index]

        found_node = linked_node.contains(key)
        if found_node:
            if found_node.key == key:
                return found_node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Parameters:
            key: str

        Returns:
            True - if the given key is in the hash map.
            Otherwise returns False.
        """

        if self._size == 0:
            return False

        # Get the hashed index of the map
        hash = self._hash_function(key)
        index = hash % self._capacity
        linked_node = self._buckets[index]

        found_node = linked_node.contains(key)
        if found_node:
            if found_node.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.

        Parameters:
            key: str

        Returns:
            None
        """

        # Get the hashed index of the map
        hash = self._hash_function(key)
        index = hash % self._capacity
        linked_node = self._buckets[index]

        remove_node = linked_node.remove(key)
        if remove_node:
            self._size -= 1

        # If the key is not in the hash map.
        return

    def get_keys(self) -> DynamicArray:
        """
        Parameters:

        Returns:
            DynamicArray - contains all the keys stored in the hash map.
        """
        array_of_keys = DynamicArray()

        # Iterates through each linked_list.
        for i in range(0, self._capacity):
            linked_list = self._buckets[i]
            for node in linked_list:
                array_of_keys.append(node.key)

        return array_of_keys


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode(s) of the passed DynamicArray.

    Parameters:
        da: DynamicArray

    Returns:
        (DynamicArray, int)
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)

    result_tuple = ()

    mode_array = DynamicArray()

    potential_count = 0
    highest_count = 0

    # iterates through the input array.
    for i in range(0, da.length()):
        current_val = da[i]

        # If i is already mapped.
        already_mapped = map.contains_key(current_val)
        if already_mapped:
            nodes_value = map.get(da[i])
            nodes_value += 1
            potential_count = nodes_value
            map.put(da[i], nodes_value)
        # Else it maps it.
        else:
            map.put(da[i], 1)
            potential_count += 1

        # If a new mode is found.
        if potential_count > highest_count:
            highest_count = potential_count
            new_array = DynamicArray()
            mode_array = new_array
            mode_array.append(current_val)
            result_tuple = (mode_array, highest_count)

        # If a mode needs to be added.
        elif potential_count == highest_count:
            highest_count = potential_count
            mode_array.append(current_val)
            result_tuple = (mode_array, highest_count)

        potential_count = 0

    return result_tuple


# ------------------- BASIC TESTING ---------------------------------------- #

my_hash = HashMap(7, hash_function_3)
my_hash.put(55, 1)
my_hash.put(5, 2)
my_hash.put(42, 3)
my_hash.put(19, 4)
my_hash.put(25, 5)
my_hash.put(15, 6)
my_hash.put(32, 7)
print(my_hash)
print(my_hash.table_load())

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
