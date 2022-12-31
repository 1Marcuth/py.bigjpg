from urllib.request import urlretrieve
from pydantic import validate_arguments
from rich import print
import httpx
import json
import time

base_url = "https://bigjpg.com/api"

class BigjpgError(Exception): ...

class BigjpgImage:
    @validate_arguments
    def __init__(self, image_url: str) -> None:
        self.__image_url = image_url

    def get_url(self) -> str:
        return self.__image_url

    @validate_arguments
    def download(self, out_path: str):
        urlretrieve(self.__image_url, out_path)

class BigjpgTask:
    @validate_arguments
    def __init__(self, url: str, task_id: str) -> None:
        self.__url = url
        self.__task_id = task_id

    def fetch_util_achieve_the_result(self):
        print(f"> [green][b][Bigjpg-info][/b][/green] [yellow]Waiting for image processing...[/yellow]")

        while True:
            response = httpx.get(self.__url)
            json_response = response.json()

            data = json_response[self.__task_id]

            status = data["status"]

            if status == "success":
                return data

            elif status == "error":
                raise BigjpgError("Error processing the image!")

            time.sleep(.5)

class Bigjpg:
    @validate_arguments
    def __init__(self, api_token: str) -> None:
        self.__api_token = api_token

    @validate_arguments
    def enlarge(
        self,
        style: str,
        noise: str,
        enlarge_value: str,
        image_url: str
    ) -> BigjpgImage:

        url = f"{base_url}/task/"
        config = {
            "style": style,
            "noise": noise,
            "x2": enlarge_value,
            "input": image_url
        }

        headers = { "X-API-KEY": self.__api_token }
        data = { "conf": json.dumps(config) }

        response = httpx.post(url, data=data, headers=headers)
        json_response: dict = response.json()

        print(json_response)

        if "status" in json_response.keys():
            status = json_response["status"]

            if status == "valid_api_key_required":
                raise BigjpgError("Invalid API token, get your API token on the website by registering 'https://bigjpg.com/' and going to the 'API' section and copying your token that is present in the example code")

            elif status == "param_error":
                raise BigjpgError("Some invalid parameter, check parameters and features available in your account and try again")

        remaining_api_calls = json_response["remaining_api_calls"]

        print(f"> [green][b][Bigjpg-info][/b][/green] [yellow]Remaining API calls:[/yellow] {remaining_api_calls}")

        task_id = json_response["tid"]
        task_url = f"{base_url}/task/{task_id}"
        task = BigjpgTask(task_url, task_id)
        task_result = task.fetch_util_achieve_the_result()
        
        image_url = task_result["url"]
        image = BigjpgImage(image_url)

        return image

__all__ = [ Bigjpg ]
#{'status': 'valid_api_key_required'}