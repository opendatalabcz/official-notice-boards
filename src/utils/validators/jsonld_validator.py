import json

from src.utils.validators.file_validator import FileValidator


class JsonLdValidator(FileValidator):
    @classmethod
    def validate(cls, file_path) -> bool:  # TODO change to differentiate between regular json and jsonld
        if not cls.check_file_path(file_path):
            return False

        with open(file_path, 'r') as file:
            try:
                json.load(file)
            except json.decoder.JSONDecodeError:
                return False
            return True


        # # check JSON-LD schema
        # with open(os.path.join("data", filename), 'r') as file:
        #     with open(os.path.join("deska_schema.json"), 'r') as schema_file:
        #         try:
        #             data = json.load(file)
        #             schema = json.load(schema_file)
        #             validate(instance=data, schema=schema)
        #         except json.decoder.JSONDecodeError:
        #             print("Error: {} is not a valid JSON file.".format(filename))
        #         except ValidationError:
        #             print("Error: {} is not a valid JSON-LD file.".format(filename))