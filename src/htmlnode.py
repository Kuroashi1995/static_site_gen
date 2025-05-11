from functools import reduce
class HTMLNode:
    def __init__(
        self, tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str | None:
        raise NotImplementedError

    def props_to_html(self) -> str | None:
        html_props_list = []
        if self.props:
            for prop in self.props:
                html_props_list.append(f'{prop}="{self.props[prop]}"')
            return " " + " ".join(html_props_list) + " "
        else:
            return ""

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag and
            self.children == other.children and
            self.value == other.value and
            self.props == other.props
        )

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str , props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None,  props)

    def to_html(self) -> str:
        if not self.value and not self.tag == "img":
            raise ValueError
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None , children, props)

    def to_html(self) -> str | None:
        if not self.tag:
            raise ValueError("missing tag property")
        elif not self.children:
            raise ValueError("missing children attribute")
        else:
            return f"<{self.tag}{self.props_to_html()}>{reduce(lambda acc, child: acc + child.to_html(), self.children, '')}</{self.tag}>"
