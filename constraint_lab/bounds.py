"""Effective endpoints with complete declaration provenance."""
from .version import compare


def reduce_bound(constraints, parsed, side):
    chosen, contributors = None, []
    strongest = "greater" if side == "lower" else "less"
    for index, constraint in enumerate(constraints):
        endpoint = constraint[side]
        if endpoint is None:
            continue
        version = parsed[index][side]
        relation = strongest if chosen is None else compare(version, chosen)[0]
        contributor = dict(index=index, id=constraint["id"], **endpoint)
        if relation == strongest:
            chosen, contributors = version, [contributor]
        elif relation == "equal":
            contributors.append(contributor)
    if chosen is None:
        return None, None
    return dict(version=contributors[0]["version"],
                inclusive=all(item["inclusive"] for item in contributors),
                contributors=contributors), chosen


def classify(lower, upper, left, right):
    if lower is None and upper is None:
        return "unconstrained"
    if lower is None or upper is None:
        return "one_sided"
    relation = compare(left, right)[0]
    if relation == "less":
        return "ordered"
    if relation == "greater":
        return "inverted"
    return "equal_closed" if lower["inclusive"] and upper["inclusive"] else "equal_open"
