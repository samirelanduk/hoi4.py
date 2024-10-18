from tqdm import tqdm
from utils.check_profile import check_profile
from hoi4.parse import load_as_text
from hoi4.plain import tokenize, strip_down


class Blocks:
    cls_tokens = []
    cls_loc = 0
    pbar = None
    pbar_step = 0

    @classmethod
    def set_tokens(cls, tokens, loc=0):
        cls.cls_tokens = tokens
        cls.cls_loc = loc
        cls.pbar = tqdm(total=len(tokens))
        cls.pbar_step = len(tokens) // 100

    def __init__(self, name, start_loc: int):
        self.name = name
        self.start_loc = start_loc
        # move the Blocks.cls_loc one step forward for each instance created
        Blocks.cls_loc += 1

    @staticmethod
    def check_type(start_loc):
        """
        check the following 2 tokens after '{', then determine the type of sub block,
        whether a list, a dict or a bizarre dict.
        
        Specifically, The type of block is the type of the block content,
        e.g. a = {'b' = 1 } is a dict block, b = { {'b' = 1 } {'c' = 1 } } is a list block
        
        caution! cannot recognize: { a 1 } as a dict
        """
        try:
            tokens = Blocks.cls_tokens[start_loc + 1: start_loc + 3]
        except IndexError:  # e.g. {ENG GER} end 
            return True

        if tokens == ['=', '{', '{']:
            pass

        if tokens == ['1557', 'type', '=']:
            pass

        if Blocks.cls_loc == 0:
            return 'dict'

        if tokens[0] == '{':  # e.g. { { a = 1 } { b = 2 } }
            return 'list'

        else:
            if tokens[1] == '=':
                return 'dict'

            elif tokens[1] == '{':  # e.g. { GER { ... } }
                return 'bizarre_dict'

            else:
                return 'list'

    @staticmethod
    def instantiate_subblock():
        loc = Blocks.cls_loc
        block_type = Blocks.check_type(loc)

        if block_type == 'dict':
            return SubDictBlocks(Blocks.cls_loc)

        elif block_type == 'bizarre_dict':
            return BizarreDictBlocks(Blocks.cls_loc)

        elif block_type == 'list':
            return ListBlocks(Blocks.cls_loc)


class DictBlocks(Blocks):
    """
    difference between subtypes of DictBlocks is the way how they are named. 
    see Blocks.check_type for more type information
    """

    def __init__(self, name, start_loc: int):
        super().__init__(name, start_loc)
        self.contents = {}

    def add_to_dict(self, key, val):
        key = self.get_dict_key(key)
        self.contents[key] = val

    def get_dict_key(self, key):
        if key not in self.contents:
            return key
        new_key = key
        n = 1
        while new_key in self.contents:
            new_key = f'{key}__{n}'
            n += 1
        return new_key


class MainDictBlocks(DictBlocks):
    def __init__(self, start_loc: int):
        super().__init__('main', start_loc)


class SubDictBlocks(DictBlocks):
    def __init__(self, start_loc: int):
        self.name = Blocks.cls_tokens[start_loc - 2]
        super().__init__(self.name, start_loc)


class BizarreDictBlocks(DictBlocks):
    def __init__(self, start_loc: int):
        self.name = Blocks.cls_tokens[start_loc - 1]
        super().__init__(self.name, start_loc)


class ListBlocks(Blocks):
    def __init__(self, start_loc: int):
        self.name = Blocks.cls_tokens[start_loc - 2]
        super().__init__(self.name, start_loc)
        self.contents = []


def parse_block_tokens(block: Blocks):
    """
    use Blocks.cls_loc to locate the current token
    parse logic:
    1. return if meet '}' token
    2. determine method according to the type of block, see Blocks.check_type for more type information
        - general approach:
            - create a sub block when meet '{' token, parse it add sub block to its contents.
            - difference detail according to the type of block
        - list block: 
            - if '{', general approach
            - not '{' token: append token to contents
        - bizarre dict block:
            - get name of its subblock
            - create a sub block, parse and add it
        - dict block:
            whether a key-val pair or subblock is differentiated by token following '=',
            so only check the following token
            - if '{', general approach
            - not '{' token: add key-val pair to its contents
    """
    while Blocks.cls_loc < len(Blocks.cls_tokens):
        if Blocks.cls_loc % Blocks.pbar_step == 0:
            Blocks.pbar.n = Blocks.cls_loc
            Blocks.pbar.refresh()
        token = Blocks.cls_tokens[Blocks.cls_loc]

        if token == "}":
            return

        else:
            if isinstance(block, ListBlocks):
                if token == "{":
                    sub_block = Blocks.instantiate_subblock()
                    parse_block_tokens(sub_block)
                    block.contents.append(sub_block.contents)
                else:
                    block.contents.append(token)

            elif isinstance(block, BizarreDictBlocks):
                name = token
                Blocks.cls_loc += 1
                sub_block = Blocks.instantiate_subblock()
                parse_block_tokens(sub_block)
                block.add_to_dict(name, sub_block.contents)

            elif isinstance(block, DictBlocks):
                if token == "=":
                    Blocks.cls_loc += 1
                    token = Blocks.cls_tokens[Blocks.cls_loc]

                    if token == "{":
                        sub_block = Blocks.instantiate_subblock()
                        parse_block_tokens(sub_block)
                        block.add_to_dict(sub_block.name, sub_block.contents)

                    else:
                        block.add_to_dict(Blocks.cls_tokens[Blocks.cls_loc - 2], Blocks.cls_tokens[Blocks.cls_loc])

            Blocks.cls_loc += 1


def parse_tokens(tokens):
    """
    1. set settings for Blocks class attributes: cls_tokens, cls_loc, and pbar for tqdm
    2. create the main block and go into the parsing loop
    """
    Blocks.set_tokens(tokens)
    main_block = MainDictBlocks(0)
    parse_block_tokens(main_block)
    return main_block.contents


# @check_profile(20)  # check performance if needed
def load_as_dict_block(path):
    """
    read from save path and return a parsed dict
    
    load_as_text: get a plain-text filestring from a HOI4 save file
    strip_down: remove line breaks and redundant spaces, let space be the only delimiter
    
    tokenize: turn the filestring into a list of tokens, many data format lost here, might be improved
    """

    filestring = load_as_text(path)
    data = strip_down(filestring)
    tokens = tokenize(data)

    return parse_tokens(tokens)
