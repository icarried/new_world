from typing import Union, Optional

class UnexpectedBindingType(Exception):
    pass

class BaseBinding:
    def __init__(self):
        self.bindname = 'BaseBinding'
        self.bindings = {}

    def reverse_bind(self, key: Optional[str] = None, obj: Optional['BaseBinding'] = None):
        """
        用于被bind调用, 实现反向绑定
        """
        if key not in self.bindings or self.bindings[key] is None or isinstance(self.bindings[key], BaseBinding):
            self.bindings[key] = obj
        elif isinstance(self.bindings[key], list):
            self.bindings[key].append(obj)
        else:
            raise UnexpectedBindingType(f'reverse_bind error: Unexpected Binding Type {type(obj)}')

    def bind(self, key: Optional[str] = None, obj: Union['BaseBinding', list['BaseBinding'], None] = None, self_key: Optional[str] = None):
        """
        用于绑定两个对象，两个对象之间的绑定是双向的
        若不指定key, 则绑定到对应对象的bindname上
        若obj为list, 则将list中的每个对象都绑定到对应对象的bindname上
        """
        if obj is None:
            return
        self_key = self_key if self_key is not None else self.bindname
        # hasattr(obj, "bindname"): 判断obj是否继承自BaseBinding，且时间复杂度为O(1)，而issubclass(obj, BaseBinding)的时间复杂度为O(n)
        if key is None:
            if hasattr(obj, "bindname"):
                key = obj.bindname
            elif isinstance(obj, list):
                for o in obj:
                    if hasattr(o, "bindname"):
                        key = o.bindname
                        break
                else:
                    raise Exception('bind error') # 将要绑定的列表中没有继承自BaseBinding的对象
            else:
                raise UnexpectedBindingType(f'bind error: Unexpected Binding Type {type(obj)}')
        # 若key不存在，则新增key
        if key not in self.bindings:
            if isinstance(obj, list):
                self.bindings[key] = []
            else:
                self.bindings[key] = None
        if self.bindings[key] is None or hasattr(self.bindings[key], "bindname"):
            # 绑定新增或替换，当替换时，需要先解除绑定原来的对象
            if hasattr(self.bindings[key], "bindname"):
                self.unbind(key)
            self.bindings[key] = obj
            if hasattr(obj, "bindname"):
                obj.reverse_bind(self_key, self)
            else:
                raise UnexpectedBindingType(f'bind error: Unexpected Binding Type {type(obj)}')
        elif isinstance(self.bindings[key], list):
            if isinstance(obj, list):
                self.bindings[key].extend(obj)
                for o in obj:
                    o.reverse_bind(self_key, self)
            elif hasattr(obj, "bindname"):
                self.bindings[key].append(obj)
                obj.reverse_bind(self_key, self)
            else:
                raise UnexpectedBindingType(f'bind error: Unexpected Binding Type {type(obj)}')
        else:
            raise UnexpectedBindingType(f'bind error: Unexpected Binding Type {type(self.bindings[key])}')
        
    def reverse_unbind(self, key: Optional[str] = None, obj: Optional['BaseBinding'] = None):
        """
        用于被unbind调用, 实现反向解除绑定
        """
        if key not in self.bindings or self.bindings[key] is None:
            raise Exception('reverse_unbind error') # 不存在绑定
        elif hasattr(self.bindings[key], "bindname"):
            self.bindings[key] = None
        elif isinstance(self.bindings[key], list):
            self.bindings[key].remove(obj)
        else:
            raise UnexpectedBindingType(f'reverse_unbind error: Unexpected Binding Type {type(self.bindings[key])}')

    def unbind(self, key: Optional[str] = None, obj: Union['BaseBinding', list['BaseBinding'], None] = None, self_key: Optional[str] = None):
        """
        用于解除两个对象之间的绑定
        若不指定obj, 则解除对应key的所有绑定, 若key也为None, 则解除所有绑定
        若不指定key, 则解除对应对象的bindname上的绑定、
        若obj为list, 则将list中的每个对象都解除对应对象的bindname上的绑定
        每次解除绑定都会调用reverse_unbind, 使得双向绑定都被解除
        """
        self_key = self_key if self_key is not None else self.bindname
        # hasattr(self.bindings[key], "bindname"): 判断self.bindings[key]是否继承自BaseBinding，且时间复杂度为O(1)，而issubclass(self.bindings[key], BaseBinding)的时间复杂度为O(n)
        if obj is None:
            if key is None:
                for key in self.bindings:
                    if hasattr(self.bindings[key], "bindname"):
                        self.bindings[key].reverse_unbind(self_key, self)
                    elif isinstance(self.bindings[key], list):
                        for o in self.bindings[key]:
                            o.reverse_unbind(self_key, self)
                    self.bindings[key] = None
            else:
                if key not in self.bindings or self.bindings[key] is None:
                    raise Exception('unbind error') # 不存在绑定
                elif hasattr(self.bindings[key], "bindname"):
                    self.bindings[key].reverse_unbind(self_key, self)
                    self.bindings[key] = None
                elif isinstance(self.bindings[key], list):
                    for o in self.bindings[key]:
                        o.reverse_unbind(self_key, self)
                    self.bindings[key] = None
                else:
                    raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(self.bindings[key])}')
            return
        elif key is None:
            if hasattr(obj, "bindname"):
                key = obj.bindname
            elif isinstance(obj, list):
                for o in obj:
                    if hasattr(o, "bindname"):
                        key = o.bindname
                        break
                else:
                    raise Exception('unbind error') # 将要绑定的列表中没有继承自BaseBinding的对象
            else:
                raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(obj)}')
        if key not in self.bindings or self.bindings[key] is None:
            raise Exception('unbind error') # 不存在绑定
        elif hasattr(self.bindings[key], "bindname"):
            self.bindings[key].reverse_unbind(self_key, self)
            self.bindings[key] = None

        elif isinstance(self.bindings[key], list):
            if isinstance(obj, list):
                for o in obj:
                    o.reverse_unbind(self_key, self)
                    self.bindings[key].remove(o) # 时间复杂度为O(n)，可以优化
            elif hasattr(obj, "bindname"):
                obj.reverse_unbind(self_key, self)
                self.bindings[key].remove(obj)
            else:
                raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(obj)}')
        else:
            raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(self.bindings[key])}')

    def __del__(self):
        # 对象删除时，解除所有绑定
        self.unbind()

