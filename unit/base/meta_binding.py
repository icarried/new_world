from typing import Union, Optional, Tuple

class UnexpectedBindingType(Exception):
    pass

class BaseBinding:
    def __init__(self):
        self.bindname = 'bindname' # BaseBinding
        self.bindings = {} # 每个值的格式：{obj_key: (obj, self_key)} 或 {obj_key: [(obj, self_key), ...]}

    def one_way_bind(self, obj: Union['BaseBinding', list['BaseBinding']], self_key: Optional[str] = None, obj_key: Optional[str] = None):
        """
        仅用于被bind调用, 实现单向绑定
        默认使用bindname作为key
        """
        # 当key为None时，自动设定为对应的bindname
        self_key = self_key if self_key is not None else self.bindname
        if obj_key is None:
            # hasattr(obj, "bindname"): 判断obj是否继承自BaseBinding，且时间复杂度为O(1)，而issubclass(obj, BaseBinding)的时间复杂度为O(n)
            # if isinstance(self.bindings[obj_key], Tuple) and hasattr(self.bindings[obj_key][0], "bindname"): # 用于self.bindings[obj_key]为Tuple的情况
            if hasattr(obj, "bindname"):
                obj_key = obj.bindname
            elif isinstance(obj, list):
                if hasattr(obj[0], "bindname"):
                    # 判断列表的bindname是否相同
                    for o in obj:
                        if o.bindname != obj[0].bindname:
                            raise UnexpectedBindingType(f'one_way_bind error: Unexpected Binding Type {type(o)}')
                    else:
                        obj_key = obj[0].bindname
                else:
                    raise UnexpectedBindingType(f'one_way_bind error: Unexpected Binding Type {type(obj)}')
                
        # 按照self.bindings值的格式，将要设定的value
        value = (obj, self_key)

        # 如果key不存在，则新增key
        if obj_key not in self.bindings:
            if isinstance(obj, list):
                self.bindings[obj_key] = []
            else:
                self.bindings[obj_key] = None

        # 若为list，则直接将value添加到列表中
        if isinstance(self.bindings[obj_key], list):
            self.bindings[obj_key].append(value)
            return

        # 如果有绑定则先解除绑定(已排除list的情况)
        if self.bindings[obj_key] is not None:
            self.unbind(obj_key=obj_key)
        # 设定绑定
        self.bindings[obj_key] = value

    def bind(self, obj: Union['BaseBinding', list['BaseBinding']], self_key: Optional[str] = None, obj_key: Optional[str] = None):
        """
        用于绑定两个对象，两个对象之间的绑定是双向的
        若不指定key, 则绑定的key为对应对象的bindname 
        若obj为list, 则将list中的每个对象都绑定到对应对象的bindname上
        """
        # 通过one_way_bind实现双向绑定
        if obj is None:
            return
        self.one_way_bind(obj, self_key, obj_key)
        if hasattr(obj, "bindname"):
            obj.one_way_bind(self, obj_key, self_key)
        elif isinstance(obj, list):
            for o in obj:
                o.one_way_bind(self, obj_key, self_key)
        else:
            raise UnexpectedBindingType(f'bind error: Unexpected Binding Type {type(obj)}')
        
    def one_way_unbind(self, obj: Union['BaseBinding', list['BaseBinding'], None] = None, obj_key: Optional[str] = None):
        """
        仅用于被unbind调用, 实现单向解除绑定
        当不指定obj但指定key时, 解除对应key的所有绑定
        当指定obj但不指定key时, 解除对应对象的bindname上的绑定
        当指定obj且指定key时, 解除对应key中的对应对象的绑定(用于key对应的值为list的情况且只解除其中部分绑定)
        当不指定obj且不指定key时, 解除所有绑定
        """
        if obj is None:
            if obj_key is None:
                for obj_key in self.bindings:
                    if isinstance(self.bindings[obj_key], Tuple) and hasattr(self.bindings[obj_key][0], "bindname"):
                        self.bindings[obj_key] = None
                    elif isinstance(self.bindings[obj_key], list):
                        self.bindings[obj_key] = []
            else:
                if obj_key not in self.bindings or self.bindings[obj_key] is None:
                    raise Exception('unbind error') # 不存在绑定
                elif isinstance(self.bindings[obj_key], Tuple) and hasattr(self.bindings[obj_key][0], "bindname"):
                    self.bindings[obj_key] = None
                elif isinstance(self.bindings[obj_key], list):
                    self.bindings[obj_key] = []
                else:
                    raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(self.bindings[obj_key])}')
        elif obj_key is None:
            if hasattr(obj, "bindname"):
                obj_key = obj.bindname
            elif isinstance(obj, list):
                for o in obj:
                    if hasattr(o, "bindname"):
                        obj_key = o.bindname
                        break
                else:
                    raise Exception('unbind error') # 将要绑定的列表中没有继承自BaseBinding的对象
            else:
                raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(obj)}')
            
            if obj_key not in self.bindings or self.bindings[obj_key] is None:
                raise Exception('unbind error')
            elif isinstance(self.bindings[obj_key], Tuple) and hasattr(self.bindings[obj_key][0], "bindname"):
                if self.bindings[obj_key][0] != obj:
                    raise Exception('unbind error') # 不存在绑定
                self.bindings[obj_key] = None
            elif isinstance(self.bindings[obj_key], list): # 时间复杂度为O(n)，可以优化
                for o in self.bindings[obj_key]:
                    if o[0] == obj:
                        self.bindings[obj_key].remove(o)
                        break
            else:
                raise UnexpectedBindingType(f'unbind error: Unexpected Binding Type {type(self.bindings[obj_key])}')
            

    def unbind(self, obj: Union['BaseBinding', list['BaseBinding'], None] = None, obj_key: Optional[str] = None):
        """
        用于解除两个对象之间的绑定
        self_key在value元组中, 格式为(obj, self_key), 或在list中, 格式为[(obj, self_key), ...]
        当不指定obj但指定key时, 解除对应key的所有绑定, 对应key中绑定的对象也会对self调用one_way_unbind
        当指定obj但不指定key时, 解除对应对象的bindname上的绑定, 对应对象也会对self调用one_way_unbind
        当指定obj且指定key时, 解除对应key中的对应对象的绑定(用于key对应的值为list的情况且只解除其中部分绑定), 对应对象也会对self调用one_way_unbind
        每次解除绑定都会对self和obj调用one_way_unbind, 使得双向绑定都被解除(obj为list时, 对list中每个对象都调用one_way_unbind)
        """
        if obj is None:
            if obj_key is None:
                for obj_key in self.bindings:
                    if isinstance(self.bindings[obj_key], Tuple) and hasattr(self.bindings[obj_key][0], "bindname"):
                        self_key = self.bindings[obj_key][1]
                        self.bindings[obj_key][0].one_way_unbind(self, self_key)
                        self.bindings[obj_key] = None
                    elif isinstance(self.bindings[obj_key], list):
                        for o in self.bindings[obj_key]:
                            self_key = o[1]
                            o[0].one_way_unbind(self, self_key)
                        self.bindings[obj_key] = []
            else:
                if obj_key not in self.bindings or self.bindings[obj_key] is None:
                    raise Exception('unbind error') # 不存在绑定
                elif isinstance(self.bindings[obj_key], Tuple) and hasattr(self.bindings[obj_key][0], "bindname"):
                    self_key = self.bindings[obj_key][1]
                    self.bindings[obj_key][0].one_way_unbind(self, self_key)
                    self.bindings[obj_key] = None
                    

    def __del__(self):
        # 对象删除时，解除所有绑定
        self.unbind()

