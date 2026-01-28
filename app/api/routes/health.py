from fastapi import APIRouter, Response, status

health_router: APIRouter = APIRouter(
    prefix="/server",
    tags=["Server"],
)


@health_router.get(
    path="/health",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def verify_the_server_status() -> Response:
    """
    Indicates whether the server is running and ready to accept requests. If it is not running, an error will be returned.
    """

    return Response(status_code=status.HTTP_204_NO_CONTENT)
