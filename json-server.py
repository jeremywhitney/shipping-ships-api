import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import list_docks, retrieve_dock, delete_dock, update_dock, create_dock
from views import (
    list_haulers,
    retrieve_hauler,
    delete_hauler,
    update_hauler,
    create_hauler,
)
from views import list_ships, retrieve_ship, delete_ship, update_ship, create_ship


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for shipping ships"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "docks":
            if url["pk"] != 0:
                response_body = retrieve_dock(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_docks()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "haulers":
            if url["pk"] != 0:
                response_body = retrieve_hauler(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_haulers()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "ships":
            if url["pk"] != 0:
                response_body = retrieve_ship(url["pk"], url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_ships(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_PUT(self):
        """Handle PUT requests from a client"""

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "ships":
            if pk != 0:
                successfully_updated = update_ship(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        elif url["requested_resource"] == "docks":
            if pk != 0:
                successfully_updated = update_dock(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "haulers":
            if pk != 0:
                successfully_updated = update_hauler(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        return self.response(
            "Requested resource not found",
            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
        )

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "ships":
            if pk != 0:
                successfully_deleted = delete_ship(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        elif url["requested_resource"] == "haulers":
            if pk != 0:
                successfully_deleted = delete_hauler(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        elif url["requested_resource"] == "docks":
            if pk != 0:
                successfully_deleted = delete_dock(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        """Handle POST requests from a client"""

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        # Define required fields for each resource type
        required_fields = {
            "ships": ["name", "hauler_id"],
            "docks": ["location", "capacity"],
            "haulers": ["name", "dock_id"],
        }

        resource = url["requested_resource"]
        if resource in required_fields:
            fields = required_fields[resource]
            if all(field in request_body for field in fields):
                if resource == "ships":
                    successfully_created = create_ship(request_body)
                elif resource == "docks":
                    successfully_created = create_dock(request_body)
                elif resource == "haulers":
                    successfully_created = create_hauler(request_body)

                if successfully_created:
                    return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    return self.response(
                        "Bad request",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
            else:
                return self.response(
                    "Missing or invalid fields",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )
        else:
            return self.response(
                "Resource not found",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
