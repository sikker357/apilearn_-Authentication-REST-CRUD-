# Package initializer: expose submodules for `from apilearn import *` and provide safe imports.

# Minimal safe imports so `from apilearn import main` works when modules are present.
# Wrapping imports to avoid raising at package import time if some modules are missing (e.g., during tooling).
try:
    from . import main, auth, crud, database, models, schemas  # type: ignore
except Exception:
    # Modules may not exist yet during editing / tooling; ignore import errors.
    pass

__all__ = ["main", "auth", "crud", "database", "models", "schemas"]
