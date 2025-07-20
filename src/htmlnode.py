

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("This function should not be called from an object of this class, only it's children")

    def props_to_html(self):
        if self.props == None:
            return ""
        return "".join(list(map(lambda prop: f' {prop}="{self.props[prop]}"', self.props)))
    
    def __repr__(self):
        return f'TAG: {self.tag}\nVALUE: {self.value}\nCHILDREN: {self.children}\nPROPS: {self.props}'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Value value missing")
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag passed")
        if self.children == None:
            raise ValueError("Children value missing")
        return f'<{self.tag}{self.props_to_html()}>{"".join(list(map(lambda child: child.to_html(), self.children)))}</{self.tag}>'
