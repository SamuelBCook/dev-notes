from dataclasses import dataclass
from collections import namedtuple

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LinkMeta:
    name: str
    url: str
    img: str
    width: str


class DefaultSettings:
    logo_data: tuple[LinkMeta, ...] = (
        LinkMeta(
            name="GitLab",
            url="https://gitlab.com",
            img="https://about.gitlab.com/images/press/logo/svg/gitlab-logo-500.svg",
            width="150px",
        ),
        LinkMeta(
            name="Stack Overflow",
            url="https://stackoverflow.com",
            img="https://upload.wikimedia.org/wikipedia/commons/e/ef/Stack_Overflow_icon.svg",
            width="100px",
        ),
        LinkMeta(
            name="Python Docs",
            url="https://docs.python.org/3/",
            img="https://www.python.org/static/community_logos/python-logo.png",
            width="150px",
        ),
        LinkMeta(
            name="GitHub",
            url="https://github.com",
            img="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            width="100px",
        ),
    )

    def __init__(self):
        pass
