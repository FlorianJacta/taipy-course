import taipy.gui.builder as tgb


def creates_pages(pages):
    return [(f"/{page}", page.replace("_", " ").title()) for page in list(pages)[1:]]


with tgb.Page() as root_page:
    with tgb.part("header sticky"):
        with tgb.layout(
            "100px 12rem 1 8rem 150px",
            columns__mobile="100px 12rem 1 8rem 150px",
            class_name="header-content",
        ):
            tgb.image("favicon.png", width="50px")
            tgb.text("Model **RH**", mode="md")
            tgb.navbar(
                lov=lambda pages: creates_pages(pages),
            )
            tgb.part()

            tgb.text(
                "Bienvenue **Lorem Ipsum**!",
                mode="md",
            )

    with tgb.part("content"):
        tgb.html("br")

        tgb.content()

        tgb.toggle(theme=True)
