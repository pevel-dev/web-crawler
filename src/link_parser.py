import html.parser


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def reset(self):
        super().reset()
        self.links = []

    def handle_starttag(self, tag, attributes) -> list[str]:
        if tag == "a":
            for (name, value) in attributes:
                if name == "href":
                    self.links.append(value)
