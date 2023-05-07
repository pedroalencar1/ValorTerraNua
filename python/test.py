
#%% import functions
import functions_resed as rsd
# %%
demand_crop = rsd.demand_from_crop(6, 0.24, 1.67, "Sorgo forrageiro",20)
demand_crop

#%% 
npk_soil_gkg = rsd.npk_to_gkg(0.51, 6, 0.24)
npk_soil_kgm3 = rsd.npk_to_kgm3(npk_soil_gkg, 1.67)
npk_soil_kgm3
# individual_bal = rsd.sediment_balance_individual(demand_crop, npk_sed)
# individual_bal

# %%

npk_sed_gkg = rsd.npk_to_gkg(3.56, 210, 0.55)
npk_sed_kgm3 = rsd.npk_to_kgm3(npk_sed_gkg, 1.17)
npk_sed_kgm3
# individual_bal = rsd.sediment_balance_individual(demand_crop, npk_sed)
# individual_bal
#%%
depth = 20
sup = "Fósforo"
# %%
depth_sed = rsd.get_mix(demand_crop, npk_soil_kgm3, npk_sed_kgm3, depth, sup)
depth_sed
# %%
deficit_new = rsd.persistent_deficit(depth_sed, demand_crop, npk_soil_kgm3, npk_sed_kgm3, depth)
deficit_new
# %%    
add_sup = rsd.additional_supplements(deficit_new, depth, 1, 1, 1)
add_sup
# %%    
vols = rsd.soil_movement(depth_sed)
vols

#%%



#%%
nutrients = ("Nitrogênio", "Fósforo", "Potássio")
expantion_factor = 1.25
    
id_sup = nutrients.index(supplement)
#%%
    
demand = np.array(list(demand_crop.values()))
soil_supply = np.array(list(npk_soil_kgm3.values()))
sed_supply = np.array(list(npk_sed_kgm3.values()))

sed_supply_exp = sed_supply/expantion_factor
    
d_sed = depth*demand[id_sup]/(sed_supply_exp[id_sup] - soil_supply[id_sup])
d_sed


#%%

supply_new = (d_sed*sed_supply_exp + (depth - d_sed)*soil_supply)/depth
# supply_new
deficit_new = demand + soil_supply - supply_new
# deficit_new
deficit_new[deficit_new<0.001] = 0
deficit_new

#%%
comb_bal = rsd.sediment_balance_combined(npk_balance = individual_bal, 
                                         npk_demand = demand_crop, 
                                         npk_sed = npk_sed)

comb_bal
# %%
bags = rsd.bags_supplement(comb_bal)
bags
# %%
prices_list = rsd.bag_price_as_list(100, 100, 197)

cost = rsd.cost_supplements(bags, prices_list)
cost
# %%
