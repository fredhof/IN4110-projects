# My strømpris API
My strømpris API is an interactive web-based visualizer that displays the current and past electricity price in Norway, aswell as it's average.

### Installation instructions
Clone the repository, "cd" into it and install the requirements with pip as `pip install -r requirements.txt`. The command may differ depending on your system. 

### Usage
It is recommended to run this through FastAPI as it provides a better user experience.
The package can be run as `python3 strompris.py` for local Altair plot or `python3 app.py` to run it through FastAPI  `localhost:5000`.

## Test
Testuing is done automatically with Pytest. Run `python3 -m pytest -v tests/`.\
Beware that this repository uses mostly alt.HConcatChart's instead of alt.Chart's so some of the test WILL fail if unmodified!
The test do however pass if one only passes one chart (that is, an alt.Chart) to pytest.