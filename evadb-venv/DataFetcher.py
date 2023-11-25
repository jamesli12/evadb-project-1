import pandas as pd
import numpy as np

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe

class DataFetcher(AbstractFunction):
    @setup(cacheable=False, function_type="DataFetching", batchable=False)
    def setup(self):
        pass

    @property
    def name(self) -> str:
        return "DataFetcher"

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["company", "news_type"],
                column_types=[NdArrayType.STR, NdArrayType.STR],
                column_shapes=[(1), (1)],
            )
        ],
        output_signatures=[
            PandasDataframe(
                columns=["data"],
                column_types=[NdArrayType.STR],
                column_shapes=[(1)],
            )
        ],
    )
    def forward(self, df: pd.DataFrame) -> pd.DataFrame:
        def _forward(row: pd.Series) -> np.ndarray:
            import requests
            from bs4 import BeautifulSoup
            import re

            company = row.iloc[0]
            news_type = row.iloc[1]

            data = []

            uri = f"https://www.google.com/search?q={company}+Company+{news_type}+News"
            res = requests.get(uri)

            soup = BeautifulSoup(res.text, "html.parser") 
            heading_object = soup.find_all('h3') 
            for info in heading_object: 
                formatted_str = re.sub(r'\W+', ' ', info.getText()).strip()
                data.append(bytes(formatted_str, 'utf-8').decode('utf-8', 'ignore'))
            return np.array(data)

        ret = pd.DataFrame()
        ret["data"] = df.apply(_forward, axis=1)
        return ret