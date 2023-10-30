from pyfio.fio_adapter import FIOAdapter
from pyfio.validators import validate_ticker
from pyfio.models.material_models import MaterialTicker, MaterialTickerList
from pyfio.exceptions import MaterialTickerNotFound, MaterialCategoryNotFound


class Material:
    def __init__(self, adapter: FIOAdapter) -> None:
        self._adapter: FIOAdapter = adapter

    def _validate_ticker(self, material_ticker: str) -> None:
        """Validates a material ticker

        Args:
            material_ticker (str): Material ticker

        Raises:
            MaterialTickerInvalid: Material ticker can't be None type
            MaterialTickerInvalid: Material ticker can't be longer than 3 characters
            MaterialTickerInvalid: Material ticker can't be shorter than 1 character
            MaterialTickerInvalid: Material ticker can't contain spaces
        """
        validate_ticker(material_ticker=material_ticker)

    def get(self, material_ticker: str) -> MaterialTicker:
        """Gets a single material from FIO

        Args:
            material_ticker (str): Material Ticker (e.g., "DW")

        Raises:
            MaterialTickerNotFound: Material Ticker was not found

        Returns:
            MaterialModel: Material
        """

        self._validate_ticker(material_ticker=material_ticker)

        (status, data) = self._adapter._do(
            http_method="get",
            endpoint=self._adapter.urls.material_get_url(
                material_ticker=material_ticker
            ),
            err_codes=[204],
        )

        if status == 200:
            return MaterialTicker.model_validate(data)
        elif status == 204:
            raise MaterialTickerNotFound("Materialticker not found")

    def all(self) -> MaterialTickerList:
        """Gets all materials from FIO

        Returns:
            MaterialModelList: List of Materials as List[MaterialModel]
        """
        (_, data) = self._adapter._do(
            http_method="get",
            endpoint=self._adapter.urls.material_allmaterials_url(),
        )
        return MaterialTickerList.model_validate(data)

    def category(self, category_name: str) -> MaterialTickerList:
        """Gets all materials of specified category

        Args:
            category_name (str): Category name (e.g., "agricultural products")

        Raises:
            MaterialCategoryNotFound: Category was not found

        Returns:
            MaterialModelList: List of Materials as List[MaterialModel]
        """
        (status, data) = self._adapter._do(
            http_method="get",
            endpoint=self._adapter.urls.material_get_category(
                category_name=category_name
            ),
            err_codes=[204],
        )

        if status == 200 and len(data) > 0:
            return MaterialTickerList.model_validate(data)
        elif status == 204 or len(data) == 0:
            raise MaterialCategoryNotFound("Material category not found")
