from taipy.gui import Gui
from pages.explorer.explorer_pd import *
from pages.root import *

pages = {
    "/": root_page,
    "Explorateur": explorer_page,
    "Comparaison": "### Comparaison",
    "Detail": "### Detail",
    "Rapport": "### Rapport",
}

Gui(pages=pages).run(title="Model RH", dark_mode=False, margin=0)
