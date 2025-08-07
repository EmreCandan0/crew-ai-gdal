import warnings
from crew import CrewTiffcropper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        "filepath":"{filepath to your image}",
        "crop_minx":0,
        "crop_miny":0,
        "crop_maxx":0,
        "crop_maxy":0
    }

    try:
        CrewTiffcropper().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
