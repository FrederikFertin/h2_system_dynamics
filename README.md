# h2_system_dynamics
## Folders
### data
This folder contains input data for the vensim model runs. This is primarily time series forecast data.

### model_considerations
This folder contains all miscellaneous files, which give general insight into the project, but does not provide directly usable data.

### python_scripts
This folder contains the python scripts, which are primarily based on the PySD library, which translates and runs Vensim models in python.

### vensim_models
This folder contains the vensim models, which are the structural and visual presentation of the system dynamics models.

### sector_breakdown
This folder contains the sector breakdown for potential hydrogen offtakers. The folder divides into subfolders for each main sector.

#### Buildings
Divided into residential and public building energy usage.

#### Industry
Covers a large number of subsectors: Oil refining, steel, ammonia, HVC, methanol, cement, glass, other

#### Power
Basis for potential hydrogen usage in the power sector: Ancillary services, peak power, seasonal storage

#### Transport
Divided into shipping, aviation, road, and rail transport.

## Development
It is free to create new Vensim models and edit existing ones.

Forecasts are needed for each sector's future H2 convertible energy demand.
Costs of energy for each sector is needed.

### Examples:
#### Shipping:
Determine area of hydrogen usage:
Marine fuels
Determine competing technologies:
MeOH, NH3, MDO, (LNG, LPG, LBG, MGO)...
Need {capex, lifetime, opex, resource needs, emission factor, capacity factor} of each technology to calculate cost of each technology/determine which one is to be invested in.

#### Cement:
Determine area of hydrogen usage:
High temperature heat >1000*C
Determine competing technologies:
Electric arc, hydrogen combustion, nat. gas direct heat?
Need {capex, lifetime, opex, resource needs, emission factor, capacity factor} of each technology to calculate cost of each technology/determine which one is to be invested in.
