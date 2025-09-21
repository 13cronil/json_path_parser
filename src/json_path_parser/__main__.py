from .logger import logger
from .parser import create_parser
from .transformer import JSONPathTransformer


from lark import Lark, Tree, Token, Transformer


# First, let's create a detailed inspector
def inspect_transformer_input(rule_name, items):
    print(f"\n=== {rule_name} received ===")
    print(f"Items count: {len(items)}")

    for i, item in enumerate(items):
        print(f"  [{i}] Type: {type(item).__name__}")

        if isinstance(item, Tree):
            print(f"      Tree.data: '{item.data}'")
            print(f"      Tree.children: {item.children}")
        elif isinstance(item, Token):
            print(f"      Token.type: '{item.type}'")
            print(f"      Token.value: '{item.value}' (repr: {repr(item.value)})")
        else:
            print(f"      Raw value: {repr(item)}")


# Now let's create a transformer that shows us everything
class InspectorTransformer(Transformer):
    def field(self, items):
        inspect_transformer_input("field", items)
        # Don't transform, just return as-is to see the flow
        return ("FIELD", items)

    def bracket_selector(self, items):
        inspect_transformer_input("bracket_selector", items)
        return ("BRACKET_SELECTOR", items)

    def index(self, items):
        inspect_transformer_input("index", items)
        return ("INDEX", items)

    def slice(self, items):
        inspect_transformer_input("slice", items)
        return ("SLICE", items)

    def wildcard_index(self, items):
        inspect_transformer_input("wildcard_index", items)
        return ("WILDCARD_INDEX", items)

    def name(self, items):
        inspect_transformer_input("name", items)
        return ("NAME", items)

    def recursive_selector(self, items):
        inspect_transformer_input("recursive_selector", items)
        return ("RECURSIVE_SELECTOR", items)

    def root(self, items):
        inspect_transformer_input("root", items)
        return ("ROOT", items)


def main():
    try:
        parser = create_parser()
        sample_json_path = r"$.store.book[1:2].title"
        parse_tree = parser.parse(sample_json_path)
        # logger.info(parse_tree.pretty())

        inspector = InspectorTransformer()
        json_transformer = JSONPathTransformer()
        result = json_transformer.transform(parse_tree)
        logger.info(f"Result is {result}")
    except Exception as e:
        logger.error("An error occurred while parsing JSON.", exc_info=e)
        raise


if __name__ == "__main__":
    main()
