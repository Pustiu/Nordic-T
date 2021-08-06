# The Nordic Transparency Model for Analysis
The Nordic Transparency Model for Analysis is an open researchers model of the Nordic Electrical Power System being built on available transparent data, published by the Nordic Transmission System Operators(TSOs); *Fingrid - Finland, Energinet - Denmark, Statnett - Norway and Svenska kraftnät - Sweden, and ENTSO-E.*

Having it's offspring as this repository owners final delivery for M.Sc. in Energy and Environment at NTNU, Trondhjem Norway, although it is not yet complete, it's work will be continued as long as there is need for 50+-0.1Hz in our sockets.

Making the data and results easily available, key deliveries and interactive result displays have been included below for all convenience.


## The Nordic Transparency Modelling Sources


## Implementing the Transparent Sources in a Model

During this work, great was mad to create simple, pythonic implementations of the transparent sources into the Nordic-T modelling platform for its continuous transparent maintainance. As a result, pythonic client modules for all available transparent data sources has been created and made accessable as open repositories at [this main github site](ocrj.github.com).

## The Nordic-t Modelling Maps

### Raw-Net Transparency Data Model

This model representation is simply the transparent, raw network representations as found in the transparent sources, combined into one simple model map display. Zooming closely inn on Norway and Finland reveals their networks full contents.

<p align="center"><iframe src="data/maps/nordict_raw-net_map.html" height="500" width="700"></iframe></p>

## Network Map

<p align="center"><iframe src="nordic_state_model_map.html" height="500" width="700"></iframe></p>

## State Map

<p align="center"><iframe src="nordic_state_model_map.html" height="500" width="700"></iframe></p>

## Analysis Map

Utilizing the open source [PandaPower](https://www.pandapower.org/) open source power system modelling tool, initial solutions for the models linearized power flows solutions is seen in this analysis map.

You can edit the maps own html site [here](https://github.com/ocrj/nordic/blob/gh-pages/nordic_state_model_map.html)
