class result_loading_class:

    h2_summary = ["H2 DEMAND in TWh", "industry TWh", "trans TWh", "power TWh"]
    subsidy_summary = ["TOTAL GREEN HYDROGEN DEMAND", "Green H2 cost", "TOTAL SUBSIDIES"]

    # Define the sectors of the model
    steel_sector = ["Coal BF BOF", "Coal BF BOF CCS", "NGDRI EAF", "H2DRI EAF"]
    hvc_sector = ["Fossil naphtha", "Biogenic naphtha", "Synthetic naphtha"]
    meoh_sector = ["Grey MeOH", "Blue MeOH", "BioMeOH", "eMeOH"]
    fertilizer_sector = ["Grey NH3", "Blue NH3", "Green NH3"]
    temp_sector = ["Grey NG NM", "Blue NG NM", "Biogas NM", "H2 NM"]
    refining_sector = ["Grey refinery", "Blue refinery", "Green refinery"]
    industry_sectors = steel_sector + hvc_sector + fertilizer_sector + temp_sector + refining_sector + meoh_sector

    int_aviation_sector = ["Jetfuel consumption", "Syn kerosene consumption", "Bio kerosene consumption"]
    dom_aviation_sector = ["Jetfuel consumption dom", "Syn kerosene consumption dom", "Bio kerosene consumption dom"]
    int_shipping_sector = ["HFO shipping consumption", "NH3 shipping consumption", "MeOH shipping consumption"]
    dom_shipping_sector = ["Domestic HFO shipping consumption", "Domestic battery shipping consumption", "Domestic MeOH shipping consumption", "Domestic H2 shipping consumption"]
    ld_road_transport_sector = ["LD Fossil consumption", "LD BEV consumption", "LD FCEV consumption"]
    hd_road_transport_sector = ["HD Fossil consumption", "HD BEV consumption", "HD FCEV consumption"]
    transport_sectors = int_aviation_sector + dom_aviation_sector + int_shipping_sector + dom_shipping_sector + ld_road_transport_sector + hd_road_transport_sector

    # Define the costs for each sector
    steel_costs = ["BF Coal cost", "BF CCS cost", "NGDRI cost", "H2DRI cost"]
    hvc_costs = ["Naphtha cost", "BioNaphtha cost", "SynNaphtha cost",]
    meoh_costs = ["convMeOH cost", "Blue MeOH cost", "Green bioMeOH cost", "Green eMeOH cost"]
    fertilizer_costs = ["Grey NH3 cost", "Blue NH3 cost", "fertilizer NH3 cost"]
    temp_costs = ["Grey NG cost", "Blue NG cost", "NM H2 GJ cost", "biogas cost"]
    refining_costs = ["Grey H2 cost", "Blue H2 cost", "refinery H2 cost"]

    int_aviation_costs = ["Jetfuel cost", "SynKero cost", "BioKero cost"]
    dom_aviation_costs = ["Jetfuel cost", "SynKero cost", "BioKero cost"]
    int_shipping_costs = ["HFO containership cost", "NH3 containership cost", "MeOH containership cost"]
    dom_shipping_costs = ["HFO ship cost", "BE ship cost", "MeOH ship cost", "FC ship cost"]
    ld_road_transport_costs = ["LD ICE LCO", "LD BE LCO", "LD FC LCO"]
    hd_road_transport_costs = ["HD ICE LCO", "HD BE LCO", "HD FC LCO"]

    sectors = industry_sectors + transport_sectors

    price_break_list = ["steel H2 WTP",
                    "SynNaphtha H2 WTP", 
                    "BioNaphtha H2 WTP", 
                    "eMeOH H2 WTP",
                    "bioMeOH H2 WTP",
                    "BioKero H2 WTP",
                    "SynKero H2 WTP", 
                    "fertilizer H2 WTP", 
                    "refinery H2 WTP", 
                    "high temperature H2 WTP",
                    "LD H2 WTP", 
                    "HD H2 WTP", 
                    "NH3 containership H2 WTP", 
                    "MeOH containership H2 WTP",
                    "MeOH ship H2 WTP", 
                    "FC ship H2 WTP",
                    ]
    
    co2_wtp_list = ["steel CO2 WTP",
                    "Naphtha CO2 WTP", 
                    "convMeOH CO2 WTP",
                    "Jetfuel CO2 WTP",
                    "fertilizer CO2 WTP", 
                    "Grey NG NM CO2 WTP",
                    "Blue NG NM CO2 WTP",
                    "Grey refinery CO2 WTP",
                    "Blue refinery CO2 WTP",
                    "LD CO2 WTP", 
                    "HD CO2 WTP", 
                    "HFO containership CO2 WTP", 
                    "HFO ship CO2 WTP", 
                    ]
    
    pretty_names = {"steel": "Steel",
                    "naphtha": "High Value Chemicals",
                    "MeOH": "Methanol",
                    "fertilizer": "Fertilizer",
                    "high temperature": "High Temperature Heat",
                    "refining": "Refining",
                    "int_aviation": "International Aviation",
                    "dom_aviation": "Domestic Aviation",
                    "int_shipping": "International Shipping",
                    "dom_shipping": "Domestic Shipping",
                    "ld_road_transport": "Light Duty Road Transport",
                    "hd_road_transport": "Heavy Duty Road Transport",
                    "power": "Power",
                    "TOTAL TWh": "Total",
                    }
    
    pretty_names_technologies = {
                                "Grey NH3": "Grey Ammonia",
                                "Blue NH3": "Blue Ammonia",
                                "Green NH3": "Green Ammonia",
                                "Grey refinery": "Grey Hydrogen",
                                "Blue refinery": "Blue Hydrogen",
                                "Green refinery": "Green Hydrogen",
                                "Grey NG NM": "Grey Natural Gas",
                                "Blue NG NM": "Blue Natural Gas",
                                "Biogas NM": "Biogas",
                                "H2 NM": "Hydrogen",
                                "Grey MeOH": "Grey Methanol",
                                "Blue MeOH": "Blue Methanol",
                                "BioMeOH": "Biogenic Methanol",
                                "eMeOH": "eMethanol",
                                "Coal BF BOF": "Coal BF BOF",
                                "Coal BF BOF CCS": "Coal BF BOF CCS",
                                "NGDRI EAF": "NG DRI-EAF",
                                "H2DRI EAF": "H2 DRI-EAF",
                                "Fossil naphtha": "Fossil Naphtha",
                                "Biogenic naphtha": "Biogenic Naphtha",
                                "Synthetic naphtha": "Synthetic Naphtha",
                                "Jetfuel consumption": "Fossil Kerosene",
                                "Syn kerosene consumption": "Synthetic Kerosene",
                                "Bio kerosene consumption": "Bio Kerosene",
                                "Jetfuel consumption dom": "Jetfuel",
                                "Syn kerosene consumption dom": "Synthetic Kerosene",
                                "Bio kerosene consumption dom": "Bio Kerosene",
                                "HFO shipping consumption": "HFO",
                                "NH3 shipping consumption": "NH3",
                                "MeOH shipping consumption": "Bio-MeOH",
                                "Domestic HFO shipping consumption": "HFO",
                                "Domestic battery shipping consumption": "Battery-Electric",
                                "Domestic MeOH shipping consumption": "Bio-MeOH",
                                "Domestic H2 shipping consumption": "H2 FC",
                                "LD Fossil consumption": "Diesel ICE",
                                "LD BEV consumption": "Battery EV",
                                "LD FCEV consumption": "H2 FC EV",
                                "HD Fossil consumption": "Diesel ICE",
                                "HD BEV consumption": "Battery EV",
                                "HD FCEV consumption": "H2 FC EV",
                                }
    
    pretty_names_costs = {
                        "BF Coal cost": "Coal BF BOF",
                        "BF CCS cost": "Coal BF BOF CCS",
                        "NGDRI cost": "NG DRI-EAF",
                        "H2DRI cost": "H2 DRI-EAF",
                        "Naphtha cost": "Fossil Naphtha",
                        "BioNaphtha cost": "Biogenic Naphtha",
                        "SynNaphtha cost": "Synthetic Naphtha",
                        "convMeOH cost": "Grey Methanol",
                        "Blue MeOH cost": "Blue Methanol",
                        "Green bioMeOH cost": "Biogenic Methanol",
                        "Green eMeOH cost": "eMethanol",
                        "Grey NH3 cost": "Grey Ammonia",
                        "Blue NH3 cost": "Blue Ammonia",
                        "fertilizer NH3 cost": "Green Ammonia",
                        "Grey NG cost": "Grey Natural Gas",
                        "Blue NG cost": "Blue Natural Gas",
                        "NM H2 GJ cost": "Hydrogen",
                        "biogas cost": "Biogas",
                        "Grey H2 cost": "Grey Hydrogen",
                        "Blue H2 cost": "Blue Hydrogen",
                        "refinery H2 cost": "Green Hydrogen",
                        "Jetfuel cost": "Fossil Kerosene",
                        "SynKero cost": "Synthetic Kerosene",
                        "BioKero cost": "Bio Kerosene",
                        "HFO containership cost": "HFO",
                        "NH3 containership cost": "NH3",
                        "MeOH containership cost": "Bio-MeOH",
                        "HFO ship cost": "HFO",
                        "BE ship cost": "Battery-Electric",
                        "MeOH ship cost": "Bio-MeOH",
                        "FC ship cost": "H2 FC",
                        "LD ICE LCO": "Diesel ICE",
                        "LD BE LCO": "Battery EV",
                        "LD FC LCO": "H2 FC EV",
                        "HD ICE LCO": "Diesel ICE",
                        "HD BE LCO": "Battery EV",
                        "HD FC LCO": "H2 FC EV",
                        }

    # Define the dictionary of sectors, include a key for each sector which defines the unit used in the sector
    industry_sector_dict = {
                            "refining": {"unit": "MT H2", "stocks" : refining_sector, "h2 demand" : "refinery hydrogen demand", "emissions" : "refinery emissions", "subsidy": "refinery subsidy", "WTP": "refinery H2 WTP", "CT revenue": "refinery CT revenue", "costs": refining_costs, "CO2 WTP": "Grey refinery CO2 WTP", "cost index": "refinery cost index"},
                            "high temperature": {"unit": "GWh", "stocks" : temp_sector, "h2 demand" : "high temperature hydrogen demand", "emissions" : "high temperature emissions", "biomass": "high temperature biomass demand", "subsidy": "high temperature subsidy", "WTP": "high temperature H2 WTP", "CT revenue": "high temperature CT revenue", "costs": temp_costs, "CO2 WTP": "Grey NG NM CO2 WTP", "cost index": "high temperature cost index"},
                            "fertilizer": {"unit": "MT NH3", "stocks" : fertilizer_sector, "h2 demand" : "fertilizer hydrogen demand", "emissions" : "fertilizer emissions", "subsidy": "fertilizer subsidy", "WTP": "fertilizer H2 WTP", "CT revenue": "fertilizer CT revenue", "costs": fertilizer_costs, "CO2 WTP": "fertilizer CO2 WTP", "cost index": "fertilizer cost index"},
                            "steel": {"unit": "MT Steel", "stocks" : steel_sector, "h2 demand" : "steel hydrogen demand", "emissions" : "steel emissions", "subsidy": "steel subsidy", "WTP": "steel H2 WTP", "CT revenue": "steel CT revenue", "costs": steel_costs, "CO2 WTP": "steel CO2 WTP", "cost index": "steel cost index"},
                            "naphtha": {"unit": "MT Naphtha", "stocks" : hvc_sector, "h2 demand" : "naphtha hydrogen demand", "emissions" : "naphtha emissions", "biomass": "naphtha biomass demand", "subsidy": "naphtha subsidy", "WTP": "SynNaphtha H2 WTP", "WTP 2": "BioNaphtha H2 WTP", "CT revenue": "naphtha CT revenue", "costs": hvc_costs, "CO2 WTP": "Naphtha CO2 WTP", "cost index": "naphtha cost index"},
                            "MeOH": {"unit": "MT MeOH", "stocks" : meoh_sector, "h2 demand" : "MeOH hydrogen demand", "emissions" : "MeOH emissions", "biomass": "MeOH biomass demand", "subsidy": "MeOH subsidy", "WTP": "eMeOH H2 WTP", "WTP 2": "bioMeOH H2 WTP", "CT revenue": "MeOH CT revenue", "costs": meoh_costs, "CO2 WTP": "convMeOH CO2 WTP", "cost index": "MeOH cost index"},
                            }

    transport_sector_dict = {"int_aviation": {"unit": "GWh", "stocks" : int_aviation_sector, "h2 demand" : "international aviation hydrogen demand", "emissions" : "international aviation emissions", "biomass": "international aviation biomass demand", "subsidy": "international aviation subsidy", "WTP": "SynKero H2 WTP", "WTP 2": "BioKero H2 WTP", "CT revenue": "international aviation CT revenue", "costs": int_aviation_costs, "CO2 WTP": "Jetfuel CO2 WTP", "cost index": "international aviation cost index"},
                            "dom_aviation": {"unit": "GWh", "stocks" : dom_aviation_sector, "h2 demand" : "domestic aviation hydrogen demand", "emissions" : "domestic aviation emissions", "biomass": "domestic aviation biomass demand", "subsidy": "domestic aviation subsidy", "WTP": "SynKero H2 WTP", "WTP 2": "BioKero H2 WTP", "CT revenue": "domestic aviation CT revenue", "costs": dom_aviation_costs, "CO2 WTP": "Jetfuel CO2 WTP", "cost index": "domestic aviation cost index"},
                            "ld_road_transport": {"unit": "GWh", "stocks" : ld_road_transport_sector, "h2 demand" : "light duty hydrogen demand", "emissions" : "light duty emissions", "subsidy": "light duty subsidy", "WTP": "LD H2 WTP", "CT revenue": "light duty CT revenue", "costs": ld_road_transport_costs, "CO2 WTP": "LD CO2 WTP", "cost index": "LD cost index"},
                            "hd_road_transport": {"unit": "GWh", "stocks" : hd_road_transport_sector, "h2 demand" : "heavy duty hydrogen demand", "emissions" : "heavy duty emissions", "subsidy": "heavy duty subsidy", "WTP": "HD H2 WTP", "CT revenue": "heavy duty CT revenue", "costs": hd_road_transport_costs, "CO2 WTP": "HD CO2 WTP", "cost index": "HD cost index"},
                            "int_shipping": {"unit": "GWh", "stocks" : int_shipping_sector, "h2 demand" : "international shipping hydrogen demand", "emissions" : "international shipping emissions", "biomass": "international shipping biomass demand", "subsidy": "international shipping subsidy", "WTP": "NH3 containership H2 WTP", "WTP 2": "MeOH containership H2 WTP", "CT revenue": "international shipping CT revenue", "costs": int_shipping_costs, "CO2 WTP": "HFO containership CO2 WTP", "cost index": "international shipping cost index"},
                            "dom_shipping": {"unit": "GWh", "stocks" : dom_shipping_sector, "h2 demand" : "domestic shipping hydrogen demand", "emissions" : "domestic shipping emissions", "biomass": "domestic shipping biomass demand", "subsidy": "domestic shipping subsidy", "WTP": "MeOH ship H2 WTP", "WTP 2": "FC ship H2 WTP", "CT revenue": "domestic shipping CT revenue",  "costs": dom_shipping_costs, "CO2 WTP": "HFO ship CO2 WTP", "cost index": "domestic shipping cost index"},
                            }

    sector_dict = {"industry": industry_sector_dict, "transport": transport_sector_dict}

    hydrogen_demands = {"power" : "power hydrogen demand"}
    subsidies = {"power" : "power subsidy"}
    biomass_demands = {}
    emissions = {}
    price_breaks = {}

    for main_sector in sector_dict.keys():
        for i, (sub_sector, sub_dict) in enumerate(sector_dict[main_sector].items()):
            hydrogen_demands[sub_sector] = sub_dict["h2 demand"]
            subsidies[sub_sector] = sub_dict["subsidy"]
            emissions[sub_sector] = sub_dict["emissions"]
            price_breaks[sub_sector] = sub_dict["WTP"]
            if "WTP 2" in sub_dict.keys():
                price_breaks[sub_sector + " 2"] = sub_dict["WTP 2"]
            if "biomass" in sub_dict.keys():
                biomass_demands[sub_sector] = sub_dict["biomass"]

    sector_colors = {'power': 'lightgrey',
                    'MeOH': (0.8705882352941177, 0.5607843137254902, 0.0196078431372549),
                    'refinery': (0.00784313725490196, 0.6196078431372549, 0.45098039215686275),
                    'fertilizer': (0.8352941176470589, 0.3686274509803922, 0.0),
                    'steel': (0.8, 0.47058823529411764, 0.7372549019607844),
                    'domestic shipping': (0.792156862745098, 0.5686274509803921, 0.3803921568627451),
                    'high temperature': (0.984313725490196, 0.6862745098039216, 0.8941176470588236),
                    'naphtha': 'turquoise',
                    'international shipping': (0.9254901960784314, 0.8823529411764706, 0.2),
                    'international aviation': (0.33725490196078434, 0.7058823529411765, 0.9137254901960784),
                    'domestic aviation': (0.00392156862745098, 0.45098039215686275, 0.6980392156862745),
                    'heavy duty': 'grey',
                    'light duty': 'black'}