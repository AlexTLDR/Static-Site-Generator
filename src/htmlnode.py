class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop, value in self.props.items():
            props_html += f' {prop}="{value}"'
        return props_html

    def to_html(self):
        if self.tag is None:
            return self.value
            
        props = self.props_to_html()
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"

    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None:
            raise ValueError("ParentNode must have children")

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def to_html(self):
    if self.tag is None:
        return self.value
    
    props_html = self.props_to_html()
    return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

def to_html(self):
    if self.tag is None:
        return self.value
        
    props = self.props_to_html()
    children_html = ""
    for child in self.children:
        children_html += child.to_html()
        
    return f"<{self.tag}{props}>{children_html}</{self.tag}>"



