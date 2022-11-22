# Name: Matthew Tinnel
# Description: An implementation of a HashMap with Open Addressing with Quadratic Probing
# for collision resolution. Utilizes a Dynamic Array containing HashEntry objects.
# The following methods are added by the author:
#   put()
#   get()
#   remove()
#   contains_key()
#   clear()
#   empty_buckets()
#   resize_table()
#   table_load()
#   get_keys()

from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution.
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output.
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map.
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map.
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key
        already exists in the hash map, its associated value must be replaced
        with the new value. If the given key is not in the hash map, a key/value
        pair is added.

        The table is resized to double its current capacity when this method is called
        and the current load factor of the table is greater than or equal to 0.5

        Parameters:
            key: str
            value: object

        Returns:
            None
        """
        # If the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Get the hashed index of the map
        hash = self._hash_function(key)
        index = hash % self._capacity

        # If that bucket is empty.
        if not self._buckets[index]:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # If the given key already exists in the hash map.
        elif self._buckets[index].key == key:
            self._buckets[index].value = value
            if self._buckets[index].is_tombstone is True:
                self._buckets[index].is_tombstone = False
                self._size += 1

        # If the index is a tombstone
        elif self._buckets[index].is_tombstone is True:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # If that bucket is taken by another key
        # Use quadratic probing ((index + j^2) % self._capacity where j = 1, 2, 3, ...)
        else:
            j = 1
            # Break statements:
            #   1. while the bucket is not None.
            #   2. while the bucket's key is not the passed key.
            #   3. while the bucket is not a tombstone.
            while self._buckets[(hash + (j * j)) % self._capacity] and \
                self._buckets[(hash + (j * j)) % self._capacity].key != key and \
                    self._buckets[(hash + (j * j)) % self._capacity].is_tombstone is False:
                j += 1

            # If the bucket at the found index in not None.
            if self._buckets[(hash + (j * j)) % self._capacity]:
                # If the bucket's key is the passed key
                if self._buckets[(hash + (j * j)) % self._capacity].key == key:
                    # Update the value without increasing the size (unless it's a tombstone).
                    self._buckets[(hash + (j * j)) % self._capacity].value = value
                    if self._buckets[index].is_tombstone is True:
                        self._buckets[index].is_tombstone = False
                        self._size += 1
            else:
                self._buckets[(hash + (j * j)) % self._capacity] = HashEntry(key, value)
                self._size += 1

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.

        Parameters:

        Returns:
            float
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        Parameters:

        Returns:
            int
        """

        num_empty_buckets = 0

        for i in range(0, self._capacity):
            if self._buckets[i] is None:
                num_empty_buckets += 1

        return num_empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing
        key/value pairs remain in the new hash map, and all the hash
        table links are rehashed. If new_capacity is less than 1 or
        new_capacity is less than the table's size, the method
        does nothing.

        Parameters:
            new_capacity: int

        Returns:
            None
        """

        if new_capacity < 1 or new_capacity < self._size:
            return

        # Copy current bucket to temp_bucket array to save data.
        temp_buckets = DynamicArray()
        for i in range(0, self._capacity):
            temp_buckets.append(self._buckets[i])

        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        # Save old capacity and update to new capacity and buckets.
        old_capacity = self._capacity
        self._capacity = new_capacity
        self._buckets = new_buckets
        self._size = 0

        # Copies over all values that have not been deleted (by checking is_tombstone variable).
        for i in range(0, old_capacity):
            if temp_buckets[i] and temp_buckets[i].is_tombstone is False:
                self.put(temp_buckets[i].key, temp_buckets[i].value)
            else:
                continue

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
        hash_entry = self._buckets[index]

        if hash_entry:
            if hash_entry.key == key and not hash_entry.is_tombstone:
                return hash_entry.value

            # Check if the requested key has been shifted to an open address.
            else:
                j = 1
                while self._buckets[(hash + (j * j)) % self._capacity] and \
                    self._buckets[(hash + (j * j)) % self._capacity].key != key and \
                        self._buckets[(hash + (j * j)) % self._capacity].is_tombstone is False:
                    j += 1

                probed_bucket = self._buckets[(hash + (j * j)) % self._capacity]
                if probed_bucket:
                    if probed_bucket.key == key and not probed_bucket.is_tombstone:
                        return self._buckets[(hash + (j * j)) % self._capacity].value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.

        Parameters:
            key: str

        Returns:
            object
        """
        if self._size == 0:
            return False

        # Get the hashed index of the map
        hash = self._hash_function(key)
        index = hash % self._capacity

        # If the original hashed index contains requested key.
        if self._buckets[index]:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return True

            # Check if the requested key has been shifted to an open address.
            else:
                j = 1
                while self._buckets[(hash + (j * j)) % self._capacity] and \
                    self._buckets[(hash + (j * j)) % self._capacity].key != key and \
                        self._buckets[(hash + (j * j)) % self._capacity].is_tombstone is False:
                    j += 1

                probed_bucket = self._buckets[(hash + (j * j)) % self._capacity]
                if probed_bucket:
                    if probed_bucket.key == key and not probed_bucket.is_tombstone:
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

        # If the hashed index value is our target and not already deleted...
        if self._buckets[index]:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                # ... It is deleted.
                self._buckets[index].is_tombstone = True
                self._size -= 1

            # Else, check if the requested key has been shifted to an open address.
            else:
                j = 1
                while self._buckets[(hash + (j * j)) % self._capacity] and \
                        self._buckets[(hash + (j * j)) % self._capacity].key != key:
                    j += 1

                # If the probed hashed value is our target and not already deleted...
                probed_bucket = self._buckets[(hash + (j * j)) % self._capacity]
                if probed_bucket:
                    if probed_bucket.key == key and not probed_bucket.is_tombstone:
                        # ... It is deleted.
                        self._buckets[(hash + (j * j)) % self._capacity].is_tombstone = True
                        self._size -= 1

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
            new_buckets.append(None)

        self._size = 0
        self._buckets = new_buckets

    def get_keys(self) -> DynamicArray:
        """
        Parameters:

        Returns:
            DynamicArray - contains all the keys stored in the hash map.
        """
        array_of_keys = DynamicArray()

        # Iterates through each linked_list.
        for i in range(0, self._capacity):
            hash_entry = self._buckets[i]
            if hash_entry and not hash_entry.is_tombstone:
                array_of_keys.append(hash_entry.key)

        return array_of_keys


# ------------------- BASIC TESTING ---------------------------------------- #


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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
