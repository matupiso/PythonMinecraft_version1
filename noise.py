from opensimplex.internals import _init, _noise2, _noise3
from settings import njit, SEED
perm, perm_grad_index3 = _init(seed=SEED)


@njit
def noise3(x, y, z):
    return _noise3(
        x, y, z, perm, perm_grad_index3
    )


@njit
def noise2(x, y):
    return _noise2(
        x, y, perm,
    )