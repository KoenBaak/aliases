from aliases import AliasSpace

s = AliasSpace(
    {"The Netherlands": ["NL", "Netherlands", "Holland"]}, case_sensitive=False
)

s.str("nl")

s.representative

s.str("holland") == s.str("NL")

data = {s.str("holland"): 12345}
data[s.str("nl")]

data = s.dict(holland=12345)
data["nl"]

import pandas as pd

df = pd.DataFrame(
    {"Country": ["NL", "The Netherlands", "Belgium"], "SomeData": [10, 11, 12]}
)
