# The Nordic Transparency Model for Analysis
The Nordic Transparency Model for Analysis, **Nordic-T**<sub>for short</sub>, is an open open research model of the Nordic Electrical Power System built on high accuracy, transparent sources gathered from its Transmission System Operators: Fingrid - Finland, Energinet - Denmark, Statnett - Norway and Svenska kraftnät - Sweden. 

It is created as part of the research project at NTNU.

This projects aim is to gather all available transparency data into one true, highly detailed Nordic Transparency Model to be used as the base-case system state model.

**All varioius transparent open data sources has been implemented into one interactive map as seen below, for all convenience.**


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
