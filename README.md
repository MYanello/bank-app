# bank-app

You are working with a bank that needs to manage its liquidity. Build a simple full stack application that:

- Pulls data on treasury yields
- Plots the yield curve back to the user
- Allows the user to submit an order for a specific term and amount
- Displays the user’s historical order submissions

## Architecture
### Backend
- Considered Go vs Python for the backend. Typically I would use Go for a small service like this for its speed and simplicity, but due to the rest of the team being familiar with Python and FastAPI, that overruled any gains Go would have given me.
- SQLModel was chosen as the ORM since it pairs well with Fastapi and basic usage like this. In production sqlalchemy may be a better choice for its configurability.
- For datasource there were a few non-public apis with free registration, but I chose against that so that users wouldn't need to get an api key if they wanted to run this themselves. Instead I found the daily par yield curve rates from the US Treasury API [here](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202508)
- We will cache any previous years under the assumption that the values won't change for the yields
- We will not cache or async the database due to expected active userbase being < 5
- Yield data will be stored as json for passing to the frontend when charting
### Frontend
- Chose to use basic html and js for this to not overcomplicate a simple page
- Adapted some old css from a different project I've worked on
- Just used an off the shelf npm charting plugin
### Deployment
- Will be put on my existing Kubernetes cluster for ease/speed of deployment. 
- Should be behind a Cilium gateway with a public FQDN for demo purposes.

## Running
If you have a specific port you want to run on you can choose that with `export PORT=9000`

### UV
If you have `uv` installed you can simply clone this repo and run using that 
```bash
git clone https://codeberg.org/marcusjy/bank-app.git
cd bank-app/src
uv run main.py
```
### Poetry
Otherwise, the venv can be installed with Poetry and run with that 
```bash
git clone https://codeberg.org/marcusjy/bank-app.git
cd bank-app/src
python -m venv .venv
source .venv/bin/activate
poetry install
python main.py
```
