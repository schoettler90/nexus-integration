"""Shared router dependencies."""


def get_db():
    """Resolve the active MongoDB handle at call time.

    Deliberately late-bound: the handle lives on the ``main`` module (set in
    its lifespan), and the tests patch ``main.db`` — an import-time binding
    would freeze the pre-patch value.
    """
    import main

    return main.db
