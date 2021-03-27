from fastapi import APIRouter


LIST_OF_TOOLS = [
    "rsi",
    "simple_moving_average",
    "exponential_moving_average",
    "windowed_moving_average",
    "on_balance_volume",
    "ultimate_oscillator",
    "moving_average_convergence_divergence"
]

router = APIRouter(
    prefix="/tools"
)


@router.get("/", tags=["Tools"])
def echo_tools():
    return {"tools available": LIST_OF_TOOLS}
