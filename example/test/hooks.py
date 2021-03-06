from datetime import timedelta

from hypothesis import strategies as st

import schemathesis


@st.composite
def fullname(draw):
    """Custom strategy for full names."""
    first = draw(st.sampled_from(["jonh", "jane"]))
    last = draw(st.just("doe"))
    return f"{first} {last}"


schemathesis.register_string_format("fullname", fullname())


@schemathesis.hooks.register
def before_generate_body(context, strategy):
    """Modification over the default strategy for payload generation."""
    return strategy.filter(lambda x: x.get("id", 10001) > 10000)


@schemathesis.register_check
def not_so_slow(response, case):
    """Custom response check."""
    assert response.elapsed < timedelta(milliseconds=100), "Response is slow!"


@schemathesis.register_target
def big_response(context):
    """Custom data generation target."""
    return float(len(context.response.content))
