class Item:
    def __init__(self, value=None):
        self.value = value
        self.nextValue = None


class LList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        curr = self.head
        str = '[ '
        while curr is not None:
            str += f'{curr.value},'
            curr = curr.nextValue
        str += ']'
        return str

    def contains(self, value):
        l_Item = self.head
        while l_Item:
            if value == l_Item.value:
                return True
            else:
                l_Item = l_Item.nextValue
        return False

    def push(self, newValue):
        n_Item = Item(newValue)
        if self.head is None:
            self.head = n_Item
            return
        l_Item = self.head
        while l_Item.nextValue:
            l_Item = l_Item.nextValue
        l_Item.nextValue = n_Item

    def get(self, itemIndex):
        l_Item = self.head
        boxIndex = 0
        while boxIndex <= itemIndex:
            if boxIndex == itemIndex:
                return l_Item.cat
            boxIndex = boxIndex + 1
            l_Item = l_Item.nextValue

    def remove(self, rmValue):
        h_Item = self.head

        if h_Item is not None:
            if h_Item.value == rmValue:
                self.head = h_Item.nextValue
                return
        while h_Item is not None:
            if h_Item.value == rmValue:
                break
            l_Item = h_Item
            h_Item = h_Item.nextValue
        if h_Item is None:
            return
        l_Item.nextValue = h_Item.nextValue
