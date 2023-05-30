# ProGreen Suitability Analysis
In support of the [World Bank's ProGreen](https://www.worldbank.org/en/news/infographic/2021/03/08/progreens-initial-work-plan) program, the GOST team are developing rudimentary tools and processes for generating site suitability maps based on open geospatial layers. The goal is to provide rough guides to task teams for future investigations for suitable project locations.

The process involves identification of ~10 foundational geospatial layers, and determining each layer's contribution to identifying suitable sites. This requires applying weights to values in each dataset, according to the specific investigation of interest. In the first example, we will be looking into questions of reforestation, but this methodology could be applied to other land projects such as ...

![Suitability in Kyrgyzstan](docs/images/Suitability_beta.png)

## Input Datasets 
| Category | Indicator Name | Time-Period | Endorsed by | Dataset Name | Link | Resolution | Descritpion | Exclusion Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Geophysical | Slope | 2021   | CRIL/NBS | FABDEM V1-0 | [DEM](http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/) | 3 arc second | Yamazaki D., et al. | Exclude slope above 45 |
| Geophysical | Elevation | 2021   | CRIL/NBS | FABDEM V1-0 | [DEM](http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/) | 3 arc second | Yamazaki D., et al. | Exclude areas above 2250m  |
| Geophysical | Aspect | 2021   | CRIL/NBS | FABDEM V1-0 | [DEM](http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/) | 3 arc second | Yamazaki D., et al. | Exclude N facing  |
| Climate | Precipitation | Past data | Initial list/ESRI | Precipitation | [TerraClimate](https://climate.northwestknowledge.net/TERRACLIMATE/index_directDownloads.php) | NA | NA  | rainfall > 400mm |
| Climate | Potential Evapotranspiration | 2020 | NA | Potential Evapotranspiration | [TerraClimate](https://climate.northwestknowledge.net/TERRACLIMATE/index_directDownloads.php) | NA | TerraClim | PET > 5mm |
| Life | Soil pH | 2017 | NBS team | Soil pH in H20 at 6 standard depths | [DL](https://zenodo.org/record/2525664#.ZGPk2-zMLc8) | 250m | Tomislav Hengl. (2018) | pH > 8.4 |
| Life | Soil Organic Carbon | 2017 | NBS team | Soil organic carbon content | [Soil](https://zenodo.org/record/2525553#.ZGPf--zMLc8) | 250m | Tomislav Hengl. (2018) | < 60 tons/ha |
| Life | Land cover | 2020   | NBS team | ESA WorldCover  | [ESA](https://registry.opendata.aws/esa-worldcover-vito/) | 10m   | (Zanaga et al., 2021)  | Exclude desert, urban, and forest  |
| Life | Humans | Past data | NA | Settlement Footprints | GHSL- already have | NA  | GHSL | Exclude urban/settlement areas |
