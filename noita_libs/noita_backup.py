import datetime


class NoitaBackup:
    def __init__(self, *args, **kwargs):
        self._id: str = ""

        self._name: str = ""
        self._description: str = ""
        self._date: datetime.datetime | None = None

        self.deserialize(kwargs)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def date(self) -> str | None:
        if self._date is None:
            return None

        return self._date.strftime("%Y-%m-%d")

    @property
    def id(self) -> str:
        return self._id

    @date.setter
    def date(self, new_date: str):
        if new_date == "":
            self._date = None
            return

        self._date = datetime.datetime.strptime(new_date, "%Y-%m-%d")

    @description.setter
    def description(self, new_description: str):
        self._description = new_description

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @id.setter
    def id(self, new_id: str):
        self._id = new_id

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
        }

    def deserialize(self, data: dict):
        self.id = data.get("id", "")
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.date = data.get("date", "")
